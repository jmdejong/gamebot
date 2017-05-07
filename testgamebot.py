#!/usr/bin/python3

from gamebot import GameBot
import irc.client

from loaderbot import LoaderBot


if __name__ == '__main__':
    channels = [
        #'#tildetown',
        '#bots_test',
        '#games',
        '#testgamebot'
    ]
    bots = [
        'loaderbot',
        'adminbot',
        'helpbot',
        'grunkbot'
    ]
    
    
    reactor = irc.client.Reactor()
    client = reactor.server().connect("localhost", 6667, "testgamebot")
    
    
    bot = GameBot(reactor, channels)
    loader = LoaderBot()
    bot.add_subbot(loader, 'loaderbot')
    for bot in bots:
        loader.load(bot)
    #client.start()
    
    reactor.process_forever()
