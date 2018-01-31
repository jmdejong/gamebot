
from subbot import SubBot
import json
import importlib

class LoaderBot(SubBot):
    
    name = "loader"
    commands = {"!gamebotload"}
    channels = {"#gamebot"}
    allowedconfig = "allowed_modules.txt"
    description = "reload modules; fallback for when admin crashes"
    
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        
        try:
            modulename = args.partition(' ')[0]
            if modulename not in self.get_allowed_modules():
                print("module {} not allowed".format(modulename))
                return
            self.load(modulename)
            
        except Exception as err:
            print("loading {} failed: {}".format(modulename, err))
    
    def load(self, modulename):
        try:
            importlib.invalidate_caches()
            module = importlib.import_module(modulename)
            module = importlib.reload(module)
            subbot = module.BotModule()
            self.bot.add_subbot(subbot, modulename)
            print("succesfully loaded module {}".format(modulename))
        except Exception as err:
            print("loading {} failed: {}".format(modulename, err))
    
    def get_allowed_modules(self):
        with open(self.allowedconfig) as f:
            allowed = set(f.read().split('\n'))
        print(allowed)
        return allowed

BotModule = LoaderBot
        
