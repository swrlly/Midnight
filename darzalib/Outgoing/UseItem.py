from ..IPacket import IPacket
from ..DataStructures.GamePoint import GamePoint

class UseItem(IPacket):
    
    "Sent by client to use an item"

    def __init__(self):
        self.time = 0
        self.slotID = 0
        self.init = GamePoint(0,0)
        self.target = GamePoint(0,0)
        self.projectileID = 0
        
    def Read(self, r):
        self.time = r.ReadInt32()
        self.slotID = r.ReadByte()
        self.init.Read(r)
        self.target.Read(r)
        self.projectileID = r.ReadUInt16()

    def Write(self, w):
        w.WriteInt32(self.time)
        w.WriteByte(self.slotID)
        self.init.Write(w)
        self.target.Write(w)
        w.WriteUInt16(self.projectileID)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
