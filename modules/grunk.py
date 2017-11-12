

from gamesubbot import GameSubBot

class GrunkGame(GameSubBot):
    
    channels = {"#games", "#grunk", "#lostpig", "#bots", "#tildeplays"}
    commands = {"!grunkstart", "!grunk"}
    startcommand = "!grunkstart"
    runcommand = "!grunk"
    name = "Lost Pig"
    program_arguments = ["dfrotz", "-m", "games/LostPig.z8"]

BotModule = GrunkGame
