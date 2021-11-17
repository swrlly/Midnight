from ..Packet import Packet

class CheckPing(Packet):
    
    "Sent by client to ?"

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
