
from subbot import SubBot
from urllib import request, parse
import json

class TranslateBot(SubBot):
    
    name = "translatebot"
    commands = {"!translate"}
    description = "translate a given text. Powered by Yandex.Translate (https://translate.yandex.com/). Example usage: !translate de-en Guten Tag, wie geht es dir?"
    
    key = "trnsl.1.1.20170506T091418Z.c9cf68304a9ed14c.687b956b33714851a8300106de5de4da009190e9"
    getlangurl = "https://translate.yandex.net/api/v1.5/tr.json/getLangs"
    translateurl = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        if command == "!translate":
            action, _sep, text = args.partition(' ')
            if action == "getlang" or action == "getlangs":
                self.reply(chan, ', '.join(code + ": " + name for code, name in self.getlangs()["langs"].items()))
            else:
                translations = self.translate(action, text)["text"]
                # I don't know why text is a list, but this seems the most intuititive action
                for translation in translations:
                    self.reply(chan, translation)
    
    def translate(self, lang, text):
        return self.loadurl(self.translateurl, [("key", self.key), ("lang", lang), ("text", text)])
    
    def getlangs(self, ui="en"):
        return self.loadurl(self.getlangurl, [("key", self.key), ("ui", ui)])
    
    def loadurl(self, url, data):
        
        with request.urlopen(url, parse.urlencode(data).encode('utf-8')) as f:
            # for some reason python gives an error if I try to read json directly from the url
            s = str(f.read(), encoding="utf-8")
            j = json.loads(s)
            return j



BotModule = TranslateBot
