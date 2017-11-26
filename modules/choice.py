
from subbot import SubBot
import random
import shlex

class ChoiceBot(SubBot):
    
    name = "choisebot"
    commands = {"!choice"}
    description = "Choose one item from several options. Separations are same as in shell (space-separated unless quoted)"
    
    def on_command(self, command, args, chan, sender, text):
        choices = shlex.split(args)
        choice = random.choice(choices)
        self.reply(chan, choice)



BotModule = ChoiceBot
