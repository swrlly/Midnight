from ..Packet import Packet
from ..DataStructures.GameColor import GameColor
from ..DataStructures.ChatItem import ChatItem

class Chats(Packet):
    
    "Sent by client to escape to the nexus (or if you're in the nexus, go to character select)"

    def __init__(self):
        self.chats = []
        
    def Read(self, r):
        for _ in range(r.ReadInt32()):
            c = GameColor(255, 0, 0, 0)
            c.Read(r)
            ownerID = r.ReadInt32()
            text = r.ReadString8()
            self.chats.append(ChatItem(c, ownerID, text))

    def Write(self, w):
        w.WriteInt32(len(self.chats))
        for i in self.chats:
            i.color.Write(w)
            w.WriteInt32(i.ownerID)
            w.WriteString8(i.text)
        
    def GetType(self):
        return super().GetType()

    def PrintString(self):
       for j in self.chats:
           j.PrintString()
