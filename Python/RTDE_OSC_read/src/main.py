import sys
import json
import argparse
import asyncio
from RobotReader import RobotReader
from OSCSender import OSCSender




def main(args):
    readController = ReadController(args)
        
    
class ReadController():   
    
    def __init__(self, args) -> None:
        args = self.parse_args(args)
        

        config = self.read_config()
        if (config == -1):
            raise Exception("The configuration was not read correctly")
        
        print("Connect to robot with IP " + config['configs'][args.conf]['ip'])

        self.robotReader = RobotReader(robotIp = config['configs'][args.conf]['ip'])

        self.oscSender = OSCSender()

        """kick off reading"""
        asyncio.run(self.readLoop())

        pass

    
    def read_config(self):
        conf_file = open('config.json')
        config = json.load(conf_file)
        conf_file.close()
        return config

    def parse_args(self, args):   
        parser = argparse.ArgumentParser(description = "RTDE OSC reader")
        parser.add_argument(
            "-conf",
            "--configuration",
            dest="conf",
            help="The configuration to start the reader with",
            type=str,
            default="ur5e_htlab",
            metavar="<The configuration to start the reader with>"
        )

        return parser.parse_args(args)
    
        
    async def readLoop(self):

        while True:
            """read Data"""
            self.data = self.robotReader.readData()

            """rework Data"""

            """send Data via OSC"""
            self.oscSender.sendData(self.data)
            await asyncio.sleep(1/10)
        

if __name__ == "__main__":
    main(sys.argv[1:])