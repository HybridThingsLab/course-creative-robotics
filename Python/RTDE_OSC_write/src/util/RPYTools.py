import math
from .MatMult import matrix_multiply

def RPYtoVec(roll,pitch,yaw):
    yawMatrix = [
    [math.cos(yaw), -math.sin(yaw), 0],
    [math.sin(yaw), math.cos(yaw), 0],
    [0, 0, 1]
    ]

    pitchMatrix = [
    [math.cos(pitch), 0, math.sin(pitch)],
    [0, 1, 0],
    [-math.sin(pitch), 0, math.cos(pitch)]
    ]

    rollMatrix = [
    [1, 0, 0],
    [0, math.cos(roll), -math.sin(roll)],
    [0, math.sin(roll), math.cos(roll)]
    ]

    YP = matrix_multiply(yawMatrix, pitchMatrix)
    R = matrix_multiply(YP, rollMatrix)

    theta = math.acos(((R[0][0] + R[1][1] + R[2][2]) - 1) / 2)
    multi = 1 / (2 * math.sin(theta))

    rx = multi * (R[2][1] - R[1][2]) * theta
    ry = multi * (R[0][2] - R[2][0]) * theta
    rz = multi * (R[1][0] - R[0][1]) * theta

    return rx, ry, rz
