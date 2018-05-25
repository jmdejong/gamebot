
from subbot import SubBot

class PrimeFactors(SubBot):
    
    name = "primefactors"
    commands = {"!primefactors"}
    description = "return the primefactors of a given integer"
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        try:
            val = int(args)
        except ValueError:
            return
        reply = ""
        factors = []
        for i in range(2, 10000):
            while val%i == 0:
                factors.append(i)
                val //= i
            if val == 1:
                break
        else:
            reply = "number too large. Found so far: "
        reply += ','.join(map(str, factors))
        self.reply(chan, reply)



BotModule = PrimeFactors
