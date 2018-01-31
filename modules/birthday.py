
from subbot import SubBot
from urllib import request, parse
import json
import subprocess

class BirthdayBot(SubBot):
    
    name = "birthday"
    commands = {"!birthday", "!birthdays"}
    description = "Show what users have their birthday today."
    
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        answer = subprocess.run(["birthday"], stdout=subprocess.PIPE, timeout=3, universal_newlines=True)
        answertext = answer.stdout.replace("\n", "  ")
        self.reply(chan, answertext)
        



BotModule = BirthdayBot
