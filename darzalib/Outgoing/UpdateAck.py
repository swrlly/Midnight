from ..IPacket import IPacket

class UpdateAck(IPacket):
    
    "Sent by client to ack Update"

    def __init__(self):
        self.updateID = 0
        self.time = 0
        
    def Read(self, r):
        self.updateID = r.ReadInt32()
        self.time = r.ReadInt32()

    def Write(self, w):
        w.WriteInt32(self.updateID)
        w.WriteInt32(self.time)
        
    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
