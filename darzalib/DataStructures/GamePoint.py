from .IDataStructure import IDataStructure

class GamePoint(IDataStructure):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def Read(self, r):
        self.x = r.ReadFloat()
        self.y = r.ReadFloat()

    def Write(self, w):
        w.WriteFloat(self.x)
        w.WriteFloat(self.y)

    def PrintString(self):
        super().PrintString()