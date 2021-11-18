from ..Packet import Packet

class ProjectilesAck(Packet):
    
    "Sent by client to acknowledge receiving a Projectiles packet"

    def __init__(self):
        self.projectileID = 0
        self.time = 0
        
    def Read(self, r):
        self.projectileID = r.ReadInt32()
        self.time = r.ReadInt32()

    def Write(self, w):
        w.WriteInt32(self.projectileID)
        w.WriteInt32(self.time)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
