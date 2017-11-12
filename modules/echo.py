
from subbot import SubBot

class EchoBot(SubBot):
    
    name = "echobot"
    commands = {"!echo"}
    description = "echo some text"
    
    def on_command(self, command, args, chan, sender, text):
        self.reply(chan, args)



BotModule = EchoBot
