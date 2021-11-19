from ..IPacket import IPacket

class Hello(IPacket):

    "Sent by client to initiate the handshake."

    def __init__(self):
        self.accessToken = ""
        self.version = ""
        self.assetSum = 0
        self.platform = 0
        self.loadID = 0
        self.assetsID = 0

    def Read(self, r):
        self.accessToken = r.ReadString8()
        self.version = r.ReadString8()
        self.assetSum = r.ReadInt32()
        self.platform = r.ReadByte()
        self.loadID = r.ReadInt64()
        self.assetsID = r.ReadInt32()

    def Write(self, w):
        w.WriteString8(self.accessToken)
        w.WriteString8(self.version)
        w.WriteInt32(self.assetSum)
        w.WriteByte(self.platform)
        w.WriteInt64(self.loadID)
        w.WriteInt32(self.assetsID)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()