

import datetime
import subprocess
import urllib.request
import re
import json

import pytz

from subbot import SubBot


def getIp(username):
    finger = subprocess.run(["finger", "-p", username], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=3, universal_newlines=True).stdout
    ipmatch = re.search("\s(\d+\.\d+\.\d+\.\d+)[\s$]", finger)
    if not ipmatch:
        ipmatch = re.search("\s([0-9A-Fa-f]*:[0-9A-Fa-f:]*:[0-9A-Fa-f]+)[\s$]", finger)
        if not ipmatch:
            print("no ip matched")
            return None
    ip = ipmatch.group(1)
    return ip


def getData(ip):
    url = "http://ip-api.com/json/{ip}".format(ip=ip)
    with urllib.request.urlopen(url) as r:
        # for some reason python gives an error if I try to read json directly from the url
        text = str(r.read(), encoding="utf-8")
        data = json.loads(text)
        return data

def getTimeZone(username):
    try:
        with open("/home/"+username+"/.timezone", "r") as f:
            timezone = f.read().strip()
        return timezone
    except OSError:
        ip = getIp(username)
        if not ip:
            return None
        data = getData(ip)
        if not data:
            return None
        timezone = data.get("timezone")
        return timezone

def getTimeIn(timezoneName):
    return datetime.datetime.now(pytz.timezone(timezoneName))

class TimeFor(SubBot):
    
    name = "timefor"
    commands = {"!timefor", "!datetimefor"}
    description = "Display the current time for a tilde.town user (assuming they don't use a VPN). If the timezone doesn't show up or is incorrect, you can create a .timezone file in your homedir which contains your timezone in the format Area/City (for example Europe/Amsterdam). See /home/troido/.timezone for an example. Leave your .timezone file empty to hide your timezone."
    
    def on_command(self, command, args, chan, sender, *_args, **_kwargs):
        a = args.strip().split()
        if len(a)>0:
            user = a[0]
        else:
            user = sender
        timezone = getTimeZone(user)
        if timezone is None:
            self.reply(chan, "no timezone information found for user "+user)
            return
        elif timezone == "":
            self.reply(chan, "{} does not want to show their timezone".format(user))
            return
        try:
            time = getTimeIn(timezone).replace(microsecond=0)
        except pytz.exceptions.UnknownTimeZoneError:
            self.reply(chan, user+" has an invalid timezone string: "+timezone)
            return
        timestring = "{}    full datetime: {}".format(time.strftime("%H:%M"), time.isoformat())
        if command == "!datetimefor":
            timestring = time.isoformat()
        self.reply(chan, timestring)

BotModule = TimeFor

