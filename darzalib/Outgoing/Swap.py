from ..IPacket import IPacket

class Swap(IPacket):
    
    "Sent by client to swap items"

    def __init__(self):
        self.ownerA = 0
        self.slotA = 0
        self.ownerB = 0
        self.slotB = 0
        
    def Read(self, r):
        self.ownerA = r.ReadInt32()
        self.slotA = r.ReadByte()
        self.ownerB = r.ReadInt32()
        self.slotB = r.ReadByte()

    def Write(self, w):
        w.WriteInt32(self.ownerA)
        w.WriteByte(self.slotA)
        w.WriteInt32(self.ownerB)
        w.WriteByte(self.slotB)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
