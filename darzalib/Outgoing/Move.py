from ..IPacket import IPacket
from ..DataStructures.GamePoint import GamePoint

class Move(IPacket):
    
    "Sent by client to inform server of our new location"

    def __init__(self):
        self.position = GamePoint(0, 0)
        self.time = 0
        self.history = []
        
    def Read(self, r):
        self.position.Read(r)
        self.time = r.ReadInt32()
        for i in range(r.ReadByte()):
            j = GamePoint(0, 0)
            j.Read(r)
            self.history.append(j)

    def Write(self, w):
        self.position.Write(w)
        w.WriteInt32(self.time)
        w.WriteByte(len(self.history))
        for i in self.history:
            i.Write(w)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
        self.position.PrintString()
