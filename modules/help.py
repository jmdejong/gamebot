
from subbot import SubBot

class HelpBot(SubBot):
    
    name = "help"
    commands = {"!rollcall", "!gbrollcall", "!gamebothelp", "!gbhelp", "!gamebotmodules", "!gbmodules", "!games", "!gamebotcommands", "!gbcommands"}
    description = "Show all functionality of this bot."
    botname = "gamebot"
    spamfree = {"#tildetown", "#gamebotshort"}
    
    games = {"grunk", "hhgttg", "sofar"}
    
    def on_command(self, command, args, chan, sender, text):
        help = self.getHelp(command, args.split(), chan in self.spamfree)
        for line in help.split('\n'):
            self.reply(chan, line)
    
    def getHelp(self, command, args, spamFree=False):
        
        if command == "!rollcall" or command == "!gbrollcall":
            return self.rollcall()
        
        if command == "!gamebothelp" or command == "!gbhelp":
            if len(args) < 1:
                return self.shortHelp()
            if args[0] in self.bot.subbots:
                return self.moduleHelp(args[0])
            if args[0] == "all" or args[0] == "*":
                if spamFree:
                    return "to avoid clogging the main channel, the full list is not available here. Try another channel"
                return self.longHelp()
            if args[0] == "modules":
                return self.getModules()
        
        if command == "!gamebotmodules" or command == "!gbmodules":
            return self.getModules()
        
        if command == "!games":
            if spamFree:
                return "to avoid clogging the main channel, this list is not available here. Try another channel"
            return self.gameHelp()
        
        if command == "!gamebotcommands" or command == "!gbcommands":
            if len(args) < 1:
                return self.getAllCommands()
            return self.getCommands(args[1])
    
    
    def rollcall(self):
        return self.format("{botname} here. I am a modular bot. Run !gbmodules to see a list of loaded modules. Run !gbcommands to see a list of commands. For all more information, say '!gamebothelp' or '!gbhelp'")
    
    def shortHelp(self):
        return self.format("{botname} is ~troido's irc bot. It has several independently running modules. To see a list of currently loaded modules say '!gbmodules'. To see the list of commands that gamebot replies to say '!gbcommands'. To see information on a specific module, say '!gbhelp <module>' where <module> is the name of the module. For a list of information on all modules, say '!gbhelp *' (unavailable in channel #tildetown)")
    
    def longHelp(self):
        helptext = self.format("{botname} is ~troido's irc bot. It has several kinds of functionality:\n{allhelp}")
        return helptext
    
    def moduleHelp(self, name):
        modules = self.bot.subbots
        if name not in modules:
            return "module {} not found".format(name)
        return modules[name].get_description()
    
    def allModuleHelp(self):
        return '\n'.join(self.moduleHelp(module) for module in self.bot.subbots)
    
    def getModules(self):
        return ', '.join(name for name in self.bot.subbots)
    
    def gameHelp(self, spamfree=False):
        help = "Hi I'm gamebot. I currently have these games available:\n"
        for name, game in self.bot.subbots.items():
            if name in self.games:
                help += "{name}. Startcommand: {startcommand}, runcommand: {command}. Channels: {channels}\n".format(name=game.name, startcommand=game.startcommand, command=game.runcommand, channels = ', '.join(game.channels))
        help += "Start a session of a game by running its startcommand. Once a session is running, you can control the game with the runcommand. Everyting you enter after the runcommand will be passed as input to the game."
        return help
    
    def getAllCommands(self):
        return ', '.join(set().union(*(subbot.commands for subbot in self.bot.subbots.values())))
    
    def getBotCommands(self, bot):
        if bot not in self.subbots:
            return ""
        return ', '.join(self.subbots[bot].commands)
    
    def format(self, text):
        return (text.format(
                botname = self.botname,
                modules = self.getModules(),
                allcommands = ', '.join(set().union(*(subbot.commands for subbot in self.bot.subbots.values()))),
                allhelp = self.allModuleHelp()
            ))



BotModule = HelpBot
