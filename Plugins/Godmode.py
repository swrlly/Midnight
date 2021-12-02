from .PluginInterface import PluginInterface
from ClientConnection import ClientConnection
from darzalib.PacketUtil import *

import re

class Godmode(PluginInterface):

    hooks = {GmPacketTypes.Chat, GmPacketTypes.Move}
    load = True
    defaultState = True
    on = False

    def getAuthor(self):
        return "swrlly - https://github.com/swrlly"

    def OnMove(self, clientConnection: ClientConnection, packet: Move, send: bool) -> (Move, bool):
        
        if self.on: packet.time += 2000
        return packet, send

    def OnChat(self, clientConnection: ClientConnection, packet: Chat, send: bool) -> (Chat, bool):
        
        if len(packet.text) > 0:
            if packet.text[0] == '/':

                toks = re.split("\s+", packet.text)

                if toks[0] == '/gm':
                    self.on = not self.on
                    clientConnection.CreateNotification(GameColor(255, 48, 187, 255), 'Godmode: {}'.format("ON" if self.on else "OFF"))
                    send = False
        return packet, send




