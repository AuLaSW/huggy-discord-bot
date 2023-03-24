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
from datetime import datetime, timezone
from utils import *


@commands.command()
async def hug(ctx, *mentions):
    channel = ctx.message.channel
    author = ctx.message.author
    guild = ctx.message.guild
    date = datetime.now(timezone.utc).timestamp()

    if len(mentions) == 0:
        await channel.send(f"<@{author.id}> I need someone to hug!\nPlease!\nTell me who to hug!\n*shaking* M-my whole existence is hugging!\nWHO DO I HUG?!?!")
        return

    for user in mentions:
        userid = userIDFromMention(user)
        db.addHug(str(author.id), str(guild.id), date, str(userid))
        print("Added hug to database!")
        # hugged.append(db.getUserHug(str(userid), str(guild.id))

    """
    for mention in mentions:
        print(mention[2:-1])
    """
    mention = ", ".join(mentions)

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
        await channel.send(f"<@{author.id}> gave {mention} a hug! {hug_text}\n{hugged}", file=file)


@commands.command()
async def hugsgiven(ctx):
    text = "The Hug Leaderboard:\n\n"
    table = db.getGuildHugs(str(ctx.message.guild.id))

    for entry in table:
        line = f'<@{entry[0]}> has {entry[1]} hugs!\n'
        text += line

    await ctx.message.channel.send(text)


def setup(bot):
    """Attaches commands to the incoming bot."""
    print("Adding hugs...")
    print("Genewating hug visuals...")
    global hugs_visual
    hugs_visual = list(Path('./content/').glob('*.mp4'))
    print("Accessing the database owo...")
    global db
    db = bot.db
    bot.add_command(hug)
    print("Counting the hugs...")
    bot.add_command(hugsgiven)
