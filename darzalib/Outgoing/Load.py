from ..IPacket import IPacket

class Load(IPacket):
    
    "Sent by client to request to load a character"

    def __init__(self):
        self.charID = 0
        
    def Read(self, r):
        self.charID = r.ReadInt64()

    def Write(self, w):
        w.WriteInt64(self.charID)
        
    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
