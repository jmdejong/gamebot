
from subbot import SubBot
import random

class WaterBot(SubBot):
    
    name = "waterbot"
    commands = {"!water"}
    description = "water gamebot"
    
    actions = [
        "looks refreshed",
        "shines like new",
        "purrs happily",
        "radiates with happiness",
        "smiles at {sender}"
        ]
    
    def on_command(self, command, args, chan, sender, text, e, c, *_args, **_kwargs):
        if args.strip() == c.get_nickname():
            # note to self: stop using inheritance
            self.bot.connection.action(chan, random.choice(self.actions).format(sender=sender))



BotModule = WaterBot
