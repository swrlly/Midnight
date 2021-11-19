from ..IPacket import IPacket
from ..DataStructures.GamePoint import GamePoint

class PlayEffect(IPacket):
    
    "Sent by server to play an effect"

    def __init__(self):
        self.effect = 0
        self.onObject = 0
        self.area = 0
        self.position = GamePoint(0,0)
        self.delay = 0
        
    def Read(self, r):
        self.effect = r.ReadByte()
        self.onObject = r.ReadInt32()
        self.area = r.ReadFloat()
        self.position.Read(r)
        self.delay = r.ReadFloat()

    def Write(self, w):
        w.WriteByte(self.effect)
        w.WriteInt32(self.onObject)
        w.WriteFloat(self.area)
        self.position.Write(w)
        w.WriteFloat(self.delay)
        
    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
