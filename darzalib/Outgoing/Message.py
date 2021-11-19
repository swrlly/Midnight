from ..IPacket import IPacket

class Message(IPacket):
    
    "Sent by client to send a message"

    def __init__(self):
        self.key = ""
        self.hasValue = False
        self.value = ""
        
    def Read(self, r):
        self.key = r.ReadString8()
        self.hasValue = r.ReadBoolean()
        if self.hasValue: self.value = r.ReadString8()

    def Write(self, w):
        w.WriteString8(self.key)
        w.WriteBoolean(self.hasValue)
        if self.hasValue: w.WriteString8(self.value)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
        self.position.PrintString()
