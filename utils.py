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
import pandas as pd
from pandas import DataFrame as df
from pathlib import Path


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
        self._path = Path('.') / 'db'
        # guilds information
        self._guildsPath = self._path / 'guilds.csv'
        # users information
        self._usersPath = self._path / 'users.csv'
        
        self._setup()
    
    def _setup(self):
        # if the databases don't exist, create
        # the folder and files.
        if not self._path.exists():
            self._path.mkdir()
        if not self._guildsPath.exists():
            self._guildsPath.touch()
        if not self._usersPath.exists():
            self._usersPath.touch()
        
        # if the guilds database exists, load it.
        # otherwise, create it.
        try:
            self._guilds = pd.read_csv(self._guildsPath, header=1)
        except pd.errors.EmptyDataError:
            self._guilds = df(
                columns=[
                    'GuildID',
                    'GuildName'
                ]
            )
            # save the dataframe to csv
            self._guilds.to_csv(self._guildsPath)
        
        # If the users database exists, load it.
        # otherwise, create it.
        try:
            self._users = pd.read_csv(self._usersPath, header=1)
        except pd.errors.EmptyDataError:
            self._users = df(
                columns=[
                    'Author',
                    'GuildID',
                    'Timestamp',
                    'HugGivenTo',
                ]
            )
            # save the dataframe to csv
            self._users.to_csv(self._usersPath)
        
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
        self._users.loc[len(self._users.index)] = [
            authorid,
            guildid,
            timestamp,
            huggive,
        ]
        
        self._users.to_csv(self._usersPath)
    
    def addGuild(self, guildid, guildname):
        """Add guild to database"""
        self._guilds.loc[len(self._users.index)] = [
            guildid,
            guildname
        ]
        
        self._guilds.to_csv(self._guildsPath)


def getToken():
    """
    Retrieves the DISCORD_TOKEN from the environment variables.
    """
    load_dotenv()
    
    return os.getenv('DISCORD_TOKEN')