"""
bothouse.py
-----------

A module collection of different discord bot skeletons.
"""
from utils import *
import discord
from discord.ext.commands import Bot
from general import setup


class Botty2_0(Bot):
    """
    A botty-otty botilicious bot for hot-bot-summer work.
    """
    async def on_ready(self):
        print('Initiawizing the commands, uwu...')
        setup(self)
        await self.tree.sync()
        print(f'{self.user.name} is weady for hot-bot-summew! >_<')