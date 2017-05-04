
from subbot import SubBot
import shlex
import json
import importlib

class AdminBot(SubBot):
    
    name = "admin"
    commands = {"!gamebot"}
    channels = {"#gamebot"}
    allowedconfig = "allowed.json"
    description = "Perform administrative tasks without restarting the bot"
    
    def __init__(self):
        self.modules = {}
    
    def on_command(self, command, args, chan, sender, text):
        argv = shlex.split(args)
        task = argv[0]
        
        if task == "join":
            channel = argv[1]
            if channel in self.get_allowed()["channels"]:
                #self.join_channel(argv[1])
                self.bot.connection.join(channel)
                self.reply(chan, "joined {}".format(channel))
            else:
                self.reply(chan, "{} is not an allowed channel in {}".format(channel, self.allowedconfig))
        
        if task == "leave":
            channel = argv[1]
            if channel in self.get_allowed()["channels"]:
                self.bot.connection.part([channel])
                self.reply(chan, "left {}".format(channel))
            else:
                self.reply(chan, "{} is not an allowed channel in {}".format(channel, self.allowedconfig))
        
        if task == "load":
            modulename = argv[1]
            if modulename in self.get_allowed()["modules"]:
                self.load_subbot(modulename)
                self.reply(chan, "{} loaded".format(modulename))
            else:
                self.reply(chan, "{} failed".format(args))
        
        if task == "stop":
            botname = argv[1]
            if botname in self.get_allowed()["modules"]:
                self.stop_subbot(botname)
                self.reply(chan, "{} stopped".format(botname))
            else:
                self.reply(chan, "{} failed: not allowed".format(args))
        
        if task == "reload":
            botname = argv[1]
            if botname in self.get_allowed()["modules"]:
                status = self.reload_subbot(botname)
                self.reply(chan, status)
            else:
                self.reply(chan, "{} failed".format(args))
        
        if task == "help":
            self.reply(chan, "WIP")
        
        if task == "print":
            print(argv[1])
    
    #def join_channel(self,chan):
        #self.bot.connection.join(chan)
    
    def get_allowed(self):
        with open(self.allowedconfig) as f:
            config = json.load(f)
        return config
    
    def load_subbot(self, modulename):
        try:
            importlib.invalidate_caches()
            if modulename in self.modules:
                module = importlib.reload(self.modules[modulename])
            else:
                module = importlib.import_module(modulename)
            self.modules[modulename] = module
            subbot = module.BotModule()
            self.bot.add_subbot(subbot, modulename)
            return "loaded {}".format(modulename)
        except Exception as err:
            return "loading {} failed: {}".format(modulename, err)
    
    def reload_subbot(self, name):
        self.stop_subbot(name)
        self.load_subbot(name)
        return "reloading {} done".format(name)
    
    def stop_subbot(self, botname):
        self.bot.remove_subbot(botname)

BotModule = AdminBot
        
