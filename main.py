# ping helpers?
PINGHELPERS = False

"""

LIST OF COMMANDS:

/banlist
list of banned users (admin only)

/ban <id/user/group/message> [reason]
add user to ban list (admin only)

/dm <role> <message> (admin only)
sends a message in dms to everyone with the pinged role

/casterinfo (dms only)
sends a list of caster availability set by /setcasterinfo

/report <week> <ID> <score-score> <ID> (dms only)
used to report match, sends the info to a designated channel or gsheet

/forfeit <week> <ID> <ID> <type> (dms only)
used to report forfeit, sends the info to a designated channel or gsheet

/requestcaster <day> <time> (dms only)
used to request a caster, said caster is then pinged in a designated channel with the info

/flipout
responds with kissy face emoji

/benjamin
responds with benjamin

!!!send <channel ID> <message>
secret send command

"""

import json
import discord
import sys
import datetime
import re
import asyncio

ROLES = {
    "captain": 991634383482138714,
    "orgrep": 1021998653612769280,
    "caster": 991651438344282192,
    "activecaster": 1031270343085654107,
    "helper": 1022316227131080797,
    "moderator": 1031270343085654107,
    "admin": 991633204874326136,
    "dev": 1044024355052589146
}
USERALISES = {
    "andrew": 608263238161006592,
    "flip": 348915482356744197,
    "ben": 902657099253825646
}

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

def countdms(bruh):
    # open funny.txt and write to second line
    with open("funny.txt", "r+") as f:
        num = int(f.read())
        if not bruh:
            f.seek(0)
            f.write(str(num+1))
        else:
            return num

def zero():
    with open("funny.txt", "w") as f:
        f.write("0")

with open('ids.json') as f:
    ids = json.load(f)

@bot.event
async def on_ready():
    print(f"{bot.user} is online")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Skyward Series"))

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    if ctx.content.startswith('!!!send'):
        channel = bot.get_channel(int(ctx.content.split()[1]))
        await channel.send(' '.join(ctx.content.split()[2:]))
        await ctx.channel.send(f"Sent: {ctx.content.split()[1]} - {' '.join(ctx.content.split()[2:])}")
    if ctx.content.startswith('!!!dm'):
        if ctx.content.split()[1] in USERALISES:
            user = bot.get_user(USERALISES[ctx.content.split()[1]])
        else:
            user = bot.get_user(int(ctx.content.split()[1]))
        await user.send(' '.join(ctx.content.split()[2:]))
        await ctx.channel.send(f"Sent: {ctx.content.split()[1]} - {' '.join(ctx.content.split()[2:])}")

@bot.slash_command(name="banlist", description="List of banned users (admin only)")
async def banlist(ctx):
    if ctx.author.guild_permissions.administrator:
        with open("bans.txt", "r") as f:
            banl = []
            for line in f.read():
                banl.append(line)
            await ctx.respond(embed=discord.Embed(
                title="Banned Users/Groups",
                color=0xFF0000,
                description=[i for i in banl]
            ))
    else:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="You must be an administrator to use this command.",
            color=0xFF0000
            )
        )

@bot.slash_command(name="ban", description="Add user to ban list (admin only)", options=[
    discord.Option(name="msg", description="ID/group to ban, or a message", required=True, type=str),
    discord.Option(name="reason", description="Reason for ban", required=False, type=str)
])
async def ban(ctx, msg, reason:None):
    if ctx.author.guild_permissions.administrator:
        with open("bans.txt", "a") as f:
            if reason:
                f.write(f"{msg} - {reason}")
            else:
                f.write(f"{msg}")
        await ctx.respond(f"Banned **{msg}** for **{reason}**")
    else:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="You must be an administrator to use this command.",
            color=0xFF0000
            )
        )

@bot.slash_command(name="count", description="Number of funni messages")
async def count(ctx):
    yuh = countdms(True)
    await ctx.respond(f"Number of funni messages: {yuh}")

