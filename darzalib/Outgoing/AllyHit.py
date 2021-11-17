from ..Packet import Packet

class AllyHit(Packet):
    
    "Sent by client when an ally has been hit by a projectile"

    def __init__(self):
        self.time = 0
        self.projectileID = 0
        self.objectID = 0
        
    def Read(self, r):
        self.time = r.ReadInt32()
        self.projectileID = r.ReadInt32()
        self.objectID = r.ReadInt32()

    def Write(self, w):
        w.WriteInt32(self.time)
        w.WriteInt32(self.projectileID)
        w.WriteInt32(self.objectID)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
