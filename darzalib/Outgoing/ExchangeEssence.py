from ..IPacket import IPacket

class ExchangeEssence(IPacket):
    
    "Sent by client to ?"

    def __init__(self):
        self.index = 0
        self.itemType = 0
        
    def Read(self, r):
        self.index = r.ReadInt32()
        self.itemType = r.ReadInt16()

    def Write(self, w):
        w.WriteInt32(self.index)
        w.WriteInt16(self.itemType)
        
    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
