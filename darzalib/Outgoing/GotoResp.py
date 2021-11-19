from ..IPacket import IPacket

class GotoResp(IPacket):
    
    "Sent by client to ack Gotos"

    def __init__(self):
        self.time = 0
        
    def Read(self, r):
        self.time = r.ReadInt32()

    def Write(self, w):
        w.WriteInt32(self.time)
        
    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
