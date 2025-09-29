from states.RobotState import RobotState
from FeedbackMessage import FeedbackMessage
import states.RobotStateType
import logging

import rtde_receive
import rtde_control
from states.RobotStateType import RobotStateType

class ServoJointsState(RobotState):
    def __init__(self, statetype: RobotStateType, rtde_r: rtde_receive.RTDEReceiveInterface, rtde_c: rtde_control.RTDEControlInterface, driveRobot: bool) -> None:
        super().__init__(statetype, rtde_r, rtde_c, driveRobot)
        
        self.velocity = 0.5
        self.acceleration = 0.5
        self.dt = 1.0/500  # 2ms
        self.lookahead_time = 0.2
        self.gain = 100

        self.jointQ = None
    
    def enter(self):
        return super().enter()

    
    def run(self) -> None:
        super().run()
        if self.driveRobot:
            t_start = self.rtde_c.initPeriod()
            self.rtde_c.servoJ(self.jointQ, self.velocity, self.acceleration, self.dt, self.lookahead_time, self.gain)        
            self.rtde_c.waitPeriod(t_start)
    
    def leave(self):
        return super().leave()
    
    def setJoints(self, jointData):
        self.jointQ = jointData