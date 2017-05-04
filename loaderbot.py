
from subbot import SubBot
import json
import importlib

class LoaderBot(SubBot):
    
    name = "loader"
    commands = {"!gamebotload"}
    channels = {"#gamebot"}
    allowedconfig = "allowed.json"
    description = "reload modules; fallback for when adminbot crashes"
    
    
    def on_command(self, command, args, chan, sender, text):
        
        try:
            modulename = args.partition(' ')[0]
        
            if modulename not in self.get_allowed()["modules"]:
                print("module {} not allowed".format(modulename))
                return
            importlib.invalidate_caches()
            module = importlib.import_module(modulename)
            module = importlib.reload(module)
            subbot = module.BotModule()
            self.bot.add_subbot(subbot, modulename)
            print("succesfully loaded module {}".format(modulename))
        except Exception as err:
            print("loading {} failed: {}".format(modulename, err))
    
    def get_allowed(self):
        with open(self.allowedconfig) as f:
            config = json.load(f)
        return config

BotModule = LoaderBot
        
