from rtde_receive import RTDEReceiveInterface as RTDEReceive


class RobotReader():
    def __init__(self, robotIp: str):
        self.robotIp = robotIp
        """RTDE read"""    
        self.rtde_r = RTDEReceive(self.robotIp)
        pass    

    def readData(self) -> dict[str, str]:
        

        try:
            data = {"actualQ": self.rtde_r.getActualQ(), "actualTCPPose": self.rtde_r.getActualTCPPose()}

            return data    
            

        except:
            print("Could not fetch data")