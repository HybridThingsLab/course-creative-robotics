from queue import Queue
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from QueueData import QueueData
import asyncio
import logging

class OSCReceiver():

    def add_value_to_queue(self, key, value):
        data = {key: value}
        
        try:
            self.oscqueue.put(item=data, block=False) #Put the item onto the queue without waiting for a free slot
            logging.debug(f"Adding {data} to queue")
        except:
            #TODO: proper error handling
            # https://stackoverflow.com/questions/53148112/python-3-handling-error-typeerror-catching-classes-that-do-not-inherit-from-bas
            pass     

    def handleServoPose(self, address, *args):
        logging.debug("Address: %s", address)
        for v in args:
            logging.debug("Value: %s", v)

        """recheck Address"""
        if(address[1:] == "servopose"):
            """TIL Touchdesigner can also send NIL's - catch it"""
            for v in args:
                if v == None:
                    return
                
            self.add_value_to_queue(key = QueueData.SERVOPOSE, value = args)
        else:
            logging.warning("Address: %s, does not match servopose", address[1:])
        
    def handleMoveJoints(self, address, *args):
        logging.debug("Address: %s", address)
        for v in args:
            if v == None:
                return
        
        if(address[1:] == "movejoints"):
            self.add_value_to_queue(key = QueueData.MOVEJOINTS, value = args)
        else:
            logging.warning("Address: %s, does not match movejoints", address[1:])    

    def handleStop(self, address, *args):
        logging.debug("Address: %s", address)
        if(address[1:] == "stop"):
            self.add_value_to_queue(key = QueueData.STOP, value = True)
        else:
            logging.warning("Address: %s, does not match stop", address[1:])
    
    def handleTeachMode(self, address, *args):
        logging.debug("Address %s", address)
        if(address[1:] == "teachmode"):
            self.add_value_to_queue(key = QueueData.TEACHMODE, value = True)

        else:
            logging.warning("Address: %s, does not match teachmode", address[1:])
    
    def handleServoJoints(self, address, *args):
        logging.debug("Address %s", address)
        if(address[1:] == "servojoints"):
            for v in args:
                if v == None:
                    return
            
            self.add_value_to_queue(key = QueueData.SERVOJOINTS, value = args)
        else:
            logging.warning("Address: %s, does not match servojoints", address[1:])

    async def loop(self):
       while True:            
            await asyncio.sleep(1)

    async def init_main(self, ip, port, dispatcher):
        server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

        await self.loop()  # Enter main loop of program

        transport.close()  # Clean up serve endpoint

    #MB use a queue later on to transfer data in threads
    def __init__(self, oscqueue:Queue) -> None:
    
        self.oscqueue = oscqueue
        dispatcher = Dispatcher()        
        dispatcher.map("/servopose", self.handleServoPose)
        dispatcher.map("/movejoints", self.handleMoveJoints)
        dispatcher.map("/stop", self.handleStop)
        dispatcher.map("/teachmode", self.handleTeachMode)
        dispatcher.map("/servojoints", self.handleServoJoints)
        
        

        ip = "localhost"
        #ip = "192.168.188.78"
        port = 10001

        #server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())        
        #self.transport, protocol = server.create_serve_endpoint()  # Create datagram endpoint and start serving
        #server.serve()

        server = BlockingOSCUDPServer((ip, port), dispatcher)
        server.serve_forever()
        #await self.loop()  # Enter main loop of program

        #self.transport.close()  # Clean up serve endpoint






   








