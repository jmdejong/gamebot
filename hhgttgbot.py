

from gamesubbot import GameSubBot

class HhgttgGame(GameSubBot):
    
    channels = {"#games", "#hhgttg", "#bots", "#tildeplays"}
    commands = {"!hhgttgstart", "!hhgttg"}
    startcommand = "!hhgttgstart"
    runcommand = "!hhgttg"
    name = "Hitchhikers Guide to the Galaxy game"
    program_arguments = ["games/dfrotz", "-m", "games/SGOLD-HH.z5"]

BotModule = HhgttgGame
