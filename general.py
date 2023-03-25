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
    channel = ctx.message.channel
    author = ctx.message.author
    guild = ctx.message.guild
    date = datetime.now(timezone.utc).timestamp()
    text = ""

    if len(mentions) == 0:
        await channel.send(f"<@{author.id}> I need someone to hug!\nPlease!\nTell me who to hug!\n*shaking* M-my whole existence is hugging!\nWHO DO I HUG?!?!")
        return

    for user in mentions:
        userid = userIDFromMention(user)
        db.addHug(str(author.id), str(guild.id), date, str(userid))
        print("Added hug to database!")

        hugged = db.getUserHugs(str(userid), str(guild.id))[0][0]

        text += f"\n{user} has been hugged {hugged} times!"


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
        await channel.send(
            f"<@{author.id}> gave {mention} a hug! {hug_text}\n{text}",
            file=file
        )


@commands.command(
    brief="leaderboard of all hugs",
    description="A leaderboard of all hugs given in the server",
)
async def hugsgiven(ctx):
    channel = ctx.message.channel
    guild = ctx.message.guild
    text = "The Hug Leaderboard:\n\n"
    table = db.getGuildHugs(str(guild.id))

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

    await channel.send(text)


@commands.command(
    brief="hugs of @'d users from author",
    description="Gets the hugs of @'d users from author",
    usage="mentions: all users to check for hugs from author"
)
async def hugsto(ctx, *mentions):
    if len(mentions) == 0:
        await channel.send(f"<@{author.id}> I can't find hugs for no one!")

    channel = ctx.message.channel
    author = ctx.message.author
    guild = ctx.message.guild
    text = ""

    for user in mentions:
        userid = userIDFromMention(user)
        hugs = db.getUserHugLinks(str(author.id), str(userid), str(guild.id))[0][0]
        if hugs is None:
            hugs = "no"
        text += f"\n<@{author.id}> has given {user} {hugs} hugs!"

    await channel.send(text)


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

    print("Counting intew hugs to evewyone >,> ...")
    bot.add_command(hugsto)
