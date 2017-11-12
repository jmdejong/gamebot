#!/usr/bin/python3 -u

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
from gamebot import GameBot
import irc.client
from loader import LoaderBot
import json

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        configPath = sys.argv[1]
    else:
        configPath = "config.json"
    
    with open(configPath) as configfile:
        config = json.load(configfile)
    
    channels = config["startchannels"]
    bots = config["startmodules"]
    name = config.get("name", "gamebot")
    
    irc.client.ServerConnection.buffer_class.errors = 'replace'
    
    reactor = irc.client.Reactor()
    client = reactor.server().connect("localhost", 6667, name)
    
    bot = GameBot(reactor, channels)
    loader = LoaderBot()
    bot.add_subbot(loader, 'loaderbot')
    for bot in bots:
        loader.load(bot)
    
    reactor.process_forever()
    
