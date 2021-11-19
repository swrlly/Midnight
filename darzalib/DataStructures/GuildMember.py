from .IDataStructure import IDataStructure

class GuildMember(IDataStructure):

    def __init__(self, name, rank):
        self.name = name
        self.guildRank = rank

    def Read(self, r):
        self.name = r.ReadString8()
        self.guildRank = r.ReadByte()

    def Write(self, w):
        w.WriteString8(self.name)
        w.WriteByte(self.guildRank)

    def PrintString(self):
        super().PrintString()