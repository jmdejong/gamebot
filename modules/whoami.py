
from subbot import SubBot

class WhoAmI(SubBot):
    
    name = "whoami"
    commands = {"!whoami"}
    description = "show the caller's nick, as sent do the bot"
    
    def on_command(self, command, args, chan, sender, text):
        self.reply(chan, sender)



BotModule = WhoAmI
