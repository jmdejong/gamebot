
from subbot import SubBot

class WhoAmI(SubBot):
    
    name = "whoami"
    commands = {"!whoami"}
    description = "show the caller's nick, username and hostname as sent do the bot"
    
    def on_command(self, command, args, chan, sender, text, e, c, *_args, **_kwargs):
        self.reply(chan, " ".join([sender, e.source.user, e.source.host]))


BotModule = WhoAmI
