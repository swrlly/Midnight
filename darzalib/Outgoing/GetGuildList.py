from ..IPacket import IPacket

class GetGuildList(IPacket):
    
    "Sent by client to get list of guilds?"

    def __init__(self):
        pass
        
    def Read(self, r):
        pass

    def Write(self, w):
        pass
        
    def GetType(self):
        return super().GetType()

    def PrintString(self):
        super().PrintString()
