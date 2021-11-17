from ..Packet import Packet

class Chat(Packet):
    
    "Packet representing player message sent from chatbar"

    def __init__(self):
        self.text = ""
        
    def Read(self, r):
        self.text = r.ReadString8()

    def Write(self, w):
        w.WriteString8(self.text)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
