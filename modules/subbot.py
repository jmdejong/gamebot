

class SubBot():
    
    name = ""
    description = ""
    handle = ""
    
    commands = set()
    
    everywhere = False
    
    def _set_bot_data(self, bot, replyfn, handle):
        self.bot = bot
        self.reply = replyfn
        self.handle = handle
    
    # on_welcome is the irc welcome event, when the bot joins a server
    def on_welcome(self):
        pass
    
    # on_enter is called when the bot joins a channel
    # it's like on_join, but not called when someone else joins, and only for the channels this bot is in
    def on_enter(self, chan):
        pass
    
    # on_command is called when the first word of someone's message is a command of this bot
    def on_command(self, command, args, chan, sender, text):
        pass
    
    def get_description(self):
        return "{}. Triggered by commands: {}. {}".format(
            self.name,
            ', '.join(self.commands),
            self.description)
    
    def stop(self):
        pass
