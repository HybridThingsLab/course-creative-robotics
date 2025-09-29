from OSCFeedback import OSCFeedback
from states.RobotStateType import RobotStateType

import rtde_receive
import rtde_control

class RobotState:
    def __init__(self, statetype:RobotStateType, rtde_r:rtde_receive.RTDEReceiveInterface, rtde_c:rtde_control.RTDEControlInterface, driveRobot:bool) -> None:
        self.statetype = statetype
        self.rtde_r = rtde_r
        self.rtde_c = rtde_c
        self.driveRobot = driveRobot
        self.feedback = OSCFeedback()

    def enter(self):
        """once called when the state is entered"""

    def run(self) -> None:
        """run the state"""
        pass

    def leave(self):
        """leave the state"""
        pass

    def getStateType(self) -> RobotStateType:
        """return state type"""
        return self.statetype