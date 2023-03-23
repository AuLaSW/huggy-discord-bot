"""
utils.py
--------

All of the utilities used in the discord bot
application.
"""
import os
from dotenv import load_dotenv
from collections import namedtuple
import discord
from pathlib import Path
import sqlite3


def load_env_vars(var) -> dict():
    """
    This is a generic function for loading the environment variables.
    
    Arguments
    ---------
    
        var: A dictionary from createEnvVars of the different attributes
            for the environment variables in the application.
    
    Returns:
    --------
    
        env: A named tuple of variable_name-env_value key-value pairs.
            This holds all of the environment variables that are used
            by the project.
    """
    load_dotenv()
    
    env = {}
    temp = []
    
    for key, value in var.items():
        print(key, value)
        try:
            if value == 'DISCORD_TOKEN':
                raise RuntimeError()
            env[key] = os.getenv(value)
            temp.append(env[key])
        except AttributeError:
            print(f"No environment variable {value} found!")
        except RuntimeError:
            print(
                "I cannot access the discord token through load_env_vars.", 
                "Please find another way."
            )

    Env = namedtuple("EnvVars", temp)
    
    env = Env._make(temp)

    return env


def getIntents(base="none", **kwargs):
    """
    This is a method for cleaning up intents setting.
    
    Accepts a dictionary of intents, where the keys
    are the different intents and the values are boolean.
    """
    intents = getattr(discord.Intents, base, "none")()
    
    for intent, value in kwargs.items():
        try:
            setattr(intents, intent, value)
        except AttributeError as e:
            raise e
    
    return intents


def userIDFromMention(mention):
    return mention[2:-1]


class HugDatabase:
    """
    This class manages the data associated with the discord bot.
    """
    def __init__(self):
        # folder where "database" is stored
        self._folder = Path('.') / 'db'
        self._path = self._folder / 'hugging.db'
        
        if not self._folder.exists():
            self._folder.mkdir()
        if not self._path.exists():
            self._path.touch()

        self._connection = sqlite3.Connection(self._path)
        
        self._setup()
        
        self._connection.commit()
    
    def __str__(self):
        cur = self._connection.cursor()
        
        res = cur.execute("SELECT * FROM hugs")
        
        return str(res.fetchall())
    
    def _setup(self):
        cur = self._connection.cursor()
        res = cur.execute("SELECT name FROM sqlite_master WHERE name='hugs';")
        
        if res.fetchone() is None:
            cur.execute("""
                CREATE TABLE hugs(authorid, guildid, timestamp, huggivento);
                """
            )
        
        """
        Guilds metadata:
        ----------------
        
        | GuildID | GuildName |
        -----------------------
        | #       | str       |
        
        Users metadata:
        ---------------
        
        | Author | GuildID | Timestamp | HugGivenTo |
        ---------------------------------------------
        | str    | GuildID | UTC-time  | UserID     |
        """
    
    def _ETL(self):
        raise NotImplementedError("ETL not yet implemented")
    
    def addHug(self, authorid, guildid, timestamp, huggive=None):
        """Add hug to database"""
        inputs = [ authorid, guildid, timestamp, huggive ]
        cur = self._connection.cursor()
        
        cur.executemany("""
            INSERT INTO hugs VALUES
                (?, ?, ?, ?);
            """,
            (inputs,)
        )
        
        self._connection.commit()
        

class HugETL:
    pass


def getToken():
    """
    Retrieves the DISCORD_TOKEN from the environment variables.
    """
    load_dotenv()
    
    return os.getenv('DISCORD_TOKEN')