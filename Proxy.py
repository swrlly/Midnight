import threading
import logging

from multiprocessing import Process
from ClientConnection import *
from Logger import CreateLogger

class Proxy:

    def __init__(self, clientConnection: ClientConnection):

        self.localHostAddr = "127.0.0.1"
        self.localHostPort = 6410
        self.managerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientConnection = clientConnection
        self.serverMonitorThread = None
        self.logger = logging.getLogger("Proxy")

    def ServerMonitor(self):
        """
        Look for clients connecting to localhost.
        """
        self.managerSocket.bind((self.localHostAddr, self.localHostPort))
        self.managerSocket.listen(2)
        # always listening for client connect
        while True:
            self.clientConnection.gameSocket, addr = self.managerSocket.accept()
            self.logger.info("Client connected.")

    def StartProxy(self):
        """
        Start proxy running as a daemon thread.
        """
        self.serverMonitorThread = threading.Thread(target = self.ServerMonitor, daemon = True)
        self.serverMonitorThread.start()
        
def main():

    CreateLogger("logs")
    logger = logging.getLogger("Main")

    logger.info("[Initializer]: Loading plugins...")
    plugins = PluginManager()
    if not plugins.initialize():
        logger.info("Shutting down.")
        return

    clientConnection = ClientConnection(plugins)
    logger.info("[Initializer]: Loading packet hooks...")
    if not clientConnection.InitializePacketHooks():
        logger.info("Unable to initialize packet hooks. Shutting down")
        return
    proxy = Proxy(clientConnection)

    proxy.StartProxy()
    logger.info("[Initializer]: Started proxy.")
    clientConnection.ConnectRemote()
    clientConnection.Listen()
    

if __name__ == "__main__":
    main()