
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
    minargs = 16
    
    
    def on_command(self, command, args, chan, sender, text):
        argv = shlex.split(args)
        # ensure argv[0] and argv[1] etc. don't error
        for i in range(self.minargs):
            if i>len(argv):
                argv.append(None)
        
        task = argv[0]
        
        if task == "join":
            channel = argv[1]
            if channel in self.get_allowed()["channels"]:
                #self.join_channel(argv[1])
                self.bot.connection.join(channel)
                self.reply(chan, "joined {}".format(channel))
            else:
                self.reply(chan, "{} is not an allowed channel in {}".format(channel, self.allowedconfig))
        
        elif task == "leave":
            channel = argv[1]
            if channel in self.get_allowed()["channels"]:
                self.bot.connection.part([channel])
                self.reply(chan, "left {}".format(channel))
            else:
                self.reply(chan, "{} is not an allowed channel in {}".format(channel, self.allowedconfig))
        
        elif task == "load":
            modulename = argv[1]
            if modulename in self.get_allowed()["modules"]:
                status = load_subbot(modulename, self.bot)
                self.reply(chan, status)
            else:
                self.reply(chan, "{} not allowed".format(args))
        
        elif task == "stop":
            botname = argv[1]
            if botname in self.get_allowed()["modules"]:
                status = self.stop_subbot(botname)
                self.reply(chan, status)
            else:
                self.reply(chan, "{} not allowed".format(args))
        
        elif task == "reload":
            botname = argv[1]
            if botname in self.get_allowed()["modules"]:
                status = self.reload_subbot(botname)
                self.reply(chan, status)
            else:
                self.reply(chan, "{} not allowed".format(args))
        
        elif task == "reloadcore":
            try:
                if not self.get_allowed().get("reloadcore"):
                    self.reply(chan, "reloading core not allowed")
                    return
                oldcore = self.bot
                subbots = self.bot.subbots
                chanlist = self.bot.chanlist
                client = self.bot.client
                importlib.invalidate_caches()
                module = importlib.import_module("gamebot")
                module = importlib.reload(module)
                
                gamebot = module.GameBot(client, chanlist)
                gamebot.on_welcome(self.bot.connection, None)
                for name, subbot in subbots.items():
                    gamebot.add_subbot(subbot, name)
                    #self.bot.remove_subbot(name)
                oldcore.stop()
                self.reply(chan, "gamebot core reloaded")
                
                
            except Exception as err:
                errmsg = "reloading core failed: {}".format(err)
                print(errmsg)
                self.reply(chan, errmsg)
        
        elif task == "echo":
            self.reply(chan, argv[1])
        
        elif task == "print":
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
            module = importlib.import_module(modulename)
            module = importlib.reload(module)
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


def load_subbot(modulename, bot):
    try:
        importlib.invalidate_caches()
        module = importlib.import_module(modulename)
        module = importlib.reload(module)
        subbot = module.BotModule()
        bot.add_subbot(subbot, modulename)
        return "loaded {}".format(modulename)
    except Exception as err:
        return "loading {} failed: {}".format(modulename, err)


BotModule = AdminBot
        
