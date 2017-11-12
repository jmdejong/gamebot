
from subbot import SubBot
import pwd


SYSTEM_USERS = ['wiki', 'root', 'ubuntu', 'nate', 'nobody']

def get_users():
    """Generate tuples of the form (username, homedir) for all normal
    users on this system.
    """
    return ((p.pw_name, p.pw_dir) for p in pwd.getpwall() if
            p.pw_uid >= 1000 and
            p.pw_shell != '/bin/false' and p.pw_name not in SYSTEM_USERS)


class PopulationBot(SubBot):
    
    name = "population"
    commands = {"!population"}
    description = "Show the number of tilde.town users"
    
    
    def on_command(self, command, args, chan, sender, text):
        self.reply(chan, str(len(list(get_users()))))
        



BotModule = PopulationBot
