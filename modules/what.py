
from subbot import SubBot

class WhatBot(SubBot):
    
    name = "what"
    commands = {"!what"}
    description = "Get the description of some word by calling other bots and using duckduckgo"
    
    def on_command(self, command, args, chan, sender, text):
        ddgbot = self.bot.commands["!ddg"]
        answer = ddgbot.explain(args)
        if answer:
            self.reply(chan, answer)
        self.reply(chan, "!define " + args)
        self.reply(chan, ",ud " + args)
        self.reply(chan, "!acronym " + args)
        



BotModule = WhatBot
