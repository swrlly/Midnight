from ..IPacket import IPacket

class Create(IPacket):
    
    "Sent by client to create a new character"

    def __init__(self):
        self.objectID = 0
        self.charcterType = 0
        
    def Read(self, r):
        self.objectID = r.ReadInt32()
        self.characterType = r.ReadInt16()

    def Write(self, w):
        w.WriteInt32(self.objectID)
        w.WriteInt16(self.characterType)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
