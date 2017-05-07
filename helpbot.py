
from subbot import SubBot

class HelpBot(SubBot):
    
    name = "helpbot"
    commands = {"!rollcall", "!gamebothelp"}
    description = "Show all functionality of this bot."
    botname = "gamebot"
    
    def on_command(self, command, args, chan, sender, text):
        if command == "!gamebothelp":
            helptext = "{} is ~troido's irc bot. It has several kinds of functionality:\n{}".format(
                self.botname,
                '\n'.join(subbot.get_description() for subbot in self.bot.subbots.values()))
            for line in helptext.split("\n"):
                self.reply(chan, line)
        elif command == "!rollcall":
            self.reply(chan, "{botname} here. I am a modular bot. Currently I have these modules loaded: {modules}. I respond to these commands: {allcommands}. For more information, say !gamebothelp.".format(
                botname = self.botname,
                modules = ', '.join(subbot.name for subbot in self.bot.subbots.values()),
                allcommands = ', '.join(set().union(*(subbot.commands for subbot in self.bot.subbots.values())))))
                



BotModule = HelpBot
