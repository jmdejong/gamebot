
from subbot import SubBot
import shlex
import json
import importlib
import socket
import threading
import udsserver
import traceback
import os

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
            
            elif task == "log":
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
                self.loadmodule(name)
                self.log("reloaded python module "+name)
            
            elif task == "load":
                name = argv[1]
                module = self.loadmodule(name)
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
                
                self.loadmodule("ircsender")
                module = self.loadmodule("gamebot")
                gamebot = module.GameBot(oldcore.client, oldcore.chanlist)
                #gamebot.sender = self.loadmodule("ircsender").IrcSender()
                
                gamebot.on_welcome(self.bot.connection, None)
                for name, subbot in oldcore.subbots.items():
                    gamebot.add_subbot(subbot, name)
                oldcore.stop()
                self.log("gamebot core reloaded")
            
            elif task == "threads":
                for thread in threading.enumerate():
                    self.log(thread.name)
            
            
            elif task == "closesockets":
                for thread in threading.enumerate():
                    if thread._target and thread._target.__self__ and thread._target.__self__.sock:
                        try:
                            thread._target.__self__.sock.shutdown(socket.SHUT_RDWR)
                            self.log("shut down a socket")
                        except Exception:
                            print("failed to shut down socket")
                        self.log(thread._target.__self__.sock)
            
            elif task == "topic":
                channel = argv[1]
                topic = argv[2]
                self.bot.connection.topic(channel, topic)
                self.log("set topic for {} to {}".format(channel, topic))
            
            elif task == "mode":
                channel = argv[1]
                command = argv[2]
                self.bot.connection.mode(channel, command)
                self.log("changed mode for {} to {}".format(channel, command))
            
            elif task == "sendraw":
                command = argv[1]
                self.bot.connection.send_raw(command)
                self.log("sent raw command {}".format(command))
            
            elif task == "pid":
                self.log(os.getpid())
                
                
            elif task == "me":
                chan = argv[1]
                status = argv[2]
                self.bot.connection.action(chan, status)
            
            else:
                self.log("unknown command "+str(task))
        
        except Exception as err:
            self.log(traceback.format_exc)
            self.log(err)
    
    def stop(self):
        self.log("closing socket server. If the client does not stop/crash then restart it manually")
        self.server.close()
    
    def say(self, chan, text):
        self.reply(chan, text)
    
    def log(self, text):
        self.server.broadcast(str(text)+"\n")
        print(text)
        
    def loadmodule(self, modulename):
        importlib.invalidate_caches()
        module = importlib.import_module(modulename)
        module = importlib.reload(module)
        return module
    


BotModule = UdsAdmin
        
