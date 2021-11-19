from .GmPacketTypes import GmPacketTypes
from .DataStructures.__init__ import *

class IPacket:

    def __init__(self):
        pass

    def Read(self, r):
        pass

    def Write(self, w):
        pass

    def GetType(self):
        return getattr(GmPacketTypes, type(self).__name__)
    
    def PrintString(self):
        itr = vars(self).items()
        baseTypes = set([str, float, int, list, bool])
        print(" ".join([k + " {}".format(v) for k, v in itr if type(v) in baseTypes]))
        for k, v in itr:
            if type(v) not in baseTypes: v.PrintString()