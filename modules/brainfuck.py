#!/usr/bin/python3

from subbot import SubBot


class UnmatchedLoopException(Exception):
    pass


class BFInterpreter:
    
    
    def __init__(self, code, inp):
        self.code = code
        self.inp = inp
        self.memptr = 0
        self.codeptr = 0
        self.mem = {}
        self.nesting = 0
        
        self.commands = {
            ">": self.right,
            "<": self.left,
            "+": self.inc,
            "-": self.dec,
            "[": self.loop,
            "]": self.end,
            ".": self.putch,
            ",": self.getch}
        
        self.output = ""
        self.finished = False
    
    
    def run(self, maxcommands=10000):
        for i in range(maxcommands):
            command = self.getcommand()
            if command in self.commands:
                self.commands[command]()
            self.codeptr += 1
            if self.finished or self.codeptr >= len(self.code):
                break
        return self.output
    
    def getcommand(self):
        return self.code[self.codeptr]
    
    def getmem(self):
        return self.mem.get(self.memptr, 0)
    
    def right(self):
        self.memptr += 1
    
    def left(self):
        self.memptr -= 1
    
    def inc(self):
        self.mem[self.memptr] = self.getmem() + 1
        
    def dec(self):
        self.mem[self.memptr] = self.getmem() - 1
    
    def loop(self):
        if self.getmem():
            self.nesting += 1
        else:
            nesting = 0
            while self.codeptr < len(self.code):
                c = self.getcommand()
                if c == '[':
                    nesting += 1
                elif c == ']':
                    nesting -= 1
                    if nesting == 0:
                        break
                self.codeptr += 1
            else:
                raise UnmatchedLoopException()
    
    def end(self):
        if self.nesting < 1:
            self.finished = True
            return
        if not self.getmem():
            self.nesting -= 1
        else:
            nesting = 0
            while self.codeptr:
                c = self.getcommand()
                if c == '[':
                    nesting -= 1
                    if nesting == 0:
                        break
                elif c == ']':
                    nesting += 1
                self.codeptr -= 1
            else:
                raise UnmatchedLoopException()
    
    def putch(self):
        self.output += chr(self.getmem())
    
    def getch(self):
        if len(self.inp):
            self.mem[self.memptr] = ord(self.inp[0])
            self.inp = self.inp[1:]
        else:
            self.mem[self.memptr] = 0
                
            

class BrainFuck(SubBot):
    
    name = "brainfuck"
    commands = {"!brainfuck", "!bf"}
    description = "run some brainfuck code. The code is also the input for ','"
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        bf = BFInterpreter(args, args)
        try:
            bf.run()
            self.reply(chan, bf.output)
        except UnmatchedLoopException:
            self.reply(char, "Unterminated Loop! output so far: " + bf.output)



BotModule = BrainFuck


if __name__ == "__main__":
    import sys
    bf = BFInterpreter(sys.argv[1], sys.argv[1])
    bf.run()
    print(bf.output)
    memmin = min(bf.mem.keys())
    memmax = max(bf.mem.keys())
    for i in range(memmin, memmax+1):
        m = bf.mem.get(i, 0)
        print("{}{:4d}: {:4d}  {}".format(('*' if i == bf.memptr else ' '), i, m, chr(m)))
