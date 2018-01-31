#!/usr/bin/python3

import datetime as dt


refformat = dt.timezone(dt.timedelta(hours=2))
refdate = dt.datetime(2016, 4, 25, 7, tzinfo=refformat)


def getIdiotTime(indt=dt.datetime.now(tz=refformat)):
    diff = indt - refdate
    hours = (diff // dt.timedelta(hours=25) + 7) % 24
    minutes = int((diff % dt.timedelta(hours=25)).total_seconds() // 60)
    seconds = indt.second
    return (hours, minutes, seconds)

from subbot import SubBot

class IdiotTimeBot(SubBot):
    
    name = "idiottimebot"
    commands = {"!idiottime", "!itf", "!ITF"}
    description = "Display the current time in Idiot Time Format"
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        hours, minutes, seconds = getIdiotTime(dt.datetime.now(tz=dt.timezone(dt.timedelta(0))))
        self.reply(chan, "it's {}:{}:{}".format(hours, minutes, seconds))



BotModule = IdiotTimeBot
