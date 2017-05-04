

import irc.bot

class IRCClient(irc.bot.SingleServerIRCBot):
    def __init__(self, nickname, server='localhost', port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.bot = None
    
    
    def on_welcome(self, c, e):
        if self.bot:
            self.bot.on_welcome(c, e)
    
    def on_join(self, c, e):
        self.bot.on_join(c, e)
    
    def on_privmsg(self, c, e):
        self.bot.on_privmsg(c, e)
    
    def on_pubmsg(self, c, e):
        self.bot.on_privmsg(c, e)
