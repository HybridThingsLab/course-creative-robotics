from pythonosc.udp_client import SimpleUDPClient
from pythonosc import osc_bundle_builder
from pythonosc import osc_message_builder


class OSCSender():
    def __init__(self):
        self.oscclient = SimpleUDPClient("127.0.0.1", 10002)
        pass

    def sendData(self, data: dict):
        #print(f"OSC send {data}")
        bundle = osc_bundle_builder.OscBundleBuilder(
            osc_bundle_builder.IMMEDIATELY)       
        
        for i,v in enumerate(data["actualQ"]):
            msg = osc_message_builder.OscMessageBuilder(address='/ur5e/actualQ/'+str(i))            
            msg.add_arg(v)
            bundle.add_content(msg.build())

        for i,v in enumerate(data["actualTCPPose"]):
            msg = osc_message_builder.OscMessageBuilder(address='/ur5e/actualTCPPose/'+str(i))            
            msg.add_arg(v)
            bundle.add_content(msg.build())


        sub_bundle = bundle.build()
        bundle.add_content(sub_bundle)

        bundle = bundle.build()
        self.oscclient.send(bundle)
        pass

