from ..Packet import Packet

class Escape(Packet):
    
    "Sent by client to escape to the nexus (or if you're in the nexus, go to character select)"

    def __init__(self):
        pass
        
    def Read(self, r):
        pass

    def Write(self, w):
        pass
        
    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
