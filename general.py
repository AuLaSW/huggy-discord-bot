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


@commands.command(
    brief="Add a hug to @'d",
    description="Add a hug to all @'d members",
    usage="mentions: All @'s after the command"
)
async def hug(ctx, *mentions):
    channel = ctx.channel

    if channel.name not in channels:
        return

    author = ctx.author
    guild = ctx.guild
    date = datetime.now(timezone.utc).timestamp()
    text = ""

    mention = ", ".join(mentions)

    if len(mentions) == 0:
        await ctx.send(f"<@{author.id}> I need someone to hug!\nPlease!\nTell me who to hug!\n*shaking* M-my whole existence is hugging!\nWHO DO I HUG?!?!")
        return
    elif len(mentions) == 2:
        temp = mention.rpartition(",")
        mention = temp[0] + " and" + temp[2]
    elif len(mentions) >= 3:
        temp = mention.rpartition(",")
        mention = temp[0] + temp[1] + " and" + temp[2]

    for user in mentions:
        userid = userIDFromMention(user)
        db.addHug(str(author.id), str(guild.id), date, str(userid))
        print("Added hug to database!")

        hugged = db.getUserHugs(str(userid), str(guild.id))[0][0]

        if hugged == 1:
            text += f"\n{user} has been hugged 1 time!"
        else:
            text += f"\n{user} has been hugged {hugged} times!"


    """
    for mention in mentions:
        print(mention[2:-1])
    """

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
        await ctx.send(
            f"<@{author.id}> gave {mention} a hug! {hug_text}\n{text}",
            file=file
        )


@commands.command(
    brief="leaderboard of all hugs",
    description="A leaderboard of all hugs given in the server",
)
async def hugboard(ctx):
    channel = ctx.channel
    guild = ctx.guild

    if channel.name not in channels:
        return

    text = "The Hug Leaderboard:\n\n"
    table = db.getGuildHugs(str(guild.id))

    if len(table) == 0:
        await ctx.send("No hugs have been given yet!")
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

    await ctx.send(text)


@commands.command(
    brief="hugs of @'d users from author",
    description="Gets the hugs of @'d users from author",
    usage="mentions: all users to check for hugs from author"
)
async def hugsto(ctx, *mentions):
    channel = ctx.channel

    if len(mentions) == 0:
        await ctx.send(f"<@{author.id}> I can't find hugs for no-one!")

    if channel.name not in channels:
        return

    author = ctx.author
    guild = ctx.guild
    text = ""

    for user in mentions:
        userid = userIDFromMention(user)
        try:
            hugs = db.getUserHugLinks(str(author.id), str(userid), str(guild.id))[0][0]
        except IndexError:
            await ctx.send(f"No hugs given to <@{userid}>.")
            return

        if hugs is None:
            hugs = "no hugs"
        elif hugs == 1:
            hugs = "1 hug"
        else:
            hugs = f"{hugs} hugs"

        text += f"<@{author.id}> has given {user} {hugs}!\n"

    await ctx.send(text)


def setup(bot):
    """Attaches commands to the incoming bot."""
    print("Adding hugs...")

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

    bot.add_command(hug)

    print("Counting the hugs...")
    bot.add_command(hugboard)

    print("Counting intew hugs to evewyone >,> ...")
    bot.add_command(hugsto)
