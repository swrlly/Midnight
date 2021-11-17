from .PacketBodyReader import PacketBodyReader
from .PacketBodyWriter import PacketBodyWriter
from .GmPacketTypes import GmPacketTypes
from .DataStructures.__init__ import *
from .Outgoing.__init__ import *
from .Incoming.__init__ import *

from .Packet import Packet

def WritePacketRaw(header, data):
    """
    Given two raw bytearrays, return a bytearray representing the entire packet
    """
    return header + data

def WritePacket(packet):
    """
    Given a specific packet class + id, return a bytearray representing the entire packet
    """
    w = PacketBodyWriter()

    # write body of packet
    packet.Write(w)
    w.WriteHeader(packet.GetType())
    return w.buffer

def ProcessPacket(id : int, data : bytearray):
    """
    Given a packet ID + the body of a packet, return the corresponding processed packet type.

    Args:
        id (int): an integer representing the packet ID
        data (bytearray): a bytearray representing the body of a packet.

    Returns:
        The corresponding processed packet class.
    """

    # initialize a reader for the packet
    reader = PacketBodyReader(data)
    p = None

    if id in GmPacketTypes.reverseDict:
        try:
            p = eval(GmPacketTypes.reverseDict[id])()
        except Exception as e:
            return
            print("Packet type \'" + GmPacketTypes.reverseDict[id] + "\' has not been implemented")
            print(e)
            raise Exception(e)
    else:
        raise Exception("New packet detected")

    # read the body
    p.Read(reader)
    return p

