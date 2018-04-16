
from subbot import SubBot
from urllib import request, parse
import json

class DuckDuckBot(SubBot):
    
    name = "duckduck"
    commands = {"!ddg", "!duckduck", "?"}
    description = "explains a given term using duckduckgo instant answers"
    
    translateurl = "http://api.duckduckgo.com/"
    
    def on_command(self, command, args, chan, *_args, **_kwargs):
        abstract = self.explain(args)
        if abstract:
            self.reply(chan, abstract)
        else:
            self.reply(chan, "no instant answer found")
    
    def explain(self, term):
        data = self.geturl(self.translateurl,  [("format", "json"), ("q", term), ("skip_disambig", 1)])
        answer = data.get("Answer")
        if not answer or not isinstance(answer, str):
            answer = data.get("AbstractText")
        if not answer and "RelatedTopics" in data and len(data["RelatedTopics"]):
            answer = data["RelatedTopics"][0].get("Text")
        return answer
    
    def geturl(self, url, data):
        fullUrl = url + '?' + parse.urlencode(data)
        
        with request.urlopen(fullUrl) as f:
            # for some reason python gives an error if I try to read json directly from the url
            s = str(f.read(), encoding="utf-8")
            j = json.loads(s)
            return j



BotModule = DuckDuckBot
