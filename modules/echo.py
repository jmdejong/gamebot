
from subbot import SubBot

class EchoBot(SubBot):
    
    name = "echobot"
    commands = {"!echo"}
    description = "echo some text"
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        self.reply(chan, args)



BotModule = EchoBot
