

import time
import sys
import json

class GameBot:
    
    
    def __init__(self, client, channels):
        
        self.handlers = {
            "welcome": self.on_welcome,
            "join": self.on_join,
            "privmsg": self.on_privmsg,
            "pubmsg": self.on_pubmsg
        }
        
        self.chanlist = channels
        self.lastMsg = time.time()
        self.subbots = {}
        self.commands = {}
        self.active_channels = set()
        self.connection = None
        self.client = client
        for eventname, handler in self.handlers.items():
            client.add_global_handler(eventname, handler)
    
    # add a subbot to the bot. Return whether succesfull
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
            sys.stdout.flush()
    
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
        #self.active_channels = chan
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
                subbot.on_command(cmd, args, chan, sender, text)
            except Exception as err:
                errmsg = "subbot {} errors on command {}: {}".format(subbot.handle, text, err)
                print(errmsg)
                self.send_message(chan, errmsg)
            finally:
                sys.stdout.flush()
                sys.stderr.flush()
    
    
    def _waitForMessage(self):
        while(time.time() - self.lastMsg < 0.5):
            time.sleep(0.2)
        self.lastMsg = time.time()
    
    def send_message(self, chan, text):
        try:
            maxlen = 400
            if len(text) > maxlen:
                self.send_message(chan, text[:maxlen])
                self.send_message(chan, text[maxlen:])
                return
            
            self._waitForMessage()
            self.connection.privmsg(chan, text)
        except Exception as err:
            print("sending message {} to channel {} failed: {}".format(text, chan, err))
        finally:
            sys.stdout.flush()
    
    def stop(self):
        for eventname, handler in self.handlers.items():
            self.client.remove_global_handler(eventname, handler)

