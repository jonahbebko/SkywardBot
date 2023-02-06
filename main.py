import json
import discord
import re
import asyncio

LOG="""Last updated: February 5, 2023
- Added optional ballchasers link to /report and /forfeit
- Corrected some colors to Skyward Orange
- Removed unauthorized admin command usage logging because I don't really care
- Fixed a silly goofy error that broke the entire bot sometimes
"""

ROLES = {
    "captain": 991634383482138714,
    "orgrep": 1021998653612769280,
    "caster": 991651438344282192,
    "activecaster": 1031270343085654107,
    "helper": 1022316227131080797,
    "moderator": 1031270343085654107,
    "admin": 991633204874326136,
    "dev": 1062201184095580231
}
USERALISES = {
    "andrew": 608263238161006592,
    "flip": 348915482356744197,
    "ben": 902657099253825646
}

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

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

"""
@bot.slash_command(name="banlist", description="List of banned users (admin only)")
async def banlist(ctx):
    if ctx.author.guild_permissions.administrator:
        with open("bans.txt", "r") as f:
            await ctx.respond(embed=discord.Embed(
                title="Banned Users/Groups",
                color=0xFF0000,
                description=f.read()
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
"""

@bot.slash_command(name="help", description="Show list of commands.")
async def help(ctx):
    await ctx.respond(embed=discord.Embed(title="SkywardBot - Help", description="""**Admin-Only**
`/dm <role> <message>` - Sends a message in dms to everyone with the pinged role.

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
`/source` - Get a link to the GitHub source code for SkywardBot.
`/bug <anonymous> <message>` - Report a bug (or funny meme) to joner himself.
`/suggest <anonymous> <message>` - Suggest a few feature or improvement.

Admins can use any command regardless of role exclusivity.""", color=0xFF9179))

