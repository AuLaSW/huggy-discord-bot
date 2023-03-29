"""
general.py
----------

This module holds general commands for attaching to a discord bot.

Every command module has to have a setup(bot) method for attaching
the commands to the bot.
"""
import random
from pathlib import Path
#from discord.ext import commands
from discord import app_commands
import discord
from datetime import datetime, timezone
from utils import *


@app_commands.command(
    description="Give someone a hug!"
)
async def hug(ctx: discord.Interaction, user: discord.User):
    channel = ctx.channel

    if channel.name not in channels:
        return

    author = ctx.user
    guild = ctx.guild
    date = datetime.now(timezone.utc).timestamp()
    text = ""

    db.addHug(str(author.id), str(guild.id), date, str(user.id))
    print("Added hug to database!")

    hugged = db.getUserHugs(str(user.id), str(guild.id))[0][0]

    if hugged == 1:
        text += f"\n{user.mention} has been hugged 1 time!"
    else:
        text += f"\n{user.mention} has been hugged {hugged} times!"

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
        await ctx.response.send_message(
            f"<@{author.id}> gave {user.mention} a hug! {hug_text}\n{text}",
            file=file
        )


@app_commands.command(
    description="The leaderboard of hugs."
)
async def hugboard(ctx: discord.Interaction):
    channel = ctx.channel
    guild = ctx.guild

    if channel.name not in channels:
        return

    text = "The Hug Leaderboard:\n\n"
    table = db.getGuildHugs(str(guild.id))

    if len(table) == 0:
        await ctx.response.send_message("No hugs have been given yet!")
        return

    for entry in table:
        if entry[1] == 0:
            line = f'<@{entry[0]}> has no hugs! (free hug on me) :(\n'

            date = datetime.now(timezone.utc).timestamp()
            db.addHug(None, str(guild.id), str(date), str(entry[0]))
        elif entry[1] == 1:
            line = f'<@{entry[0]}> has 1 hug! :)\n'
        else:
            line = f'<@{entry[0]}> has {entry[1]} hugs! Wow! :O\n'
        text += line

    await ctx.response.send_message(text)


@app_commands.command(
    description="How many hugs author has given user"
)
async def hugsto(ctx: discord.Interaction, user: discord.User):
    hugsbetween(ctx, ctx.user, user)
    
    
@app_commands.command(
    description="How many hugs between users"
)
async def hugsbetween(ctx: discord.Interaction, user1: discord.User, user2: discord.User):
    channel = ctx.channel

    if channel.name not in channels:
        return

    guild = ctx.guild
    text = ""

    try:
        hugs = db.getUserHugLinks(str(user1.id), str(user2.id), str(guild.id))[0][0]
    except IndexError:
        await ctx.response.send_message(f"No hugs given to {user2.mention}.")
        return

    if hugs is None:
        hugs = "no hugs"
    elif hugs == 1:
        hugs = "1 hug"
    else:
        hugs = f"{hugs} hugs"

    text += f"{user1.mention} has given {user2.mention} {hugs}!\n"

    await ctx.response.send_message(text)


def setup(bot):
    """Attaches commands to the incoming bot."""
    print("Adding hugs...")
    
    tree = bot.tree

    print("Listening to channels...")
    global channels

    # a list of channels to listen to
    channels = [
        "bot-commands"
    ]

    print("Genewating hug visuals...")
    global hugs_visual
    hugs_visual = list(Path('./content/').glob('*.mp4'))
    for hugs in hugs_visual:
        print(str(hugs))

    print("Accessing the database owo...")
    global db
    db = bot.db

    tree.add_command(hug)

    print("Counting the hugs...")
    tree.add_command(hugboard)

    print("Counting intew hugs to evewyone >,> ...")
    tree.add_command(hugsto)
    
    print("Counting hugs between evewyone >,> ...")
    tree.add_command(hugsbetween)
    
    return tree
