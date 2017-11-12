
import sys
import socket
import threading
import os
import time

MESSAGE_SIZE = 4096

class Server:
    
    
    def __init__(self, onConnection=(lambda *_:None), onMessage=(lambda *_:None), onConnectionClose=(lambda *_:None)):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.onConnection = onConnection
        self.onMessage = onMessage
        self.onConnectionClose = onConnectionClose
        self.connections = set()
        self.closed = False
    
    
    def start(self, address):
        
        try:
            os.unlink(address)
        except FileNotFoundError:
            if os.path.exists(address):
                raise
        try:
            
            self.sock.bind(address)
            os.chmod(address, 0o600)
        except PermissionError:
            print("You don't have permission to use this socket file.\nRun the server with the '-s' option to specify another socket file path.\nWARNING: if an existing file is given, it will be overwritten.")
            sys.exit(-1)
        except OSError:
            print("Unable to create a socket file.\nMost likely this means that a server is already running and using the socket file, or the execution of this program didn't clean up well.\nIf no other server is running, try removing "+address+".\nIf you can't specify another socket file with the -s option (and tell all players to connect to that)")
            sys.exit(-1)
        
        self.sock.listen()
        
        self.listener = threading.Thread(target=self._listen, name="uds main server thread "+time.asctime(), daemon=True)
        self.listener.start()
    
    
    def _listen(self):
        while not self.closed:
            connection, client_address = self.sock.accept()
            listener = threading.Thread(target=self._listenCon, args=(connection,), name="uds server thread "+time.asctime(), daemon=True)
            listener.start()
    
    def _listenCon(self, connection):
        #print(connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED))
        self.connections.add(connection)
        self.onConnection(connection)
        buff = ""
        data = connection.recv(MESSAGE_SIZE)
        while data:
            self.onMessage(connection, str(data, encoding="utf-8"))
            try:
                data = connection.recv(MESSAGE_SIZE)
            except socket.error:
                break
            if not len(data):
                break
        self.connections.discard(connection)
        self.onConnectionClose(connection)
        connection.close()
    
    
    
    def send(self, connection, msg):
        try:
            connection.send(msg.encode("utf-8"))
        except:
            self.connections.discard(connection)
            self.onConnectionClose(connection)
            print("failed to send to client")
    
    def broadcast(self, msg):
        for connection in frozenset(self.connections):
            self.send(connection, msg)
    
    def close(self):
        self.closed = True
        for connection in self.connections:
            self.onConnectionClose(connection)
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        print("socket closed")

