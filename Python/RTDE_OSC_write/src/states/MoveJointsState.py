from states.RobotState import RobotState
from states.RobotStateType import RobotStateType
import logging
from FeedbackMessage import FeedbackMessage
import math
import rtde_receive
import rtde_control



class MoveJointsState(RobotState):
    def __init__(self, statetype: RobotStateType, rtde_r: rtde_receive.RTDEReceiveInterface, rtde_c: rtde_control.RTDEControlInterface, driveRobot: bool) -> None:
        super().__init__(statetype, rtde_r, rtde_c, driveRobot)
        self.jointdata = None
        self.acceleration = None
        self.speed = None
        self.distanceThreshold = 0.01        

    def setJoints(self, jointdata, speed, acceleration):
        self.jointdata = jointdata
        self.acceleration = acceleration
        self.speed = speed

    def enter(self):        
        return super().enter()
    
    def run(self) -> None:
        posenow = self.rtde_r.getActualTCPPose()
        logging.debug("Actual Pose %s", posenow)

        jointq = self.rtde_r.getActualQ()
        logging.debug("Actual joint positions in degree %s", list(map(lambda x:math.degrees(x), jointq)))       
        
        if(abs(math.dist(self.jointdata, jointq)) < self.distanceThreshold):
            logging.debug("Drive suppressed: Joint distance from target %s", math.dist(self.jointdata, jointq))
            
        else:        
            logging.debug("JointsWithinSafetyLimits result:%s", self.rtde_c.isJointsWithinSafetyLimits(self.jointdata))

            if (not self.rtde_c.isJointsWithinSafetyLimits(self.jointdata)):
                self.feedback.send(FeedbackMessage.JOINTSAFETYVIOLATION)
                return
            
            #recalculate TCPPose according to FK
            targetpose = self.rtde_c.getForwardKinematics(self.jointdata, [0, 0, 0.175, 0, 0, 0])      
            logging.debug("MoveJoint requested to pose %s", targetpose)       
                
            if(not self.rtde_c.isPoseWithinSafetyLimits(targetpose)):
                self.feedback.send(FeedbackMessage.POSESAFETYVIOLATION)
                return
                        

            if(self.driveRobot):            
                self.feedback.send(FeedbackMessage.MOVEJOINTSSTART)
                logging.debug('Moving to %s, with speed %s, acceleration %s', self.jointdata, self.speed, self.acceleration)
                self.rtde_c.moveJ(self.jointdata, self.speed, self.acceleration, False)
                self.feedback.send(FeedbackMessage.MOVEJOINTSFINISHED)

            logging.debug("Arrived at pose %s", self.rtde_r.getActualTCPPose())
            
    
    def leave(self):
        return super().leave()