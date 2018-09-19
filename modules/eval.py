
import asteval

from subbot import SubBot

class Evaluator(SubBot):
    
    name = "eval"
    commands = {"!eval"}
    description = "evaluates a (python-like) expression using asteval"
    
    def __init__(self):
        self.aeval = asteval.Interpreter(no_print=True, no_raise=True, no_assert=True, blacklist_builtins=True, no_functiondef=True)
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        try:
            reply = str(self.aeval(args))
        except Exception as e:
            reply = str(e)
        self.reply(chan, reply)



BotModule = Evaluator
