from ..Packet import Packet

class BiomeDisplay(Packet):
    
    "Sent by client to escape to the nexus (or if you're in the nexus, go to character select)"

    def __init__(self):
        self.biome = ""
        self.levels = ""
        
    def Read(self, r):
        self.biome = r.ReadString8()
        self.levels = r.ReadString8()

    def Write(self, w):
        w.WriteString8(self.biome)
        w.WriteString8(self.levels)

    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
