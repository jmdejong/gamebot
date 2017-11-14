
from subbot import SubBot

class SwedishTranslationBot(SubBot):
    
    name = "swedish"
    commands = {"!swedish"}
    description = "makes your input swedish (https://www.youtube.com/watch?v=RqvCNb7fKsg)"
    
    
    def on_command(self, command, args, chan, sender, text):
        self.reply(chan, args)
        self.reply(chan, "s//f")
        



BotModule = SwedishTranslationBot
