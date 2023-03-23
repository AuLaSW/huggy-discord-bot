"""
general.py
----------

This module holds general commands for attaching to a discord bot.

Every command module has to have a setup(bot) method for attaching
the commands to the bot.
"""
from discord.ext import commands

@commands.command()
async def hello(ctx):
    channel = ctx.message.channel
    await channel.send("Hello!")


def setup(bot):
    """Attaches commands to the incoming bot."""
    bot.add_command(hello)