
from subbot import SubBot

class SwedishTranslationBot(SubBot):
    
    name = "swedish"
    commands = {"!swedish", "!veryswedish", "!veryveryswedish"}
    description = "makes texts swedish with help from yaib. See also: https://www.youtube.com/watch?v=RqvCNb7fKsg"
    
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        self.reply(chan, args)
        self.reply(chan, "s//f")
        if "very" in command:
            self.reply(chan, "s//f")
        if "veryvery" in command:
            self.reply(chan, "s//f")
        

BotModule = SwedishTranslationBot
