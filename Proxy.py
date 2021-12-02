import threading

from multiprocessing import Process
from ClientConnection import *

class Proxy:

    def __init__(self, clientConnection: ClientConnection):

        self.localHostAddr = "127.0.0.1"
        self.localHostPort = 6410
        self.managerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientConnection = clientConnection
        self.serverMonitorThread = None

    def ServerMonitor(self):
        """
        Look for clients connecting to localhost.
        """
        self.managerSocket.bind((self.localHostAddr, self.localHostPort))
        self.managerSocket.listen(2)
        # always listening for client connect
        while True:
            self.clientConnection.gameSocket, addr = self.managerSocket.accept()
            print("Client connected.")

    def StartProxy(self):
        """
        Start proxy running as a daemon thread.
        """
        self.serverMonitorThread = threading.Thread(target = self.ServerMonitor, daemon = True)
        self.serverMonitorThread.start()
        
def main():

    print("[Initializer]: Loading plugins...")
    plugins = PluginManager()
    if not plugins.initialize():
        print("Shutting down.")
        return

    clientConnection = ClientConnection(plugins)
    print("[Initializer]: Loading packet hooks...")
    if not clientConnection.InitializePacketHooks():
        print("Unable to initialize packet hooks. Shutting down")
        return
    proxy = Proxy(clientConnection)

    
    proxy.StartProxy()
    print("[Initializer]: Started proxy.")
    clientConnection.ConnectRemote()
    clientConnection.Listen()
    

if __name__ == "__main__":
    main()