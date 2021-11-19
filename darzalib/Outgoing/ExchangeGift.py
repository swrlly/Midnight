from ..IPacket import IPacket

class ExchangeGift(IPacket):
    
    "Sent by client to ?"

    def __init__(self):
        self.index = 0
        
    def Read(self, r):
        self.index = r.ReadInt32()

    def Write(self, w):
        w.WriteInt32(self.index)
        
    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