@bot.slash_command(name="ping", description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(embed=discord.Embed(
        title="Pong!",
        description=f"Pong! Latency is {str(1000.0*bot.latency)[:5]}ms.",
        color=0xFF9179
    ))

@bot.slash_command(name="flipout", description="flipout")
async def flipout(ctx):
    await ctx.respond("flipout :kissing_heart:")

@bot.slash_command(name="benjamin", description="benjamin")
async def benjamin(ctx):
    await ctx.respond("benjamin :flushed:")

@bot.slash_command(name="source", description="Get a link to the GitHub source code for SkywardBot.")
async def source(ctx):
    await ctx.respond(embed=discord.Embed(title="SkywardBot - Source Code", description="You can view the source code of SkywardBot here:\nhttp://github.com/jonahbebko/SkywardBot"))

@bot.slash_command(name="log", description="See the recent updates for SkywardBot.")
async def log(ctx):
    await ctx.respond(embed=discord.Embed(title="SkywardBot - Log", description=LOG, color=0xFF9179))

@bot.slash_command(name="bug", description="Report a bug to joner himself.", options=[
    discord.Option(name="anon", description="Whether to anonymously report your bug. (username and UID will be hidden)", type=bool, required=True),
    discord.Option(name="message", description="The bug you encountered.", type=str, required=True)
])
async def bug(ctx, anon, message):
    await ctx.respond("Bug reported! Thanks for your help.")
    server = bot.get_guild(991005374314328124)
    if not anon:
        desc = f"**User:** {ctx.author} ({ctx.author.id})\n**Message:** {message}"
    else:
        desc = f"*Anonymous report.*\n**Message:** {message}"
    for member in server.members:
        if ROLES["dev"] in [role.id for role in member.roles]:
            await member.send(embed=discord.Embed(
                title="SkywardBot - Bug Report",
                description=desc,
                color=0xFF0000
                )
            )

@bot.slash_command(name="suggest", description="Suggest a new feature or improvement.", options=[
    discord.Option(name="anon", description="Whether to anonymously send your suggestion. (username and UID will be hidden)", type=bool, required=True),
    discord.Option(name="message", description="The suggestion you want to provide.", type=str, required=True)
])
async def suggest(ctx, anon, message):
    await ctx.respond("Suggestion sent! Thanks for your help.")
    server = bot.get_guild(991005374314328124)
    if not anon:
        desc = f"**User:** {ctx.author} ({ctx.author.id})\n**Message:** {message}"
    else:
        desc = f"*Anonymous report.*\n**Message:** {message}"
    for member in server.members:
        if ROLES["dev"] in [role.id for role in member.roles]:
            await member.send(embed=discord.Embed(
                title="SkywardBot - Suggestion",
                description=desc,
                color=0xFF9179
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
                color=0xFF9179
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

@bot.slash_command(name="casterinfo", description="Sends a list of caster availability.")
async def casterinfo(ctx):
    if ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664:
        await ctx.respond(embed=discord.Embed(
            color=0xFF9179,
            title="Caster Info",
            description="<:dot:1031708752140832768> You can see caster availability [here!](https://docs.google.com/spreadsheets/d/1YfXo1ehAI8GDIiwG6dI09_In2VbxX7TjwBLA0Lgs430/edit?usp=sharing)"
        ))
    else:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="This is a DMs-only command.",
            color=0xFF0000
        )); return

@bot.slash_command(name="report", description="Used to report match, sends the info to a designated channel.", options=[
    discord.Option(name="league", description="League played.", required=True, options=[
        discord.Option(name="premier", description="Premier league."),
        discord.Option(name="all-star", description="All-star league."),
        discord.Option(name="challenger", description="Challenger league."),
        discord.Option(name="prospect", description="Prospect league.")
    ]),
    discord.Option(name="gamemode", description="2v2 or 3v3 gamemode", required=True, options=[
        discord.Option(name="2v2", description="2v2 gamemode."),
        discord.Option(name="3v3", description="3v3 gamemode.")
    ]),
    discord.Option(name="week", description="Week of the match", type=int, required=True),
    discord.Option(name="team_one_tag", description="Tag of the first team", type=str, required=True),
    discord.Option(name="score", description="Score of the match", type=str, required=True),
    discord.Option(name="team_two_tag", description="Tag of the second team", type=str, required=True),
    discord.Option(name="ballchasers", description="Ballchasers link (optional)", type=str, required=False)
])
async def report(ctx, league, gamemode, week, team_one_tag, score, team_two_tag, ballchasers=None):

    if not (ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664):
        await ctx.respond("This is a DMs-only command."); return
    
    if league not in ["premier", "all-star", "challenger", "prospect"]:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `league`, given '{league}'\n" + \
                "League must be one of the following: `premier`, `all-star`, `challenger`, `prospect`",
            color=0xFF0000
        )); return
    league = league.capitalize()

    if gamemode not in ["2v2", "3v3"]:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `gamemode`, given '{gamemode}'\n" + \
                "Gamemode must be one of the following: `2v2`, `3v3`",
            color=0xFF0000
        )); return

    try: int(week)
    except: await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Error",
        description=f"**Error** in parameter `week`, given '{week}'\nWeek must be a number.",
        color=0xFF0000
    )); return

    try: int(score.split("-")[0])
    except: await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Error",
        description=f"**Error** in parameter `score`, given '{score}'\nScore must be in the format `a-b` where `a` and `b` are both positive integers.",
        color=0xFF0000
    )); return
    
    temp = [int(i) for i in score.split("-")]

    if temp[0] > temp[1]:
        who_won = f"**{team_one_tag}** won against **{team_two_tag}**"
    elif temp[0] < temp[1]:
        who_won = f"**{team_one_tag}** lost to **{team_two_tag}**"
    else:
        who_won = f"**{team_one_tag}** and **{team_two_tag}** tied"

    await bot.get_channel(1025198171435049032).send(embed=discord.Embed(
        color=0xFF9179,
        title=f"{team_one_tag} vs. {team_two_tag} - Reported Match",
        description=f"**{gamemode} {league} League - Week {week}**\n{who_won} with a score of **{score}**" \
            + (f"\n[**Ballchasers link**]({ballchasers})" if ballchasers else "")
    ).set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.display_avatar
    ))

    await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Info",
        description="Report sent.",
        color=0xFF9179
    ))

