

import time
import sys
import json
import importlib
import queue
import threading
import ircsender


class GameBot:
    
    
    def __init__(self, client, name, address="localhost", port=6667, channels=[]):
        
        self.handlers = {
            "welcome": self.on_welcome,
            "join": self.on_join,
            "privmsg": self.on_privmsg,
            "pubmsg": self.on_pubmsg
        }
        
        self.name = name
        self.address = address
        self.port = port
        
        self.chanlist = channels
        self.lastMsg = time.time()
        
        self.sender = ircsender.IrcSender()
        
        self.subbots = {}
        self.commands = {}
        self.active_channels = set()
        self.connection = None
        self.client = client
        for eventname, handler in self.handlers.items():
            client.add_global_handler(eventname, handler)
    
    
    def connect(self):
        self.client.server().connect(self.address, self.port, self.name)
    
    def process(self):
        self.client.process_forever(2)
    
    def disconnect(self, message="Bye all"):
        self.client.disconnect_all(message)
    
    def load_module(self, name):
        try:
            importlib.invalidate_caches()
            module = importlib.import_module(modulename)
            module = importlib.reload(module)
        except Exception as err:
            print("Failed to load module '{}': {}".format(name, err))
    
    def load_subbot(self, modulename):
        try:
            module = self.load_module(modulename)
            subbot = module.BotModule()
            self.add_subbot(subbot, modulename)
            print("succesfully loaded subbot {}".format(modulename))
        except Exception as err:
            print("loading {} failed: {}".format(modulename, err))
        
    
    # add a running subbot to the bot. Return whether succesfull
    def add_subbot(self, subbot, handle):
        try:
            if handle in self.subbots:
                print("subbot '{}' already present; ignored".format(handle))
                return
            self.subbots[handle] = subbot
            for command in subbot.commands:
                self.commands[command] = subbot
            subbot._set_bot_data(self, self.send_message, handle)
            if self.connection:
                subbot.on_welcome()
            return True
        except Exception as err:
            print("adding subbot {} failed: {}".format(handle, err))
            self.remove_subbot(handle)
            return False
        finally:
            sys.stdout.flush() # I suppose this is never executed because of the returns?
    
    def remove_subbot(self, handle):
        if handle not in self.subbots:
            print("subbot '{}' not present; ignored removal".format(handle))
            return
        subbot = self.subbots[handle]
        del self.subbots[handle]
        for command in subbot.commands:
            del self.commands[command]
        try:
            subbot.stop()
            return True
        except Exception as err:
            print("subbot {} errors on stop: {}".format(handle, err))
            return False
        finally:
            sys.stdout.flush()
    
    
    def on_welcome(self, c, e):
        self.connection = c
        self.sender.setConnection(c);
        for channel in self.chanlist:
            c.join(channel)
        for handle, subbot in self.subbots.items():
            try:
                subbot.on_welcome()
            except Exception as err:
                print("subbot {} errors on welcome: {}".format(handle, err))
            finally:
                sys.stdout.flush()
    
    
    def on_join(self, c, e):
        if e.source.nick != c.get_nickname():
            return
        chan = e.target
        self.active_channels.add(chan)
        for handle, subbot in self.subbots.items():
            try:
                subbot.on_enter(chan)
            except Exception as err:
                errmsg = "subbot {} errors on enter: {}".format(handle, err)
                print(errmsg)
                self.send_message(chan, errmsg)
            finally:
                sys.stdout.flush()
    
    def on_pubmsg(self, c, e):
        self.process_command(c, e, e.arguments[0])

    def on_privmsg(self, c, e):
        self.process_command(c, e, e.arguments[0])

    def process_command(self, c, e, text):
        sender = e.source.nick
        chan = e.target
        cmd, _sep, args = text.partition(' ')
        if cmd in self.commands:
            subbot = self.commands[cmd]
            try:
                subbot.on_command(cmd, args, chan, sender, text, e, c)
            except Exception as err:
                errmsg = "subbot {} errors on command {}: {}".format(subbot.handle, text, err)
                print(errmsg)
                self.send_message(chan, errmsg)
            finally:
                sys.stdout.flush()
                sys.stderr.flush()
    
    def send_message(self, chan, text):
        self.sender.send(chan, text)
    
    
    def stop(self):
        for eventname, handler in self.handlers.items():
            self.client.remove_global_handler(eventname, handler)
        if hasattr(self.sender, "stopProcessing"):
            self.sender.stopProcessing()

