
from subbot import SubBot

class HelpBot(SubBot):
    
    name = "helpbot"
    commands = {"!rollcall"}
    description = "Show all functionality of this bot."
    botname = "gamebot"
    
    def on_command(self, command, args, chan, sender, text):
        self.reply(chan, "{} is ~troido's irc bot. It has several kinds of functionality:   {}".format(
            self.botname,
            '   '.join(subbot.get_description() for subbot in self.bot.subbots.values())))



BotModule = HelpBot
