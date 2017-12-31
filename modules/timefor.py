

import datetime
import subprocess
import urllib.request
import re
import json

import pytz

from subbot import SubBot


def getIp(username):
    finger = subprocess.run(["finger", "-p", username], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=3, universal_newlines=True).stdout
    #ip = finger.split("\n")[2].split(" ")[-1]
    ipmatch = re.search("\d+\.\d+\.\d+\.\d+", finger)
    if not ipmatch:
        return None
    ip = ipmatch.group(0)
    return ip

def getData(ip):
    url = "https://freegeoip.net/json/"+ip
    with urllib.request.urlopen(url) as r:
        # for some reason python gives an error if I try to read json directly from the url
        text = str(r.read(), encoding="utf-8")
        data = json.loads(text)
        return data

def getTimeIn(timezoneName):
    return datetime.datetime.now(pytz.timezone(timezoneName))

class TimeFor(SubBot):
    
    name = "timefor"
    commands = {"!timefor", "!datetimefor"}
    description = "Display the current time for a tilde.town user (assuming they don't use a VPN)"
    
    def on_command(self, command, args, chan, sender, text):
        user = args.split()[0]
        ip = getIp(user)
        if not ip:
            self.reply(chan, "no ip found for user "+user)
            return
        data = getData(ip)
        if not data or "time_zone" not in data or not data["time_zone"]:
            self.reply(chan, "no timezone info found for user "+user)
            return
        timezone = data["time_zone"]
        time = getTimeIn(timezone).replace(microsecond=0)
        timestring = "{}:{}    full datetime: {}".format(time.hour, time.minute, time.isoformat())
        if command == "!datetimefor":
            timestring = time.isoformat()
        self.reply(chan, timestring)

BotModule = TimeFor

