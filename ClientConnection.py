import socket
import struct
import select
import random
import time
import json
import traceback
import math
import re
import glob

from PluginManager import *
from darzalib.PacketUtil import *

import logging

class ClientConnection:

    def __init__(self, pm: PluginManager, projDict, aoeDict, itemDict):

        self.debug = False
        self.firstUpdate = False

        # some parameters used throught the game
        self.remoteHostAddr = "3.80.30.35"#"18.197.125.211"#"54.219.230.109"
        self.remoteHostPort = 6410
        # variables we use to keep track of client's state
        self.reconnecting = False
        self.connected = False
        self.gameSocket = None
        self.serverSocket = None
        self.killSignal = False
        self.nextX = 0
        self.nextY = 0
        self.objectID = -1
        self.pluginManager = pm
        self.clientPacketHooks = {}
        self.projDict = projDict
        self.aoeDict = aoeDict
        self.itemDict = itemDict

        # stuff to ignore when debugging
        self.ignoreIn = [GmPacketTypes.HealthUpdate, GmPacketTypes.Aoe, GmPacketTypes.ChallengeUpdated, GmPacketTypes.Chats, GmPacketTypes.Projectiles, GmPacketTypes.CheckPingAck, GmPacketTypes.Ping, GmPacketTypes.Update, GmPacketTypes.Tiles]#[GmPacketTypes.Chats, GmPacketTypes.HealthUpdate, GmPacketTypes.Projectiles, GmPacketTypes.Tiles, GmPacketTypes.Update, GmPacketTypes.CheckPingAck, GmPacketTypes.Ping]
        self.ignoreOut = [GmPacketTypes.Shoot, GmPacketTypes.Hit, GmPacketTypes.CheckPing, GmPacketTypes.ProjectilesAck, GmPacketTypes.Move, GmPacketTypes.UpdateAck, GmPacketTypes.Pong]#[GmPacketTypes.UpdateAck, GmPacketTypes.StartUpdate]#[GmPacketTypes.ProjectilesAck, GmPacketTypes.UpdateAck, GmPacketTypes.Move, GmPacketTypes.CheckPing, GmPacketTypes.Pong]
        self.printOut = [GmPacketTypes.Hello, GmPacketTypes.Create, GmPacketTypes.Load]
        self.printIn = [GmPacketTypes.ChallengeUpdated, GmPacketTypes.Reconnect, GmPacketTypes.Chats, GmPacketTypes.CreateResp, GmPacketTypes.MapInfo]
        self.logger = logging.getLogger("Client")

    def InitializePacketHooks(self) -> bool:
        """
        Make dictionaries of {GmPacketType: function to call}
        """

        # parse outgoing
        for name in glob.glob("darzalib/Outgoing/*[A-z].py"):
            tok = re.split("\\\\|/", name)[-1][:-3]
            try:
                self.clientPacketHooks.update({getattr(GmPacketTypes, tok) : getattr(self, "On" + tok)})
            except:
                self.logger.info("Failed to initialize packet hook for {}".format(tok))

        return True

    # disconnect the client from the proxy
    # disconnect the proxy from the server
    def Disconnect(self):
        self.connected = False
        if self.serverSocket:
            self.serverSocket.shutdown(socket.SHUT_RDWR)
            self.serverSocket.close()
        if self.gameSocket:
            self.gameSocket.shutdown(socket.SHUT_RDWR)
            self.gameSocket.close()
        self.gameSocket = None
        self.serverSocket = None

    def Reconnect(self):
        self.ConnectRemote()
        self.connected = True
        self.reconnecting = False

    # Connect to remote host. Block until client connected
    def ConnectRemote(self):
        while self.gameSocket == None:
            if self.killSignal: return
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.connect((self.remoteHostAddr, self.remoteHostPort))

    # closes both sockets
    def Close(self):
        self.gameSocket.close()
        self.serverSocket.close()

    # restart entire connection
    def Reset(self):

        # fix this later :skull:
        self.Disconnect()
        self.Reconnect()

    """
    Listens to one packet from the client.
    """
    def ListenToClient(self):

        # buffer for packet body
        data = bytearray()
        # buffer for packet header
        header = self.gameSocket.recv(5)
        leftToRead = 5 - len(header)
        
        # if server sent nothing, just return
        if len(header) == 0 or self.reconnecting:
            self.Reset()
            return
        
        # if server was not ready to send 5 bytes
        while leftToRead > 0:
            header += self.gameSocket.recv(leftToRead)
            leftToRead -= len(header)

        if header[0] == 4 and header[1] == 1:
            rest = self.gameSocket.recv(10)
            header = header + rest
            self.gameSocket.send(bytearray([4, 90, *header[2:8]]))
            return

        packetID = header[4]
        # packet length in little endian format, subtract 1 since header counts in length
        expectedPacketLength = struct.unpack("<i", header[:4])[0] - 1
        
        # read packet body
        while expectedPacketLength > 0: 
            buf = bytearray(self.gameSocket.recv(expectedPacketLength))
            data += buf
            expectedPacketLength -= len(buf)

        self.ProcessClientPacket(packetID, header, data)

    def ProcessClientPacket(self, packetID: int, header: bytearray, data: bytearray) -> bool:
        """
        Given header + raw packet body from the client, process it into proper packet class.
        """

        p = None
        send = True
        reassembledPacket = None

        # given packetID + data, return the processed packet
        try:
            p = ProcessPacket(packetID, data, False)
        except:
            pass
        
        if self.debug:
            try:
                if packetID not in self.ignoreOut:
                    self.logger.info("Client sent: " + GmPacketTypes.reverseDict[packetID])
                    if packetID == GmPacketTypes.EnterPortal:
                        self.logger.info(data)
                    if packetID in self.printOut:
                        p.PrintString()
            except Exception as e:
                self.logger.info(e)
                self.logger.info("Got unknown packet from client, id {}".format(packetID))

        # hook packets
        # will fail if a hook is not implemented but packetType is present
        if packetID in self.clientPacketHooks and p is not None:
            p, send = self.RoutePacket(p, send, self.clientPacketHooks[packetID])
        reassembledPacket = WritePacket(p) if p != None else WritePacketRaw(header, data)
        if send: self.SendPacketToServer(reassembledPacket)
        return True

    """
    Listens to one packet from the server.
    """
    def ListenToServer(self):

        # buffer for packet body
        data = bytearray()
        # buffer for packet header
        header = self.serverSocket.recv(5)
        leftToRead = 5 - len(header)
        
        # if server sent nothing, just return
        if len(header) == 0 or self.reconnecting:
            self.Reset()
            return
        
        # if server was not ready to send 5 bytes
        while leftToRead > 0:
            header += self.serverSocket.recv(leftToRead)
            leftToRead -= len(header)

        packetID = header[4]
        # packet length in little endian format, subtract 1 since header counts in length
        expectedPacketLength = struct.unpack("<i", header[:4])[0] - 1
        
        # read packet body
        while (expectedPacketLength > 0): 
            buf = bytearray(self.serverSocket.recv(expectedPacketLength))
            data += buf
            expectedPacketLength -= len(buf)

        self.ProcessServerPacket(packetID, header, data)

    def ProcessServerPacket(self, packetID: int, header: bytearray, data: bytearray):
        """
        Given header + raw packet body from the server, process it into proper packet class.
        """

        p = None
        send = True
        reassembledPacket = None
        
        # given packetID + data, return the corresponding packet type, already read.
        try:
            p = ProcessPacket(packetID, data, False)
        except Exception as e:
            self.logger.info(data)
            traceback.print_exc()
        if self.debug:
            try:
                if packetID not in self.ignoreIn:
                    self.logger.info("Server sent: " + GmPacketTypes.reverseDict[packetID])
                    if packetID in self.printIn:
                        p.PrintString()
            except:
                traceback.print_exc()
                self.logger.info("Got unknown packet from server, id {}".format(packetID))

        #########################
        ######### Hooks #########
        #########################

        if packetID == GmPacketTypes.Update:
            p, send = self.RoutePacket(p, send, self.OnUpdate)

        if packetID == GmPacketTypes.MapInfo:
            p, send = self.RoutePacket(p, send, self.OnMapInfo)

        if packetID == GmPacketTypes.Reconnect:
            p, send = self.RoutePacket(p, send, self.OnReconnect)

        if packetID == GmPacketTypes.Projectiles:
            p, send = self.RoutePacket(p, send, self.OnProjectiles)

        if packetID == GmPacketTypes.MapInfo:
            p, send = self.RoutePacket(p, send, self.OnMapInfo)

        if packetID == GmPacketTypes.HealthUpdate:
            p, send = self.RoutePacket(p, send, self.OnHealthUpdate)

        if packetID == GmPacketTypes.Failure:
            self.Reset()

        reassembledPacket = WritePacket(p) if p != None else WritePacketRaw(header, data)
        if send: self.SendPacketToClient(reassembledPacket)
        return True

    """
    Given a specific packet type, call the relevant clientConnection onPacketType function to read the packet
    Then, iterate through hook dict to call plugins which hook this packet.

    :param p: A processed packet object
    :param send: whether or not to send the packet
    :param onPacketType: The implemented callback inside a plugin when this packet type is encountered.
        This function will be defined within the Client class.

    returns: (PacketClass, send)
    """
    def RoutePacket(self, p, send, onPacketType):

        p, send = onPacketType(p, send)

        # if this certain packet has a hook present (meaning it's used by some plugin)
        if p.GetType() in self.pluginManager.hooks:

            # then we search for the plugin, and whether if it's active or not.
            for plugin in self.pluginManager.hooks[p.GetType()]:
                # if the plugin is active
                if self.pluginManager.plugins[plugin]:
                    # at each step, we are editing the packet on the wire
                    # important: make sure you're spelling your class methods correctly.
                    p, send = getattr(plugin, "On" + type(p).__name__)(self, p, send)

        return p, send

    """
    Starts to listen for packets
    """
    def Listen(self):

        while True:
            try:

                ready = select.select([self.gameSocket, self.serverSocket], [], [])[0]

                if self.reconnecting:
                    self.Reset()
                    continue
  
                # client has data ready to send to server
                if self.gameSocket in ready:
                    self.ListenToClient()
                # server has data ready to send to client
                if self.serverSocket in ready:
                    self.ListenToServer()

                for plugin in self.pluginManager.plugins:
                    try: getattr(plugin, "Main")(self)
                    except AttributeError: pass

            except ConnectionAbortedError as e:
                self.logger.info("Connection was aborted")
                self.Reset()

            except ConnectionResetError as e:
                self.logger.info("Connection was reset")
                self.remoteHostAddr = "3.80.30.35"
                self.remoteHostPort = 6410
                self.Reset()

            except KeyboardInterrupt:
                self.logger.info("User aborted. Shutting down proxy.")
                self.connected = False
                self.killSignal = True
                self.Reset()
                return

            except OSError as e:
                traceback.print_exc()
                self.logger.info("Restarting proxy...")	
                self.Reset()

            except Exception as e:
                self.logger.info("General catchall.")
                traceback.print_exc()
                self.remoteHostAddr = "3.80.30.35"
                self.remoteHostPort = 6410
                self.Reset()


    # server -> client
    def SendPacketToClient(self, p):
        try: self.gameSocket.sendall(p)
        except Exception: raise Exception("Error when sending packet")

    # client -> server
    def SendPacketToServer(self, p):
        try: self.serverSocket.sendall(p)
        except Exception: raise Exception("Error when sending packet")


