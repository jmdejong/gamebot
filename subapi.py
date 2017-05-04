


import subprocess as sp
from threading import Thread

class SubApi:
    
    def __init__(self):
        self.outputListeners = set()
    
    
    def start(self, args, listenDaemon=True):
        self.program = sp.Popen(args, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True)
        
        self.t = Thread(target=self.listen, daemon=listenDaemon)
        self.t.start()
    
    
    def listen(self):
        while self.program.stdout.readable():
            outputLine = self.program.stdout.readline()[:-1]
            for listener in self.outputListeners:
                listener(outputLine)
    
    def sendInput(self, command):
        self.program.stdin.write(command+"\n")
        self.program.stdin.flush()
    
    def stop(self):
        self.program.terminate()
        self.program.stdout.close()


    
