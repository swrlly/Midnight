from ..IPacket import IPacket

class MapInfoAck(IPacket):
    
    "Sent by client to ack MapInfo"

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
