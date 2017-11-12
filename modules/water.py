
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
        "radiates with happiness"
        ]
    
    def on_command(self, command, args, chan, sender, text):
        if args.strip() == "gamebot": # argh! I definitely need a new bot
            # note to self: stop using inheritance
            self.bot.connection.action(chan, random.choice(self.actions))



BotModule = WaterBot
