

from gamesubbot import GameSubBot

class SoFarGame(GameSubBot):
    channels = {"#games", "#sofar", "#bots", "#tildeplays"}
    commands = {"!sofarstart", "!sofar"}
    startcommand = "!sofarstart"
    runcommand = "!sofar"
    name = "So Far"
    program_arguments = ["dfrotz", "-m", "games/SoFar.z8"]



BotModule = SoFarGame
