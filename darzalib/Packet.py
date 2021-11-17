from .GmPacketTypes import GmPacketTypes

class Packet:

    def __init__(self):
        pass

    def Read(self, r):
        pass

    def Write(self, w):
        pass

    def GetType(self):
        return getattr(GmPacketTypes, type(self).__name__)
    
    def PrintString(self):
        print(" ".join([k + " {}".format(v) for k, v in vars(self).items()]))