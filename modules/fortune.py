
from subbot import SubBot
from urllib import request, parse
import json
import subprocess

class DuckDuckBot(SubBot):
    
    name = "fortunek"
    commands = {"!fortune"}
    description = "Show a random epigram."
    
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        answer = subprocess.run(["fortune", "-s"], stdout=subprocess.PIPE, timeout=3, universal_newlines=True)
        answertext = answer.stdout.replace("\n", "  ")
        self.reply(chan, answertext)
        



BotModule = DuckDuckBot
