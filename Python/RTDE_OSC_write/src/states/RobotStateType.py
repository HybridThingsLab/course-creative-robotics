from enum import Enum

class RobotStateType(Enum):
    STOP = 0
    MOVEJOINTS = 1
    SERVOPOSE = 2
    TEACHMODE = 3
    SERVOJOINTS = 4

