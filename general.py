"""
general.py
----------

This module holds general commands for attaching to a discord bot.

Every command module has to have a setup(bot) method for attaching
the commands to the bot.
"""
import random
from pathlib import Path
from discord.ext import commands
import discord



@commands.command()
async def hug(ctx, *mentions):
    channel = ctx.message.channel
    author = ctx.message.author
    
    if len(mentions) == 0:
        await channel.send(f"<@{author.id}> I need someone to hug!\nPlease!\nTell me who to hug!\n*shaking* M-my whole existence is hugging!\nWHO DO I HUG?!?!")
        return
    
    mention = ", ".join(mentions)
    
    """
    for mention in mentions:
        print(mention[2:-1])
    """

    if len(mentions) > 1:
        mention = mention.rpartition(",")
        if len(mentions) == 2:
            mention = mention[0] + " and" + mention[2]
        else:
            mention = mention[0] + mention[1] + " and" + mention[2]
    
    hugs_text = [
        "I bet you needed that today!",
        "Aww, come on in!",
        "*licks your ear*",
        "I don't know what you're wearing, but it smells great!",
        "It's okay, I'm here for you.", 
        "I hope your day gets better."
    ]
    
    hug_text = random.choice(hugs_text)
    
    with random.choice(hugs_visual) as hug_visual:
        file = discord.File(fp=hug_visual)
        await channel.send(f"<@{author.id}> gave {mention} a hug! {hug_text}", file=file)


def setup(bot):
    """Attaches commands to the incoming bot."""
    print("Adding hugs...")
    print("Generating hug visuals...")
    global hugs_visual
    hugs_visual = list(Path('./content/').glob('*.mp4'))
    for path in hugs_visual:
        print(path)
    bot.add_command(hug)