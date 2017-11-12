
from subbot import SubBot

class HelpBot(SubBot):
    
    name = "helpbot"
    commands = {"!rollcall", "!gamebothelp", "!games"}
    description = "Show all functionality of this bot."
    botname = "gamebot"
    spamfree = {"#tildetown", "#gamebotshort"}
    
    games = {"grunkbot", "hhgttgbot", "sofarbot"}
    
    def on_command(self, command, args, chan, sender, text):
        botmodules = self.bot.subbots.values()
        if command == "!gamebothelp":
            if chan in self.spamfree:
                self.reply(chan, "To prevent spamming the channel, full help is not available here. Try in another channel")
            else:
                helptext = "{} is ~troido's irc bot. It has several kinds of functionality:\n{}".format(
                    self.botname,
                    '\n'.join(subbot.get_description() for subbot in botmodules))
                for line in helptext.split("\n"):
                    self.reply(chan, line)
        elif command == "!rollcall":
            self.reply(chan, "{botname} here. I am a modular bot. Currently I have these modules loaded: {modules}. I respond to these commands: {allcommands}. For more information, say !gamebothelp (long list).".format(
                botname = self.botname,
                modules = ', '.join(subbot.name for subbot in botmodules),
                allcommands = ', '.join(set().union(*(subbot.commands for subbot in botmodules)))))
        elif command == "!games":
            if chan in self.spamfree:
                self.reply(chan, "To prevent spamming the channel, the game list is not available here. Try in another channel")
            else:
                self.reply(chan, "Hi I'm gamebot. I currently have these games available:")
                for name, game in self.bot.subbots.items():
                    if name in self.games:
                        self.reply(chan, "{name}. Startcommand: {startcommand}, runcommand: {command}. Channels: {channels}".format(name=game.name, startcommand=game.startcommand, command=game.runcommand, channels = ', '.join(game.channels)))
                self.reply(chan, "Start a session of a game by running its startcommand. Once a session is running, you can control the game with the runcommand. Everyting you enter after the runcommand will be passed as input to the game.")
                



BotModule = HelpBot
