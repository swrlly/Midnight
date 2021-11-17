import struct

class PacketBodyReader:

	def __init__(self, data):
		# start from the beginning of the body, always assume no headers if you're starting to read
		self.index = 0
		self.buffer = data

	def BytesLeft(self):
		return len(self.buffer) - self.index

	def ReadByte(self):
		self.index += 1
		return self.buffer[self.index - 1]

	def ReadFloat(self):
		tmp = struct.unpack("<f", self.buffer[self.index : self.index + 4])[0]
		self.index += 4
		return tmp

	def ReadDouble(self):
		tmp = struct.unpack("<d", self.buffer[self.index : self.index + 4])[0]
		self.index += 4
		return tmp

	def ReadInt16(self):
		tmp = struct.unpack("<h", self.buffer[self.index : self.index + 2])[0]
		self.index += 2
		return tmp

	def ReadUInt16(self):
		tmp = struct.unpack("<H", self.buffer[self.index : self.index + 2])[0]
		self.index += 2
		return tmp

	def ReadInt32(self):
		tmp = struct.unpack("<i", self.buffer[self.index : self.index + 4])[0]
		self.index += 4
		return tmp

	def ReadUInt32(self):
		tmp = struct.unpack("<I", self.buffer[self.index : self.index + 4])[0]
		self.index += 4
		return tmp

	def ReadInt64(self):
		tmp = struct.unpack("<q", self.buffer[self.index : self.index + 8])[0]
		self.index += 8
		return tmp

	def ReadUInt64(self):
		tmp = struct.unpack("<Q", self.buffer[self.index : self.index + 8])[0]
		self.index += 8
		return tmp
		
	def ReadBoolean(self):
		tmp = struct.unpack("<?", self.buffer[self.index : self.index + 1])[0]
		self.index += 1
		return tmp

	def ReadString8(self):
		"""
		length: 8 bit unsigned integer
		"""
		length = self.ReadByte()
		return self.ReadStringBytes(length)

	def ReadString16(self):
		length = self.ReadUInt16()
		return self.ReadStringBytes(length)

	def ReadString32(self):
		length = self.ReadUInt32()
		return self.ReadStringBytes(length)

	def ReadStringBytes(self, length):
		tmp = struct.unpack("<{}s".format(length), self.buffer[self.index : self.index + length])[0].decode()
		self.index += length
		return tmp