@bot.slash_command(name="help", description="Show list of commands.")
async def help(ctx):
    await ctx.respond(embed=discord.Embed(title="SkywardBot - Help", description="""**Admin-Only**
`/dm <role> <message>` - Sends a message in dms to everyone with the pinged role.
`/banlist` - List of banned users/groups.
`/ban <id/user/group> [reason]` - Add user/group to ban list.

**Casters** (DMs only)
`/casterinfo` - Get a list of casters and their availability.
`/requestcaster <ID> <day> <time>` - Request a caster for a match.

**Match Reporting** (Captains and DMs only)
`/report <week> <ID> <score-score> <ID>` - Report a match.
`/forfeit <week> <ID> <ID> <type>` - Report a forfeit.

**Misc**
`/flipout` - flipout
`/benjamin` - benjamin
`/ping` - Check bot latency (my wifi is fine).

**Bot**
`/log` - See recent changes to SkywardBot.
`/reportbug <message>` - Report a bug (or funny meme) to joner himself.

Admins can use any command regardless of role exclusivity.""", color=0x429B97))

@bot.slash_command(name="ping", description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(embed=discord.Embed(
        title="Pong!",
        description=f"Pong! Latency is {str(1000.0*bot.latency)[:5]}ms.",
        color=0x429B97
    ))

@bot.slash_command(name="flipout", description="flipout")
async def flipout(ctx):
    await ctx.respond("flipout :kissing_heart:")

@bot.slash_command(name="benjamin", description="benjamin")
async def benjamin(ctx):
    await ctx.respond("benjamin :flushed:")

@bot.slash_command(name="log", description="See the recent updates for SkywardBot.")
async def log(ctx):
    await ctx.respond(embed=discord.Embed(title="SkywardBot - Log", description="""Last updated: 2022-11-20
- Added `/log`, `/reportbug`, `/forfeit`, and `/help` commands.
- Almost every message is now in a shiny-looking embed.""", color=0x429B97))

@bot.slash_command(name="reportbug", description="Report a bug to joner himself.")
async def reportbug(ctx, message: str):
    await ctx.respond("Bug reported! Thanks for your help.")
    server = bot.get_guild(991005374314328124)
    # loop through all members in server with ROLES["dev"] role
    for member in server.members:
        if ROLES["dev"] in [role.id for role in member.roles]:
            await member.send(embed=discord.Embed(
                title="SkywardBot - Bug Report",
                description=f"**User:** {ctx.author} ({ctx.author.id})\n**Message:** {message}",
                color=0x429B97
                )
            )

@bot.slash_command(name="dm", description="Sends a message in dms to everyone with the pinged role.")
async def dm(ctx, role: discord.Role, message: str):
    if ctx.author.guild_permissions.administrator:
        await ctx.respond(f"Sending message to all members with role **\"{role}\"** (ID: {role.id})...")
        # send message to all members with role
        for member in role.members:
            await member.send(embed=discord.Embed(
                title="SkywardBot - Message",
                description=f"**{ctx.author}** says:\n{message}",
                color=0x429B97
                )
            )
        await ctx.send("Sent.")
    else:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="You must be an administrator to use this command.",
            color=0xFF0000
            )
        )
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
        countdms()
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="This is a DMs-only command.",
            color=0xFF0000
        )); return

@bot.slash_command(name="report", description="Used to report match, sends the info to a designated channel.", options=[
    discord.Option(name="week", description="Week of the match", type=int, required=True),
    discord.Option(name="team_one_tag", description="Tag of the first team", type=str, required=True),
    discord.Option(name="score", description="Score of the match", type=str, required=True),
    discord.Option(name="team_two_tag", description="Tag of the second team", type=str, required=True)
])
async def report(ctx, week, team_one_tag, score, team_two_tag):

    if not (ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664):
        await ctx.respond("This is a DMs-only command."); return

    try: int(week)
    except: await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Error",
        description=f"**Error** in parameter **week**, given '{week}'\nWeek must be a number.",
        color=0xFF0000
    )); return

    try: int(score.split("-")[0])
    except: await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Error",
        description=f"**Error** in parameter **score**, given '{score}'\nScore must be in the format `a-b` where `a` and `b` are both numbers.",
        color=0xFF0000
    )); return
    
    temp = [int(i) for i in score.split("-")]

    if temp[0] > temp[1]:
        who_won = f"**{team_one_tag}** won against **{team_two_tag}**"
    elif temp[0] < temp[1]:
        who_won = f"**{team_one_tag}** lost to **{team_two_tag}**"
    else:
        who_won = f"**{team_one_tag}** and **{team_two_tag}** tied"

    await bot.get_channel(1025198171435049032).send((f"<@&{ROLES['helpers']}>" if PINGHELPERS else ""), embed=discord.Embed(
        color=0x429B97,
        title=f"{team_one_tag} vs. {team_two_tag} - Reported Match",
        description=f"**Week {week}**\n{who_won} with a score of **{score}**"
    ).set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.display_avatar
    ))

    await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Info",
        description="Report sent.",
        color=0x429B97
    ))

