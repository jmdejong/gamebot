#!/usr/bin/env python3

import socket
import threading
import os.path


class AdminClient:
	
	def __init__(self):
		self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	
	def start(self, address):
		self.sock.connect(address)
		threading.Thread(target=self.listen, daemon=True).start()
		
		while True:
			command = input()
			self.sock.sendall(bytes(command, "utf-8"))
	
	def listen(self):
		while True:
			data = self.sock.recv(2048)
			print(str(data, "utf-8"))

def main():
	address = os.path.join(os.path.dirname(__file__), "adminsocket.sock")
	AdminClient().start(address)
	


if __name__ == "__main__":
	main()
