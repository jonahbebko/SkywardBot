# ping helpers?
PINGHELPERS = True

"""

LIST OF COMMANDS:

/dm <role> <message> (admin only)
sends a message in dms to everyone with the pinged role

/casterinfo (dms only)
sends a list of caster availability set by /setcasterinfo

/setcasterinfo <message> (admin only)
sets the message given by /casterinfo

/report <week> <ID> <score-score> <ID> (dms only)
used to report match, sends the info to a designated channel or gsheet

/casterrequest <ID> <day> <time> (dms only)
used to request a caster, said caster is then pinged in a designated channel with the info

/flipout
responds with kissy face emoji

/benjamin
responds with benjamin

"""

import json
import discord
import sys
import datetime
import re
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

if len(sys.argv) == 1:

    with open('ids.json') as f:
        ids = json.load(f)

    @bot.event
    async def on_ready():
        print(f"{bot.user} is online")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Skyward Series"))

    @bot.slash_command(name="ping", description="Sends the bot's latency.")
    async def ping(ctx):
        await ctx.respond(f"Pong! Latency is {str(1000.0*bot.latency)[:5]}ms.")

    @bot.slash_command(name="flipout", description="flipout")
    async def flipout(ctx):
        await ctx.respond("flipout :kissing_heart:")

    @bot.slash_command(name="benjamin", description="benjamin")
    async def benjamin(ctx):
        await ctx.respond("benjamin :flushed:")

    @bot.slash_command(name="dm", description="Sends a message in dms to everyone with the pinged role.")
    async def dm(ctx, role: discord.Role, message: str):
        if ctx.author.guild_permissions.administrator:
            await ctx.respond(f"Sending message to all members with role **\"{role}\"** (ID: {role.id})...")
            # send message to all members with role
            for member in role.members:
                await member.send(f"**{ctx.author}** says:\n{message}")
            await ctx.send("Sent.")
        else:
            await ctx.respond("You must be an administrator to use this command.")
            today = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
            with open("log.txt", "w+") as logf:
                logf.write(f"[{today}] {ctx.author} attempted to use /dm on role \"{role}\" with message \"{message}\"")
            print(f"[{today}] {ctx.author} attempted to use /dm on role \"{role}\" with message \"{message}\"")

    @bot.slash_command(name="casterinfo", description="Sends a list of caster availability.")
    async def casterinfo(ctx):
        if ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664:
            await ctx.respond(embed=discord.Embed(
                color=0x429B97,
                title="Caster Info",
                description="<:dot:1031708752140832768> You can see caster availability [here!](https://docs.google.com/spreadsheets/d/1YfXo1ehAI8GDIiwG6dI09_In2VbxX7TjwBLA0Lgs430/edit?usp=sharing)"
            ))
        else:
            await ctx.respond("This is a DMs-only command.")

    @bot.slash_command(name="report", description="Used to report match, sends the info to a designated channel.", options=[
        discord.Option(name="week", description="Week of the match", type=int, required=True),
        discord.Option(name="team_one_tag", description="Tag of the first team", type=str, required=True),
        discord.Option(name="score", description="Score of the match", type=str, required=True),
        discord.Option(name="team_two_tag", description="Tag of the second team", type=str, required=True)
    ])
    async def report(ctx, week, team_one_tag, score, team_two_tag):
        if ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664:
            try: int(week)
            except: await ctx.respond(f"**Error** in parameter **week**, given '{week}'\nWeek must be a number."); return

            try: int(score.split("-")[0])
            except: await ctx.respond(f"**Error** in parameter **score**, given '{score}'\nScore must be in the format `a-b` where `a` and `b` are both numbers."); return
            
            temp = [int(i) for i in score.split("-")]

            if temp[0] > temp[1]:
                who_won = f"**{team_one_tag}** won against **{team_two_tag}**"
            elif temp[0] < temp[1]:
                who_won = f"**{team_one_tag}** lost to **{team_two_tag}**"
            else:
                who_won = f"**{team_one_tag}** and **{team_two_tag}** tied"

            await bot.get_channel(1025198171435049032).send(("<@&1022316227131080797>" if PINGHELPERS else ""), embed=discord.Embed(
                color=0x429B97,
                title=f"{team_one_tag} vs. {team_two_tag} - Reported Match",
                description=f"**Week {week}**\n{who_won} with a score of **{score}**"
            ).set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.display_avatar
            ))
            await ctx.respond("Report sent.")
        else:
            await ctx.respond("This is a DMs-only command.")

    @bot.slash_command(name="requestcaster", description="Used to request a caster, said caster is then pinged in a designated channel with the info.", options=[
                        discord.Option(name="day", description="Day of the match", type=str),
                        discord.Option(name="time", description="Time of the match (THIS MUST BE IN EST)", type=str),
    ])
    async def requestcaster(ctx, day, time):
        if ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664:
            # check if day in MM/DD format using regex
            if not re.match(r"^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$", day):
                await ctx.respond(f"**Error** in parameter **day**, given '{day}'\nDay must be a valid day, and in the format `MM/DD`")
                return
            await ctx.respond(
                embed=discord.Embed(
                    description="**PLEASE CHECK CASTER SCHEDULES WITH /casterinfo BEFORE REQUESTING A CASTER**\n" + \
                    "Respond 'yes' to confirm you've checked the schedule."
                )
            )
            try:
                msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=20)
            except asyncio.TimeoutError:
                await ctx.respond("Confirmation timed out after 20 seconds, please try again.")
                return
            if msg.content.lower() != "yes":
                await msg.respond("Confirmation failed, please try again.")
                return
            await ctx.send(
                "Please enter the number corresponding to the caster you would like to request:\n",
                embed=discord.Embed(
                    color=0x429B97,
                    title="Caster Request Numbers",
                    description="\n".join([f"{i+1}. {caster}" for i, caster in enumerate(ids)])
                )
            )
            try:
                msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=20)
            except asyncio.TimeoutError:
                await ctx.respond("Request timed out after 20 seconds, please try again.")
                return
            if msg.content == "joner":
                await bot.get_channel(1025196891794853888).send(f"<@{ctx.author.id}>\nYou can't request joner, he's not a caster. But this test works, so that's good.\nparameters: `{day}`, `{time}`")
                return
            await bot.get_channel(1025196891794853888).send(
                f"<@{[i for i in ids.values()][int(msg.content)-1]}>",
                embed=discord.Embed(
                    title="Caster Request",
                    description=f"\n{ctx.author} has requested a caster for **{day}** at **{time}**"
                )
            )
            await ctx.respond("Caster request sent.")
        else:
            await ctx.respond("This is a DMs-only command.")

