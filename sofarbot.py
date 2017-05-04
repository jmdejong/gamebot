

from gamesubbot import GameSubBot

class SoFarGame(GameSubBot):
    channels = {"#games", "#sofar", "#bots"}
    commands = {"!sofarstart", "!sofar"}
    startcommand = "!sofarstart"
    runcommand = "!sofar"
    name = "So Far"
    program_arguments = ["./dfrotz", "-m", "SoFar.z8"]



BotModule = SoFarGame