################################################
##### packet hooks and extra functionality #####
################################################

def extends(k):
    def decorator(func):
        setattr(k, func.__name__, func)
        return func
    return decorator

@extends(ClientConnection)
def OnReconnect(self, p: Reconnect, send: bool) -> (Reconnect, bool):
    self.reconnecting = True
    self.remoteHostAddr = p.host
    self.remoteHostPort = p.port
    p.host = "127.0.0.1"
    p.port = 6410
    return p, send

@extends(ClientConnection)
def OnHealthUpdate(self, p: HealthUpdate, send: bool) -> (HealthUpdate, bool):
    return p, send

@extends(ClientConnection)
def OnProjectiles(self, p: Projectiles, send: bool) -> (Projectiles, bool):
    return p, send

@extends(ClientConnection)
def OnActivateObject(self, p: ActivateObject, send: bool) -> (ActivateObject, bool):
    return p, send

@extends(ClientConnection)
def OnAllyHit(self, p: AllyHit, send: bool) -> (AllyHit, bool):
    return p, send

@extends(ClientConnection)
def OnChat(self, p: Chat, send: bool) -> (Chat, bool):
    return p, send

@extends(ClientConnection)
def OnCheckPing(self, p: CheckPing, send: bool) -> (CheckPing, bool):
    return p, send

