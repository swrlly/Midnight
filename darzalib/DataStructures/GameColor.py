from .IDataStructure import IDataStructure

class GameColor(IDataStructure):

    def __init__(self, a, r, g, b):
        self.a = a
        self.r = r
        self.g = g
        self.b = b

    def Read(self, r):
        self.a = r.ReadByte()
        if self.a == 0: return
        self.r = r.ReadByte()
        self.g = r.ReadByte()
        self.b = r.ReadByte()

    def Write(self, w):
        w.WriteByte(self.a)
        if self.a == 0: return
        w.WriteByte(self.r)
        w.WriteByte(self.g)
        w.WriteByte(self.b)

    def PrintString(self):
        print("a", self.a, "r", self.r, "g", self.g, "b", self.b)