from ..IPacket import IPacket

class SwapAck(IPacket):
    
    "Sent by server to inform client if the swap was successful"

    def __init__(self):
        self.success = False
        
    def Read(self, r):
        self.success = r.ReadBoolean()

    def Write(self, w):
        w.WriteBoolean(self.success)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