@extends(ClientConnection)
def OnCreate(self, p: Create, send: bool) -> (Create, bool):
    return p, send

@extends(ClientConnection)
def OnEditEssence(self, p: EditEssence, send: bool) -> (EditEssence, bool):
    return p, send

@extends(ClientConnection)
def OnEscape(self, p: Escape, send: bool) -> (Escape, bool):
    return p, send

@extends(ClientConnection)
def OnExchangeEssence(self, p: ExchangeEssence, send: bool) -> (ExchangeEssence, bool):
    return p, send

@extends(ClientConnection)
def OnExchangeGift(self, p: ExchangeGift, send: bool) -> (ExchangeGift, bool):
    return p, send

@extends(ClientConnection)
def OnGetGuildList(self, p: GetGuildList, send: bool) -> (GetGuildList, bool):
    return p, send

@extends(ClientConnection)
def OnGotoResp(self, p: GotoResp, send: bool) -> (GotoResp, bool):
    return p, send

@extends(ClientConnection)
def OnHello(self, p: Hello, send: bool) -> (Hello, bool):
    return p, send

@extends(ClientConnection)
def OnHit(self, p: Hit, send: bool) -> (Hit, bool):
    return p, send

@extends(ClientConnection)
def OnLoad(self, p: Load, send: bool) -> (Load, bool):
    return p, send

