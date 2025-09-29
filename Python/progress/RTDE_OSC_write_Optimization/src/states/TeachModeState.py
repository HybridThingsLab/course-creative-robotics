from states.RobotState import RobotState
from states.RobotStateType import RobotStateType
import rtde_receive
import rtde_control

class TeachModeState(RobotState):
    def __init__(self, statetype: RobotStateType, rtde_r: rtde_receive.RTDEReceiveInterface, rtde_c: rtde_control.RTDEControlInterface, driveRobot: bool) -> None:
        super().__init__(statetype, rtde_r, rtde_c, driveRobot)

    def enter(self):
        super().enter()
        if(self.driveRobot):
            self.rtde_c.teachMode()            
    
    def run(self) -> None:
        return super().run()
    
    def leave(self):
        super().leave()
        if self.driveRobot:
            self.rtde_c.endTeachMode()
    