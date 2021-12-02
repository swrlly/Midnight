from ..IPacket import IPacket

class Update(IPacket):
    
    "Sent by server to inform client of new mana"

    def __init__(self):
        self.updateID = 0
        self.removedObjects = []
        self.objectStats
        
    def Read(self, r):
        self.mana = r.ReadInt16()

    def Write(self, w):
        w.WriteInt16(self.mana)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
