
import ast
import asteval
# using a modified version of asteval (unless it will be merged)
# see https://github.com/jmdejong/asteval/tree/gb

try:
    import hy
    from hy.compiler import hy_compile
except ImportError:
    hy = None

from subbot import SubBot

class Evaluator(SubBot):
    
    name = "eval"
    commands = {"!eval", "!python", "!python3", "!hy"}
    description = "evaluates a (python-like) expression using asteval"
    
    def __init__(self):
        symtable = asteval.make_symbol_table()
        del symtable["open"]
        self.aeval = asteval.Interpreter(symtable, no_print=True, blacklist_builtins=True)
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        if command == "!hy":
            if hy is None:
                self.reply(chan, "Hy is not installed")
                return
            try:
                tree = hy_compile(hy.read_str(args), "__main__")
            except Exception as ex:
                # I don't like catching all but I don't know how many errors this can throw
                self.reply(chan, "Parsing Error: "+str(ex))
                return
        else:
            try:
                tree = ast.parse(args)
            except SyntaxError as ex:
                self.reply(chan, "Syntax Error: "+str(ex))
        returnval = None
        error = None
        try:
            returnval = str(self.aeval(args))
        except asteval.EvalError as e:
            error = e
        if returnval:
            self.reply(chan, returnval)
        if error:
            self.reply(chan, error)



BotModule = Evaluator