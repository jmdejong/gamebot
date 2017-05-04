

from gamesubbot import GameSubBot

class GrunkGame(GameSubBot):
    
    channels = {"#games", "#grunk", "#lostpig", "#bots"}
    commands = {"!grunkstart", "!grunk"}
    startcommand = "!grunkstart"
    runcommand = "!grunk"
    name = "Lost Pig"
    program_arguments = ["./dfrotz", "-m", "LostPig.z8"]

BotModule = GrunkGame
