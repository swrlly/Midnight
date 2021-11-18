import struct

class PacketBodyWriter:

    def __init__(self):
        self.buffer = bytearray()

    def WriteByte(self, data):
        self.buffer += struct.pack("<B", data)

    def WriteInt16(self, data):
        self.buffer += struct.pack("<h", data)

    def WriteUInt16(self, data):
        self.buffer += struct.pack("<H", data)

    def WriteInt32(self, data):
        self.buffer += struct.pack("<i", data)

    def WriteInt64(self, data):
        self.buffer += struct.pack("<q", data)

    def WriteUInt32(self, data):
        self.buffer += struct.pack("<I", data)

    def WriteBoolean(self, data):
        self.buffer += struct.pack("<?", data)

    def WriteFloat(self, data):
        self.buffer += struct.pack("<f", data)

    def WriteString8(self, data: str):
        self.WriteByte(len(data))
        self.buffer += struct.pack("<{}s".format(len(data)), data.encode('utf-8'))

    def WriteString16(self, data: str):
        self.WriteShort(len(data))
        self.buffer += struct.pack("<{}s".format(len(data)), data.encode('utf-8'))

    def WriteString32(self, data: str):
        self.WriteInt32(len(data))
        self.buffer += struct.pack("<{}s".format(len(data)), data.encode('utf-8'))

    def WriteStringBytes(self, data: bytearray):
        self.buffer += struct.pack("<{}s".format(len(data)), data)

    def WriteHeader(self, id):
        self.buffer = bytearray(struct.pack("<i", len(self.buffer) + 1)) + self.buffer
        self.buffer.insert(4, id)
