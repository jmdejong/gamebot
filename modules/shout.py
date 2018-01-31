
from subbot import SubBot

class Shout(SubBot):
    
    name = "shout"
    commands = {"!shout", "!SHOUT"}
    description = "shout some text"
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        self.reply(chan, args.upper())



BotModule = Shout
