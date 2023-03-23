"""
Bot.py
------

This application creates a simple and generic Discord Bot instance.
"""
from utils import *
from bothouse import Botty2_0


def main():
    var = {}
    
    load_env_vars(var)

    intentdict = {}
    intentdict["message_content"] = True
    intents = getIntents("default", **intentdict)
    
    db = HugDatabase()
    
    bot = Botty2_0(command_prefix="\\", intents=intents)
    #bot.db = db
    bot.setup()
    
    bot.run(getToken())


if __name__ == "__main__":
    main()