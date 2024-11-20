# Controlling a Universal Robot UR by OSC
:zap: Receives robot poses as OSC (Open Sound Control) messages

:car: Drives the robot to the desired pose

:x: Script stops when joints are in singularities, IK can't be reached, or security violation 

:robot: Tested with a UR5e

## Prerequisites
:snake: >= Python 3.10

:books: Library [ur-rtde](https://sdurobotics.gitlab.io/ur_rtde/index.html) by SDURobotics

:books: Library [python-osc](https://pypi.org/project/python-osc/)

## Script control 
### Logging (optional)
With the `--log` startup argument you control the talkativeness of this script choose betwwen `DEBUG, INFO, WARNING, ERROR, CRITICAL`

#### Example:

`python main.py --log DEBUG` will tell you literally everything

### Dry run (optional)
For safety purposes, controlmessages are not sent to the robot, until you start the script with the `--driverobot` argument. The script will need the **robot present, up and running**, as it really only suppresses the controlmessages. The connection to the robot is established and IK's are calculated on the machine nevertheless.

#### Example:

`python main.py --driverobot` will actually move the robot

## OSC messages and modes
The script waits for OSC messages on port 20000. By sending the commands described, you can switch through the states or modes.

### stop and switching states

Stop the robot by sending:

`\stop`

When started, the script will be in *stop-Mode*. This is the basic state from which you can enter all other states. As soon as you send another command (e.g. servoPose), the stop mode will be left, and the new state will be entered. From now on, the script will only accept osc messages, belonging to the current runstate (in our example: servoPose messages), or a stop command.

By sending a *stop* command, the robot will be stopped with a fixed deceleration. After stopping, you may send another command.


### servopose
Expects values very often and tries to drive the robot to the closest point by issueing an internal controlloop.
OSC messages have to be formed in an endeffector pose vector6d format like this:

`\servopose posX posY posZ rotX rotY rotZ rotationMode` or `\servopose posX posY posZ roll pitch yaw rotationMode`

Have a look at our [rotation modes](#rotation-modes) for a deeper understanding.

The positions are values given in meters, seen from the base (0, 0, 0). They can be negative.

The rotations are expected to be in **radians** and can be negative, too. When you are dealing with values in degrees, you have to convert them to radians first.

#### Example:
`\servopose 0 0.5 0.5 0 0 0`

### servoJoints
Similar to [servopose](#servopose), but expecting angles **in radians** for each joint.

`\servojoints j0 j1 j2 j3 j4 j5`


### movejoints
For large, joint based motions, you can use the `movejoints` command. The complete motionpath is calculated on the machine itself, you only provide the desired joint angles in **radians**, speed in **radians per second** and acceleration in **radians per second^2**. 

`\movejoints j0 j1 j2 j3 j4 j5 speed acceleration`

The underlying command is the `moveJ` command, which is blocking. No new commands can be sent during a move command. You get corresponding information (move started & stopped) via the [OSC return channel](#infos).

### rotation modes
![diagram rotation](https://upload.wikimedia.org/wikipedia/commons/5/51/Euler_AxisAngle.png)

When stated in this doc, you have to ways to provide the rotational information for your osc command:
#### 1. Euclidian rotation
This is the common way to describe rotations in robotics. You provide the rotational parts in 3 axis (X, Y, Z). These would be the blue axis in the diagram above. While this is the common way to deal with rotations robotics, it can be a little bit hard to understand.

#### 2. Euler rotation
This requires additional math, but gives you a more intuitive way to deal with rotations. These are used for example in aerospace and vehicle dynamics and describe the rotation in three angles: Roll, Pitch and Yaw. This is the green arrow in the diagram above. Within this arrow the rotations are described like here:
![rpy diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Yaw_Axis_Corrected.svg/639px-Yaw_Axis_Corrected.svg.png)

For the osc commands, all angles are expected to be **radians**. You can provide an additional argument to choose the way you'd like to send angles: the rotation mode.

1. default, 0 or no rotation mode provided: you send the angles as euclidian rotation
2. rotation mode set to 1: you send the angles as euler rotation in the order: roll, pitch, yaw

## Error management
### Errors
Unfortunately it is likely that you drive the robot into impossible or forbidden positions. There are many reasons why the robot has issues, reaching your desired pose. Some of them are:
* The robot can't find a mathematical solution (inverse kinematic) to your desired pose (e.g. the pose is too far for the robot to reach)
* The pose you wish to drive to, is not reacheable (e.g. due to safety limitations)
* The joint angles the robot needs to reach for the desired inverse kinematic are not reachable (e.g. due to safety limitations)

Fortunately we let you know about such events and stop the robot in the meantime. To do so we open an OSC feedback channel on **port 10001** where we send the corresponding messages to the errors above:
* \iknosolution
* \posesafetyviolation
* \jointsafetyviolation

If you receive such a message, there is something wrong with the pose you send. You can either try to recover by sending another pose, or move to a predefinded start position by issueing a `\movejoints` command.

### Infos
If the robot is running with a [movejoints](#movejoints) command, we will tell you with these two messages:
* \movejointsstart -> move joints started, will drop future commands
* \movejointsfinished -> move joints finished, will accept future commands

If you sent a `\stop` command, we will let you know when the robot is steady by sending back:

**\stopped**

We will send this every 10 secs to let you know the robot is steady.

## Important changes
### We lowercase OSC commands
:warning: We changed the OSC commands to listen only to lowecase commands.

Till now we implemented two ways of adressing the robot: **joints** and **poses**.


SERVOPOSE :arrow_right: servos the robot by accepting a pose

MOVEJOINTS :arrow_right: moves the robot by accepting jointq's

There could be more...

|   |   |   |
| --- | --- | --- |
|   | **move** | **servo** |
| **pose** |  | servopose |
| **joints** | movejoints | servojoints |