from threading import Thread
from queue import Queue
from QueueData import QueueData
from OSCFeedback import OSCFeedback
from FeedbackMessage import FeedbackMessage
from states.StopState import StopState
from states.ServoPoseState import ServoPoseState
from states.MoveJointsState import MoveJointsState
from states.RobotStateType import RobotStateType
from states.RobotState import RobotState
from states.TeachModeState import TeachModeState
from states.ServoJointsState import ServoJointsState
from states.RotationModeType import RotationModeType

import logging
import rtde_receive
import rtde_control
import time


class RobotController(Thread):
    def __init__(self, dataQueue: Queue, driveRobot: bool):

        self.stopRequest = False

        # prepare robot connection
        #self.robotIP = "192.168.178.83"
        self.robotIP = "127.0.0.1"

        # Control/update loop rate (Hz). Use 125 for CB-series, up to 500 for e-Series.
        self.readFreq = 500

        self.dataQueue = dataQueue
        self.driveRobot = driveRobot
        self.feedback = OSCFeedback()

        # connect to the robot
        logging.info('Connecting to robot %s', self.robotIP)
        self.rtde_c = rtde_control.RTDEControlInterface(self.robotIP)
        self.rtde_r = rtde_receive.RTDEReceiveInterface(self.robotIP)

        # prepare runstates
        self.stopState = StopState(RobotStateType.STOP, self.rtde_r, self.rtde_c, self.driveRobot)
        self.servoPoseState = ServoPoseState(RobotStateType.SERVOPOSE, self.rtde_r, self.rtde_c, driveRobot)
        self.servoJointsState = ServoJointsState(RobotStateType.SERVOJOINTS, self.rtde_r, self.rtde_c, self.driveRobot)
        self.moveJointsState = MoveJointsState(RobotStateType.MOVEJOINTS, self.rtde_r, self.rtde_c, self.driveRobot)
        self.teachModeState = TeachModeState(RobotStateType.TEACHMODE, self.rtde_r, self.rtde_c, self.driveRobot)

        self.previousRunState = None
        self.runState = self.stopState

        logging.info("Connected!")
        Thread.__init__(self)

    def __flushQueue(self):
        # drop all previously sent commands
        with self.dataQueue.mutex:
            self.dataQueue.queue.clear()
            self.dataQueue.all_tasks_done.notify_all()
            self.dataQueue.unfinished_tasks = 0

    def __fetchQueueData(self) -> dict:
        if self.dataQueue.empty():
            return {QueueData.EMPTYQUEUE: None}

        data = self.dataQueue.get()
        logging.debug("Got new Queue Data %s", data)
        self.dataQueue.task_done()

        # Match queue data to runstates
        queuedRunstate: RobotState = None
        key = list(data.keys())[0]

        if key == QueueData.SERVOPOSE:
            queuedRunstate = self.servoPoseState
        elif key == QueueData.MOVEJOINTS:
            queuedRunstate = self.moveJointsState
        elif key == QueueData.SERVOJOINTS:
            queuedRunstate = self.servoJointsState
        elif key == QueueData.STOP:
            queuedRunstate = self.stopState
        elif key == QueueData.TEACHMODE:
            queuedRunstate = self.teachModeState
        else:
            # Unknown data type; ignore
            return

        # Ensure the data belongs to the current runstate, otherwise switch states
        if self.runState.getStateType() != queuedRunstate.getStateType():
            if self.runState.statetype == RobotStateType.STOP:
                # From STOP we can switch to other states
                self.changeState(queuedRunstate)
                logging.info("Changed runstate from %s to %s",
                             self.previousRunState.getStateType(), self.runState.getStateType())

            elif queuedRunstate.getStateType() == RobotStateType.STOP:
                logging.info("Received stop request - entering stop state")
                self.changeState(self.stopState)

            else:
                logging.warning("Data %s does not match current runstate %s",
                                queuedRunstate.getStateType(), self.runState.getStateType())
                return

        # Update current runstate with payload
        if key == QueueData.SERVOPOSE:
            # early return when the transform matrix is malformed
            if len(data[QueueData.SERVOPOSE]) < 6:
                logging.warning("Transformmatrix malformed")
                return

            # Reform to list matching std::vector<double> &x
            transformdata = list(map(float, data[QueueData.SERVOPOSE][:6]))
            logging.debug("ServoPose transform: %s", transformdata)

            rotationmode = 0
            if len(data[QueueData.SERVOPOSE]) == 7:
                rotationmode = int(data[QueueData.SERVOPOSE][6])

            if rotationmode == 0:
                self.runState.setRobotPose(transformdata, RotationModeType.RxRyRz)
            elif rotationmode == 1:
                self.runState.setRobotPose(transformdata, RotationModeType.RPY)
            else:
                logging.warning("Invalid rotation mode provided: %s", rotationmode)
                self.runState.setRobotPose(transformdata, RotationModeType.RxRyRz)

        elif key == QueueData.MOVEJOINTS:
            if len(data[QueueData.MOVEJOINTS]) != 8:
                logging.warning("Movejoints values malformed")
                return

            jointdata = list(map(float, data[QueueData.MOVEJOINTS][:6]))
            speed = float(data[QueueData.MOVEJOINTS][6])
            acceleration = float(data[QueueData.MOVEJOINTS][7])

            logging.debug("MoveJoints: q=%s, v=%s, a=%s", jointdata, speed, acceleration)
            self.runState.setJoints(jointdata, speed, acceleration)

        elif key == QueueData.SERVOJOINTS:
            if len(data[QueueData.SERVOJOINTS]) != 6:
                logging.warning("Servojoints values malformed")
                return

            jointdata = list(map(float, data[QueueData.SERVOJOINTS]))
            self.runState.setJoints(jointdata)

        # STOP / TEACHMODE carry no extra payload beyond the state switch

    def startRobotControl(self):
        # kick off thread
        self.start()

    def cancel(self):
        self.stopRequest = True

    def run(self):

        
        logging.info("RobotWriteLoop started with state %s", self.runState)

        dt = 1.0 / self.readFreq
        next_t = time.perf_counter()

        try:
            while self.stopRequest is False:
                # 1) Receive new data and update states
                self.__fetchQueueData()

                # 2) Run current state for this tick (non-blocking)
                #    Prefer run(dt); fall back to run() for legacy states
                try:
                    self.runState.run(dt)
                except TypeError:
                    self.runState.run()

                # 3) Phase-locked sleep for deterministic cadence
                next_t += dt
                delay = next_t - time.perf_counter()
                if delay > 0:
                    time.sleep(delay)
                else:
                    # Overrun; resync without trying to "catch up"
                    next_t = time.perf_counter()
            else:
                # Stop the Robot and return
                self.changeState(self.stopState)
                self.runState.run()
                return

        except KeyboardInterrupt:
            logging.info("Robot writer stopped by keyboard interrupt")

    def changeState(self, newState: RobotState):
        self.__flushQueue()
        self.previousRunState = self.runState
        self.runState.leave()
        self.runState = newState
        self.runState.enter()
