from ..Packet import Packet
from ..DataStructures.GamePoint import GamePoint

class Shoot(Packet):
    
    "Sent by client when you shoot with primary weapon"

    def __init__(self):
        self.position = GamePoint(0,0)
        self.angle = 0
        self.time = 0
        self.bulletID = 0
        self.bulletIndex = 0
        
    def Read(self, r):
        self.position.Read(r)
        self.angle = r.ReadFloat()
        self.time = r.ReadInt32()
        self.bulletID = r.ReadUInt16()
        self.bulletIndex = r.ReadByte()

    def Write(self, w):
        self.position.Write(w)
        w.WriteFloat(self.angle)
        w.WriteInt32(self.time)
        w.WriteUInt16(self.bulletID)
        w.WriteByte(self.bulletIndex)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
