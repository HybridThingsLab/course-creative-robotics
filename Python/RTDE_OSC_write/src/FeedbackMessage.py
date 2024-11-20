from enum import Enum

class FeedbackMessage(Enum):
    IKNOSOLUTION = 0; '''Send when i don't find a solution for the requested IK'''
    POSESAFETYVIOLATION = 1; '''Send when the pose is violating safety limitations (safetyzones etc...)'''
    JOINTSAFETYVIOLATION = 2; '''Send when the joints are violating safety limitations (max angles etc...)'''
    MOVEJOINTSSTART = 3; '''Send when i started an MoveJ command'''
    MOVEJOINTSFINISHED = 4; '''Send when i finished an MoveJ command'''
    STOPPED = 5; '''Send when the robot is stopped'''