@extends(ClientConnection)
def OnMapInfoAck(self, p: MapInfoAck, send: bool) -> (MapInfoAck, bool):
    return p, send

@extends(ClientConnection)
def OnMapInfo(self, p: MapInfo, send: bool) -> (MapInfo, bool):
    self.firstUpdate = False
    self.objectID = p.playerID
    return p, send

@extends(ClientConnection)
def OnMessage(self, p: Message, send: bool) -> (Message, bool):
    return p, send

@extends(ClientConnection)
def OnMove(self, p: Move, send: bool) -> (Move, bool):
    self.nextX = p.position.x
    self.nextY = p.position.y
    return p, send

@extends(ClientConnection)
def OnPong(self, p: Pong, send: bool) -> (Pong, bool):
    return p, send

@extends(ClientConnection)
def OnProjectilesAck(self, p: ProjectilesAck, send: bool) -> (ProjectilesAck, bool):
    return p, send

@extends(ClientConnection)
def OnShoot(self, p: Shoot, send: bool) -> (Shoot, bool):
    return p, send

@extends(ClientConnection)
def OnStartUpdate(self, p: StartUpdate, send: bool) -> (StartUpdate, bool):
    return p, send

@extends(ClientConnection)
def OnSwap(self, p: Swap, send: bool) -> (Swap, bool):
    return p, send

@extends(ClientConnection)
def OnUpdate(self, p: Update, send: bool) -> (Update, bool):
    for obj in p.objectStats:
        if obj.objectID == self.objectID:
            for stat in obj.stats:
                if stat.statType == 75:
                    self.currentX = stat.value.x
                    self.currentY = stat.value.y

    return p, send

@extends(ClientConnection)
def OnUpdateAck(self, p: UpdateAck, send: bool) -> (UpdateAck, bool):
    return p, send

@extends(ClientConnection)
def OnUseItem(self, p: UseItem, send: bool) -> (UseItem, bool):
    return p, send

@extends(ClientConnection)
def CreateNotification(self, color, text):
    c = Chats()
    chatItem = ChatItem(color, -1, text)
    c.chats.append(chatItem)
    self.SendPacketToClient(WritePacket(c))