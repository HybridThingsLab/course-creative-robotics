from pythonosc.udp_client import SimpleUDPClient
from FeedbackMessage import FeedbackMessage
import time
import logging

class OSCFeedback():
    def __init__(self) -> None:
        self.osc = SimpleUDPClient("127.0.0.1", 10000)
        self.lastStopMsg = 0

    
    def send(self, msg:FeedbackMessage, args = []):
        oscmsg = ""
        match msg:
            case FeedbackMessage.IKNOSOLUTION:
                oscmsg = "iknosolution"                
            
            case FeedbackMessage.POSESAFETYVIOLATION:
                oscmsg = "posesafetyviolation"

            case FeedbackMessage.JOINTSAFETYVIOLATION:
                oscmsg = "jointsafetyviolation"
            
            case FeedbackMessage.MOVEJOINTSSTART:
                oscmsg = "movejointsstart"
            
            case FeedbackMessage.MOVEJOINTSFINISHED:
                oscmsg = "movejointsfinished"

            case FeedbackMessage.STOPPED:
                oscmsg = "stopped"
                if time.time()-self.lastStopMsg < 10:
                    return
                
                self.lastStopMsg = time.time()

            case _:
                oscmsg = "unknownfeedbacktype"
                logging.warn("There was an attempt to send an unknown feedback type")
        
        self.osc.send_message("/"+oscmsg, args)
        logging.warn("%s feeback sent", msg)   


