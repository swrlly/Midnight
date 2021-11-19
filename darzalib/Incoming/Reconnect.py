from ..IPacket import IPacket

class Reconnect(IPacket):
    
    "Sent by server to inform client of the new ip/host of the new location to connect to"

    def __init__(self):
        self.host = ""
        self.port = 0
        
    def Read(self, r):
        self.host = r.ReadString32()
        self.port = r.ReadInt32()

    def Write(self, w):
        w.WriteString32(self.host)
        w.WriteInt32(self.port)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
