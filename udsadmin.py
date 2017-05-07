
from subbot import SubBot
import shlex
import json
import importlib
import socket
import threading
import udsserver

class UdsAdmin(SubBot):
    
    name = "udsadmin"
    
    description = "Perform administrative tasks though an unix domain socket without restarting the bot"
    minargs = 16
    socketfile = "./adminsocket.sock"
    
    def __init__(self):
        self.server = udsserver.Server(onMessage=self.on_uds_message)
        self.server.start(self.socketfile)
    
    def on_uds_message(self, _connection, text):
        try:
            argv = shlex.split(text)
            # ensure argv[0] and argv[1] etc. don't error
            while len(argv) < self.minargs:
                argv.append(None)
            
            task = argv[0]
            
            
            if task == "say":
                self.say(argv[1], argv[2])
            
            elif task == "print":
                print(argv[1])
            
            elif task == "echo":
                self.server.broadcast(argv[1]+"\n")
            
            elif task == "info":
                self.log(argv[1])
            
            elif task == "join":
                channel = argv[1]
                self.bot.connection.join(channel)
                self.log("joined " + channel)
            
            elif task == "leave":
                channel = argv[1]
                self.bot.connection.part([channel])
                self.log("left " + channel)
            
            elif task == "loadcode":
                name = argv[1]
                self.loadmodule()
                self.log("reloaded python module "+name)
            
            elif task == "load":
                name = argv[1]
                module = self.loadmodule()
                subbot = module.BotModule()
                if name in self.bot.subbots:
                    self.bot.remove_subbot(name)
                self.bot.add_subbot(subbot, name)
                self.log("loaded subbot "+name)
            
            elif task == "stop":
                name = argv[1]
                self.bot.remove_subbot(name)
                self.log("stopped subbot "+name)
            
            elif task == "reloadcore":
                oldcore = self.bot
                
                module = self.loadmodule("gamebot")
                gamebot = module.GameBot(oldcore.client, oldcore.chanlist)
                
                gamebot.on_welcome(self.bot.connection, None)
                for name, subbot in oldcore.subbots.items():
                    gamebot.add_subbot(subbot, name)
                oldcore.stop()
                self.log("gamebot core reloaded")
            
            else:
                self.log("unknown command "+task)
        
        except Exception as err:
            self.log(err)
            raise
    
    def stop(self):
        self.server.close()
    
    def say(self, chan, text):
        self.reply(chan, text)
    
    def log(self, text):
        self.server.broadcast(text+"\n")
        print(text)
        
    def loadmodule(self, modulename):
        importlib.invalidate_caches()
        module = importlib.import_module(modulename)
        module = importlib.reload(module)
        return module
    


BotModule = UdsAdmin
        
