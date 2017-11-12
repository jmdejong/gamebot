
from subbot import SubBot
from subapi import SubApi

class GameSubBot(SubBot):
    
    
    raw_description = "Plays the game '{name}', a text-based adventure. Everybody sends commands to the same game session. {startcommand} starts the session. Once the session is running everything after the {runcommand} command is directly passed to the game. Only available in channels {channels}"
    
    
    def __init__(self):
        self.game_sessions = {}
        self.description = self.raw_description.format(channels=', '.join(self.channels), name=self.name, startcommand=self.startcommand, runcommand=self.runcommand)
    
    
    def on_command(self, command, args, chan, sender, text):
        if command == self.startcommand:
            if chan in self.game_sessions:
                self.reply(chan, "{name} is already running in this channel. Interact with it with the command {runcommand} <command>, for example: {runcommand} look".format(channels=', '.join(self.channels), name=self.name, startcommand=self.startcommand, runcommand=self.runcommand))
            elif chan not in self.channels:
                self.reply(chan, "To prevent flooding the chat, {name} is not available in this channel. Try one of these channels: {channels}".format(channels=', '.join(self.channels), name=self.name, startcommand=self.startcommand, runcommand=self.runcommand))
            else:
                gameSession = SubApi()
                gameSession.outputListeners.add(lambda text: self.reply(chan, text))
                gameSession.start(self.program_arguments)
                self.game_sessions[chan] = gameSession
            
        elif command == self.runcommand:
            if chan in self.game_sessions:
                self.game_sessions[chan].sendInput(args)
            else:
                self.reply(chan, "No {name} session is running in this channel. Start one with the command {startcommand}".format(channels=', '.join(self.channels), name=self.name, startcommand=self.startcommand, runcommand=self.runcommand))
    
    def stop(self):
        for session in self.game_sessions.values():
            session.stop()
