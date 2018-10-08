

import datetime
import subprocess
import urllib.request
import re
import json

import pytz

from subbot import SubBot


def getIp(username):
    finger = subprocess.run(["finger", "-p", username], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=3, universal_newlines=True).stdout
    ipmatch = re.search("\d+\.\d+\.\d+\.\d+", finger)
    if not ipmatch:
        return None
    ip = ipmatch.group(0)
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
        timezone = data.get("time_zone")
        return timezone

def getTimeIn(timezoneName):
    return datetime.datetime.now(pytz.timezone(timezoneName))

class TimeFor(SubBot):
    
    name = "timefor"
    commands = {"!timefor", "!datetimefor"}
    description = "Display the current time for a tilde.town user (assuming they don't use a VPN)"
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        user = args.split()[0]
        timezone = getTimeZone(user)
        if not timezone:
            self.reply(chan, "no timezone information found for user "+user)
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

