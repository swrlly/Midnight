from ..IPacket import IPacket

class Hit(IPacket):
    
    "Sent by client to inform server of player hitting enemy or enemy hitting you"

    def __init__(self):
        self.time = 0
        self.projectileID = 0
        self.objectID = 0
        self.playerProjectile = False
        
    def Read(self, r):
        self.time = r.ReadInt32()
        self.projectileID = r.ReadInt32()
        self.objectID = r.ReadInt32()
        self.playerProjectile = r.ReadBoolean()

    def Write(self, w):
        w.WriteInt32(self.time)
        w.WriteInt32(self.projectileID)
        w.WriteInt32(self.objectID)
        w.WriteBoolean(self.playerProjectile)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
