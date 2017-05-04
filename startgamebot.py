#!/usr/bin/python3

from gamebot import GameBot
from ircclient import IRCClient

from grunkbot import GrunkGame
from sofarbot import SoFarGame
from helpbot import HelpBot
from adminbot import AdminBot
from loaderbot import LoaderBot


if __name__ == '__main__':
    channels = [
        #'#tildetown',
        '#bots_test',
        '#grunk',
        '#lostpig',
        '#bots',
        '#games',
        '#gamebot'
    ]
    client = IRCClient("gamebot", "localhost")
    bot = GameBot(client, channels)
    bot.add_subbot(HelpBot(), 'helpbot')
    bot.add_subbot(GrunkGame(), 'grunkbot')
    bot.add_subbot(SoFarGame(), 'sofarbot')
    bot.add_subbot(AdminBot(), 'adminbot')
    bot.add_subbot(LoaderBot(), 'loaderbot')
    client.start()