@bot.slash_command(name="forfeit", description="Used to report a forfeit, sends the info to a designated channel.", options=[
    discord.Option(name="league", description="League played.", required=True, options=[
        discord.Option(name="premier", description="Premier league."),
        discord.Option(name="all-star", description="All-star league."),
        discord.Option(name="challenger", description="Challenger league."),
        discord.Option(name="prospect", description="Prospect league.")
    ]),
    discord.Option(name="gamemode", description="2v2 or 3v3 gamemode", required=True, options=[
        discord.Option(name="2v2", description="2v2 gamemode."),
        discord.Option(name="3v3", description="3v3 gamemode.")
    ]),
    discord.Option(name="week", description="Week of the match", type=int, required=True),
    discord.Option(name="team_one_tag", description="Tag of the first team (if single FF, this is the FFing team)", type=str, required=True),
    discord.Option(name="team_two_tag", description="Tag of the second team", type=str, required=True),
    discord.Option(name="fftype", description="Type of forfeit - must be 'single' or 'double'", required=True, options=[
        discord.Option(name="single", description="Single forfeit."),
        discord.Option(name="double", description="Double forfeit.")
    ]),
    discord.Option(name="ballchasers", description="Ballchasers link (optional)", type=str, required=False)
])
async def forfeit(ctx, league, gamemode, week, team_one_tag, team_two_tag, fftype, ballchasers=None):

    if not (ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664):
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="This is a DMs-only command.",
            color=0xFF0000
        )); return

    if league not in ["premier", "all-star", "challenger", "prospect"]:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `league`, given '{league}'\n" + \
                "League must be one of the following: `premier`, `all-star`, `challenger`, `prospect`",
            color=0xFF0000
        )); return
    league = league.captalize()

    if gamemode not in ["2v2", "3v3"]:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `gamemode`, given '{gamemode}'\n" + \
                "Gamemode must be one of the following: `2v2`, `3v3`",
            color=0xFF0000
        )); return

    try: int(week)
    except: await ctx.respond(f"**Error** in parameter `week`, given '{week}'\nWeek must be a number."); return

    if type == "single":
        await bot.get_channel(1025198171435049032).send(embed=discord.Embed(
            color=0xFF0000,
            title=f"{team_one_tag} vs. {team_two_tag} - Reported Single Forfeit",
            description=f"**Week {week}**\n**{team_one_tag}** FF'd against **{team_two_tag}**" \
                + (f"\n[**Ballchasers link**]({ballchasers})" if ballchasers else "")
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ))
    
    elif type == "double":
        await bot.get_channel(1025198171435049032).send(embed=discord.Embed(
            color=0xFF0000,
            title=f"{team_one_tag} vs. {team_two_tag} - Reported Double Forfeit",
            description=f"**{gamemode} {league} League - Week {week}**\n**{team_one_tag}** and **{team_two_tag}** double FF'd" \
                + (f"\n[**Ballchasers link**]({ballchasers})" if ballchasers else "")
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ))
    
    else:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `type`, given '{type}'\nType must be either 'single' or 'double'.",
            color=0xFF0000
        )); return
    
    await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Info",
        description="Report sent.",
        color=0xFF9179
    ))

@bot.slash_command(name="requestcaster", description="Used to request a caster, said caster is then pinged in a designated channel with the info.", options=[
    discord.Option(name="day", description="Day of the match", type=str),
    discord.Option(name="time", description="Time of the match. MUST BE IN EASTERN TIME.", type=str),
])
async def requestcaster(ctx, day, time):

    if not (ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664):
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="This is a DMs-only command.",
            color=0xFF0000
        )); return

    # check if day in MM/DD format using regex
    if not re.match(r"^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$", day):
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `day`, given '{day}'\nDay must be a valid day, and in the format `MM/DD`",
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
            color=0xFF9179,
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
        color=0xFF9179
    ))

try:
    open("token.txt").close()
except FileNotFoundError:
    token = input("Enter token: ")
else:
    with open("token.txt") as f:
        token = f.read()

bot.run(token)
