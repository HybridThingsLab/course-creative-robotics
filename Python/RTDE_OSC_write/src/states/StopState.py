from states.RobotState import RobotState
import states.RobotStateType
from FeedbackMessage import FeedbackMessage

import rtde_receive
import rtde_control

class StopState(RobotState):
    def __init__(self, statetype: states.RobotStateType, rtde_r: rtde_receive.RTDEReceiveInterface, rtde_c: rtde_control.RTDEControlInterface, driveRobot: bool) -> None:
        super().__init__(statetype, rtde_r, rtde_c, driveRobot)
       
    def enter(self):        
        self.rtde_c.servoStop(2.0)          
        pass

    def run(self):
        if self.rtde_c.isSteady():
            self.feedback.send(FeedbackMessage.STOPPED)
        
        pass

    def leave(self):
        pass