else:

    @bot.event
    async def on_ready():
        print(f"{bot.user} is online")
        await bot.change_presence(activity=discord.Game(name="with code [Under Maintenance]"))
    
    @bot.slash_command(name="ping", description="Sends the bot's latency.")
    async def ping(ctx):
        await ctx.respond(f"Pong! Latency is {str(1000.0*bot.latency)[:5]}ms.")

    @bot.slash_command(name="flipout", description="flipout")
    async def flipout(ctx):
        await ctx.respond("flipout :kissing_heart:")

    @bot.slash_command(name="benjamin", description="benjamin")
    async def benjamin(ctx):
        await ctx.respond("benjamin :flushed:")

    @bot.slash_command(name="dm", description="Sends a message in dms to everyone with the pinged role.")
    async def dm(ctx, role: discord.Role, message: str):
        await ctx.respond("SkywardBot is currently under maintenance, please try again later.")

    @bot.slash_command(name="casterinfo", description="Sends a list of caster availability.")
    async def casterinfo(ctx):
        await ctx.respond("SkywardBot is currently under maintenance, please try again later.")

    @bot.slash_command(name="report", description="Used to report match, sends the info to a designated channel.", options=[
        discord.Option(name="week", description="Week of the match", type=int, required=True),
        discord.Option(name="team_one_tag", description="Tag of the first team", type=str, required=True),
        discord.Option(name="score", description="Score of the match", type=str, required=True),
        discord.Option(name="team_two_tag", description="Tag of the second team", type=str, required=True)
    ])
    async def report(ctx, week, team_one_tag, score, team_two_tag):
        await ctx.respond("SkywardBot is currently under maintenance, please try again later.")

    @bot.slash_command(name="requestcaster", description="Used to request a caster, said caster is then pinged in a designated channel with the info.", options=[
                        discord.Option(name="day", description="Day of the match", type=str),
                        discord.Option(name="time", description="Time of the match (THIS MUST BE IN EST)", type=str),
    ])
    async def requestcaster(ctx, day, time):
        await ctx.respond("SkywardBot is currently under maintenance, please try again later.")

try:
    open("token.txt").close()
except FileNotFoundError:
    token = input("Enter token: ")
else:
    with open("token.txt") as f:
        token = f.read()

bot.run(token)