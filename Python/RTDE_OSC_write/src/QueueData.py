from enum import Enum

class QueueData(Enum):
    SERVOPOSE = 1
    EMPTYQUEUE = 2
    MOVEJOINTS = 3
    TEACHMODE = 4
    STOP = 0
    SERVOJOINTS = 5