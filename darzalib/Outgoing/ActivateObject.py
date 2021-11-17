from ..Packet import Packet

class ActivateObject(Packet):
    
    "Sent by client to activate an object, such as using a portal/buying an item"

    def __init__(self):
        self.objectID = 0
        self.value = ""
        
    def Read(self, r):
        self.objectID = r.ReadInt32()
        self.value = r.ReadString32()

    def Write(self, w):
        w.WriteInt32(self.objectID)
        w.WriteString32(self.value)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
