

import time

class GameBot:
    
    def __init__(self, client, channels):
        
        self.chanlist = channels
        self.lastMsg = time.time()
        self.subbots = {}
        self.commands = {}
        self.active_channels = set()
        self.connection = None
        self.client = client
        client.bot = self
    
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
    
    
    def on_welcome(self, c, e):
        self.connection = c
        for channel in self.chanlist:
            c.join(channel)
        for handle, subbot in self.subbots.items():
            try:
                subbot.on_welcome()
            except Exception as err:
                self.remove_subbot(handle)
                print("subbot {} errors on welcome; removed: {}".format(handle, err))
    
    
    def on_join(self, c, e):
        if e.source.nick != c.get_nickname():
            return
        chan = e.target
        self.active_channels = chan
        for hangle, subbot in self.subbots.items():
            try:
                subbot.on_enter(chan)
            except Exception as err:
                self.remove_subbot(handle)
                errmsg = "subbot {} errors on enter; removed: {}".format(handle, err)
                print(errmsg)
                self.send_message(chan, errmsg)
    
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
                self.remove_subbot(subbot.handle)
                errmsg = "subbot {} errors on command {}; removed: {}".format(subbot.handle, text, err)
                print(errmsg)
                self.send_message(chan, errmsg)
    
    
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


