from ..IPacket import IPacket

class EditEssence(IPacket):
    
    "Sent by client to ?"

    def __init__(self):
        self.index = 0
        self.drop = False
        self.essenceType = 0
        
    def Read(self, r):
        self.index = r.ReadInt32()
        self.drop = r.ReadBoolean()
        if not self.drop:
            this.essenceType = r.ReadInt32()

    def Write(self, w):
        w.WriteInt32(self.index)
        w.WriteBoolean(self.drop)
        if not self.drop:
            w.WriteInt32(self.essenceType)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
