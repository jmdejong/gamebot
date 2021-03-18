#!/usr/bin/python3


from subbot import SubBot

class ShrugBot(SubBot):
    
    name = "shrug"
    commands = {"!shrug", "!Shrug", "SHRUG"}
    description = "¯\_(ツ)_/¯ "
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        self.reply(chan, "¯\_(ツ)_/¯ ")



BotModule = ShrugBot
