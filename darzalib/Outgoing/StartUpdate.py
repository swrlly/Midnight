from ..Packet import Packet

class StartUpdate(Packet):
    
    "Sent by client to receive the first Update packet"

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
