import sys
import signal
import logging
import argparse

from queue import Queue

from OSCReceiver import OSCReceiver
from RobotController import RobotController


def main(args):
    signal.signal(signal.SIGINT, exitgracefully)
    # Argument parser
    parser = argparse.ArgumentParser(description="Read startup arguments")
    parser.add_argument('--log', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', type=str)
    parser.add_argument("--driverobot", action='store_true')
    parser.add_argument("--docker", action='store_true')
    parsed_args = parser.parse_args(args)    

    # configure loglevel based on arguments
    loglevel = vars(parsed_args)['log']
    getattr(logging, loglevel.upper())

    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    
    logging.basicConfig(level=numeric_level)

    # get our stuff up and running
    queue = Queue(maxsize=1)

    global robot_controller
    robot_controller = RobotController(queue, vars(parsed_args)['driverobot'], vars(parsed_args)['docker'])
    robot_controller.startRobotControl()

    #TODO: osc_receiver is not written here - i guess because of blocking thread. Need to rewrite OSCReceiver to be nice and threaded
    osc_receiver = OSCReceiver(queue)

def exitgracefully(sig, frame):
    global robot_controller
    robot_controller.cancel()
    print("Sänk you for trävelling wif oh äs si - teik kähr änd gut bei\r\n")
    sys.exit()

    
    

if __name__ == "__main__":
    main(sys.argv[1:])
    