# make command called "forfeit" like /report
@bot.slash_command(name="forfeit", description="Used to report a forfeit, sends the info to a designated channel.", options=[
    discord.Option(name="week", description="Week of the match", type=int, required=True),
    discord.Option(name="team_one_tag", description="Tag of the first team (if single FF, this is the FFing team)", type=str, required=True),
    discord.Option(name="team_two_tag", description="Tag of the second team", type=str, required=True),
    discord.Option(name="type", description="Type of forfeit - must be 'single' or 'double'", type=str, required=True, options=[
        discord.Option(name="single", description="Single forfeit.", type=str, required=True),
        discord.Option(name="double", description="Double forfeit.", type=str, required=True)
    ])
])
async def forfeit(ctx, week, team_one_tag, team_two_tag, type):

    if not (ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664):
        countdms()
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="This is a DMs-only command.",
            color=0xFF0000
        )); return

    try: int(week)
    except: await ctx.respond(f"**Error** in parameter **week**, given '{week}'\nWeek must be a number."); return

    if type == "single":
        await bot.get_channel(1025198171435049032).send((f"<@&{ROLES['helpers']}>" if PINGHELPERS else ""), embed=discord.Embed(
            color=0xFF0000,
            title=f"{team_one_tag} vs. {team_two_tag} - Reported Single Forfeit",
            description=f"**Week {week}**\n**{team_one_tag}** FF'd against **{team_two_tag}**"
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ))
    
    elif type == "double":
        await bot.get_channel(1025198171435049032).send((f"<@&{ROLES['helpers']}>" if PINGHELPERS else ""), embed=discord.Embed(
            color=0xFF0000,
            title=f"{team_one_tag} vs. {team_two_tag} - Reported Double Forfeit",
            description=f"**Week {week}**\n**{team_one_tag}** and **{team_two_tag}** double FF'd"
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ))
    
    else:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter **type**, given '{type}'\nType must be either 'single' or 'double'.",
            color=0xFF0000
        )); return
    
    await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Info",
        description="Report sent.",
        color=0x429B97
    ))

@bot.slash_command(name="requestcaster", description="Used to request a caster, said caster is then pinged in a designated channel with the info.", options=[
                    discord.Option(name="day", description="Day of the match", type=str),
                    discord.Option(name="time", description="Time of the match (THIS MUST BE IN EST)", type=str),
])
async def requestcaster(ctx, day, time):

    if not (ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664):
        countdms()
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="This is a DMs-only command.",
            color=0xFF0000
        )); return

    # check if day in MM/DD format using regex
    if not re.match(r"^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$", day):
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter **day**, given '{day}'\nDay must be a valid day, and in the format `MM/DD`",
            color=0xFF0000
        )); return
    
    await ctx.respond(
        embed=discord.Embed(
            description="**PLEASE CHECK CASTER SCHEDULES WITH /casterinfo BEFORE REQUESTING A CASTER**\n" + \
            "Respond 'yes' to confirm you've checked the schedule."
        )
    )

    try:
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=20)
    except asyncio.TimeoutError:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="Confirmation timed out after 20 seconds, please try again.",
            color=0xFF0000
        )); return
    
    if msg.content.lower() != "yes":
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="Confirmation failed, please try again.",
            color=0xFF0000
        )); return
    
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
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="Request timed out after 20 seconds, please try again.",
            color=0xFF0000
        )); return
    
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

    await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Info",
        description="Caster request sent.",
        color=0x429B97
    ))

try:
    open("token.txt").close()
except FileNotFoundError:
    token = input("Enter token: ")
else:
    with open("token.txt") as f:
        token = f.read()

bot.run(token)