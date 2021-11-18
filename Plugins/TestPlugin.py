from .PluginInterface import PluginInterface
from ClientConnection import ClientConnection
from darzalib.PacketUtil import *

class TestPlugin(PluginInterface):

	"""
	for each plugin, you need to instantiate three class variables: hooks, load, defaultState
	Make sure hooks is a set data structure (for O(1) access as we check for containment when checking for hooks).
	hooks will tell the program what packets you intend to hook (meaning what packets you want to look at as they pass by)
	why? suppose you have 10 plugins that utilize NewTick. You don't want to reread
	newtick 10 times. Also, you only want to call the plugins which contain a newtick
	hook. Remember, the faster this proxy is, the faster it can route packets.
	"""

	hooks = {GmPacketTypes.Hello}

	"""
	also, make sure you put this class variable to tell the PluginManager whether to load this plugin or not. If this is absent,
	the manager will throw an exception.
	"""
	load = True

	"""
	lastly, declare and initialize a variable called defaultState. This variable will tell the PluginManager to turn the plugin on or off after loading this plugin
	"""
	defaultState = True

	# Note: you should probably inherit from PluginInterface as these variables are already declared

	"""
	Next, you need to write functions that will handle each packet type in your hooks.
	Make sure your function name is on + the capitalization found in PacketTypes.py, otherwise your function will not be called.
	This is all you need to write. Here is an example for the packet type `Hello`
	def onHello(self, clientConnection: ClientConnection, packet: Hello, send: bool) -> (Hello, bool):
		clientConnection is an instance of ClientConnection
		packet is an instance of the specific packet type your function will handle. 
		send is whether or not this packet will be sent
		returns: (updated packet, send)
			send = true if you wish to send the packet, else false	
	Below is an example of this handler
	"""

	def onHello(self, clientConnection: ClientConnection, packet: Hello, send: bool) -> (Hello, bool):
		color = GameColor(255, 48, 187, 255)
		clientConnection.CreateNotification(color, b"Welcome to Midnight!") 
		return (packet, send)

	def getAuthor(self):
		return "swrlly - https://github.com/swrlly"