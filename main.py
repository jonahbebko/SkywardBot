import discord #py-cord, not discord.py
from datetime import datetime
from random import randint
from table2ascii import table2ascii as t2a, PresetStyle

LOG="""Last updated: June 28, 2023
- `/report` now checks a few things regarding matches before sending report
As always, check `/source` to see the most recent commits!
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
CHANNELS = {
    "premier": 1097335256287289374,
    "all-star": 1097335302609195048,
    "challenger": 1097335280186433647,
    "prospect": 1025198171435049032,
    "OLD": 1025198171435049032
}
JONER = 424181104598056960

intents = discord.Intents.default()
intents.presences = True
intents.message_content = True
intents.members = True

bot = discord.Bot(intents=intents)

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
    if "ratio" in ctx.content.lower():
        if randint(0, 1):
            await ctx.add_reaction("⬆️")
        else:
            await ctx.add_reaction("⬇️")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1031781423864090664)
    await channel.send(f"{member} joined at {str(datetime.now())[:19]}")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1031781423864090664)
    await channel.send(f"{member} left at {datetime.now()[:19]}")

@bot.slash_command(name="help", description="Show list of commands.")
async def help(ctx):
    await ctx.respond(embed=discord.Embed(title="SkywardBot - Help", description="""**Admin-Only**
`/dm <role> <message>` - Sends a message in dms to everyone with the pinged role.

**Casters** (DMs only)
`/casterinfo` - Get a list of casters and their availability through UNU.

**Match Reporting** (Captains and DMs only)
`/report <league> <gamemode> <week> <ID> <score-score> <ID> [ballchasing]` - Report a match.
`/forfeit <league> <gamemode> <week> <ID> <ID> <type>` - Report a forfeit.

**Misc**
`/flipout` - flipout
`/benjamin` - benjamin
`/cxrrxnt` - cxrrxnt
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
    discord.Option(name="anon", description="Whether to anonymously report your bug. (username and UID will be hidden)", choices=[
        "anonymous",
        "not anonymous"
    ], required=True),
    discord.Option(name="message", description="The bug you encountered.", required=True)
])
async def bug(ctx, anon, message):
    await ctx.respond("Bug reported! Thanks for your help.")
    if anon == "anonymous":
        desc = f"**User:** {ctx.author} ({ctx.author.id})\n**Message:** {message}"
    else:
        desc = f"*Anonymous report.*\n**Message:** {message}"
    await bot.get_user(JONER).send(embed=discord.Embed(
        title="SkywardBot - Bug Report",
        description=desc,
        color=0xFF0000
        )
    )

@bot.slash_command(name="suggest", description="Suggest a new feature or improvement.", options=[
    discord.Option(name="anon", description="Whether to anonymously send your suggestion. (username and UID will be hidden)", choices=[
        "anonymous",
        "not anonymous"
    ], required=True),
    discord.Option(name="message", description="The suggestion you want to provide.", required=True)
])
async def suggest(ctx, anon, message):
    await ctx.respond("Suggestion sent! Thanks for your help.")
    if anon == "anonymous":
        desc = f"**User:** {ctx.author} ({ctx.author.id})\n**Message:** {message}"
    else:
        desc = f"*Anonymous report.*\n**Message:** {message}"
    await bot.get_user(JONER).send(embed=discord.Embed(
        title="SkywardBot - Suggestion",
        description=desc,
        color=0xFF9179
        )
    )

@bot.slash_command(name="dm", description="Sends a message in dms to everyone with the pinged role.", options=[
    discord.Option(name="anon", description="Whether to send the message anonymously.", choices=[
        "anonymous",
        "not anonymous"
    ], required=True),
    discord.Option(name="role", description="The ID of the role to send the message to.", type=int, required=True),
    discord.Option(name="message", description="The message to send.", required=True)
])
async def dm(ctx, anon, role, message):
    if ctx.author.guild_permissions.administrator:
        await ctx.respond(f"Anonymity: {anon}\nSending **\"{message}\"** to all members with role ID **{role}**...")
        if anon == "anonymous": a = "Anonymous"
        else: a = ctx.author
        # send message to all members with role
        for member in ctx.guild.members:
            if int(role) in [r.id for r in member.roles]:
                await member.send(embed=discord.Embed(
                    title="SkywardBot - Message",
                    description=f"**{a}** says:\n{message}",
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
            description="<:dot:1031708752140832768> You can see UNU caster availability [here!](https://urnextup.gg)"
        ))
    else:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="This is a DMs-only command.",
            color=0xFF0000
        )); return

@bot.slash_command(name="report", description="Used to report match, sends the info to a designated channel", options=[
    discord.Option(name="league", description="League played.", choices=[
        discord.OptionChoice(name="Premier", value="premier"),
        discord.OptionChoice(name="All-Star", value="all-star"),
        discord.OptionChoice(name="Challenger", value="challenger"),
        discord.OptionChoice(name="Prospect", value="prospect"),
    ], required=True),
    discord.Option(name="gamemode", description="2v2 or 3v3 gamemode", choices=[
        discord.OptionChoice(name="2v2", value="2v2"),
        discord.OptionChoice(name="3v3", value="3v3")
    ], required=True),
    discord.Option(name="week", description="Week of the match", required=True),
    discord.Option(name="team_one_tag", description="Tag of the first team", required=True),
    discord.Option(name="score", description="Score of the match", required=True),
    discord.Option(name="team_two_tag", description="Tag of the second team", required=True),
    discord.Option(name="ballchasing", description="Ballchasing link (optional)", required=False)
])
async def report(ctx, league, gamemode, week, team_one_tag, score, team_two_tag, ballchasing=None):

    if not (ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664):
        await ctx.respond("This is a DMs-only command."); return
    
    if league.lower() not in ["premier", "all-star", "challenger", "prospect"]:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `league`, given '{league}'\n" + \
                "League must be one of the following: `premier`, `all-star`, `challenger`, `prospect`",
            color=0xFF0000
        )); return

    if gamemode not in ["2v2", "3v3"]:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `gamemode`, given '{gamemode}'\n" + \
                "Gamemode must be one of the following: `2v2`, `3v3`",
            color=0xFF0000
        )); return

    if (isinstance(week, int)) and (week not in ["WC", "QF", "SF", "GF"]):
        await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Error",
        description=f"**Error** in parameter `week`, given '{week}'\nWeek must be a number or valid playoff abbreviation.",
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

    if ("ballchasing.com/" not in str(ballchasing)) and (ballchasing != None):
        await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Error",
        description=f"Ballchasing link must be valid and point to a replay.",
        color=0xFF0000
    )); return

    output = ""

    if not ballchasing:

        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Stats (beta)",
            description="Since no ballchasing link was provided, you must enter player stats manually.\n" + \
                "Please enter comma-separated values for statistics, one line for each player.\n\n" + \
                "Your message should be in this format:\n```player1,score,shots,goals,assists,saves\nplayer2,score,shots,goals,assists,saves\n...```\n" + \
                "Or, upload images!",
            color=0xFF9179
        ))

        stats: list = []

        message = await bot.wait_for(
            "message",
            check=lambda x: x.channel.id == ctx.channel.id and ctx.author.id == x.author.id,
            timeout=None
            )
        
        if message.attachments:
            output += "\n".join([i.url for i in message.attachments])
        elif "https://" in message.content or "http://" in message.content:
            output += message.content

        if output:
            if len(output.split("\n")) != sum([int(i) for i in score.split("-")]):
                numAttachments = len(output.split("\n"))
                numGames = sum([int(i) for i in score.split('-')])
                await ctx.respond(embed=discord.Embed(
                    title="SkywardBot - Error",
                    description=f"Number of attachments does not equal number of games played.\nattachments ({numAttachments}) doesn't match games ({numGames})",
                    color=0xFF9179
                ))
                return
        else:
            for entry in message.content.split("\n"):
                stats.append([i.replace(" ", "").replace("\n", "") for i in entry.split(",")])
            
            if len(stats)/2 != int(gamemode[0]):
                await ctx.respond(embed=discord.Embed(
                    title="SkywardBot - Error",
                    description=f"Number of players entered does not match gamemode.\nexpected players ({int(gamemode[0])*2}) doesn't match entries ({len(stats)})",
                    color=0xFF9179
                ))
                return

            output = t2a(
                header=["Player", "Score", "Shots", "Goals", "Shooting %", "Assists", "Saves"],
                body=[
                    [i[0], i[1], i[2], i[3],
                    ((str(round(int(i[3])/int(i[2]), 4)*100)[:5]) if (i[2] != "0") else "0")+"%", # check for div by 0
                    i[4], i[5]] for i in stats
                ],
                first_col_heading=True
            )

    await ctx.send(embed=discord.Embed(
        title="SkywardBot - Info",
        description="Report sent.",
        color=0xFF9179
    ))
    
    await bot.get_channel(CHANNELS[league]).send(embed=discord.Embed(
        color=0xFF9179,
        title=f"{team_one_tag} vs. {team_two_tag} - Reported Match",
        description=f"**{gamemode} {league.capitalize()} League - Week {week}**\n{who_won} with a score of **{score}**" \
            + (f"\n[**Ballchasing link**]({ballchasing})" if ballchasing else "")
    ).set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.display_avatar
    ))
    if output: await bot.get_channel(CHANNELS[league]).send(f"```\n{output}\n```" if "https://" not in output else f"\n{output}\n")

@bot.slash_command(name="forfeit", description="Used to report a forfeit, sends the info to a designated channel.", options=[
    discord.Option(name="league", description="League played.", choices=[
        discord.OptionChoice(name="Premier", value="premier"),
        discord.OptionChoice(name="All-Star", value="all-star"),
        discord.OptionChoice(name="Challenger", value="challenger"),
        discord.OptionChoice(name="Prospect", value="prospect"),
    ], required=True),
    discord.Option(name="gamemode", description="2v2 or 3v3 gamemode", choices=[
        discord.OptionChoice(name="2v2", value="2v2"),
        discord.OptionChoice(name="3v3", value="3v3")
    ], required=True),
    discord.Option(name="week", description="Week of the match (set to 0 for playoffs)", required=True),
    discord.Option(name="team_one_tag", description="Tag of the first team (if single FF, this is the FFing team)",required=True),
    discord.Option(name="team_two_tag", description="Tag of the second team", required=True),
    discord.Option(name="fftype", description="Type of forfeit", required=True, choices=[
        discord.OptionChoice(name="Single Forfeit", value="single"),
        discord.OptionChoice(name="Double Forfeit", value="double")
    ])
])
async def forfeit(ctx, league, gamemode, week, team_one_tag, team_two_tag, fftype):

    if not (ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664):
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="This is a DMs-only command.",
            color=0xFF0000
        )); return

    if league.lower() not in ["premier", "all-star", "challenger", "prospect"]:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `league`, given '{league}'\n" + \
                "League must be one of the following: `premier`, `all-star`, `challenger`, `prospect`",
            color=0xFF0000
        )); return

    if gamemode not in ["2v2", "3v3"]:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `gamemode`, given '{gamemode}'\n" + \
                "Gamemode must be one of the following: `2v2`, `3v3`",
            color=0xFF0000
        )); return

    if (isinstance(week, int)) and (week not in ["WC", "QF", "SF", "GF"]):
        await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Error",
        description=f"**Error** in parameter `week`, given '{week}'\nWeek must be a number or valid playoff abbreviation.",
        color=0xFF0000
    )); return
    
    if fftype == "single":
        await bot.get_channel(CHANNELS[league]).send(embed=discord.Embed(
            color=0xFF0000,
            title=f"{team_one_tag} vs. {team_two_tag} - Reported Single Forfeit",
            description=f"**{gamemode} {league.capitalize()} League - Week {week}**\n**{team_one_tag}** FF'd against **{team_two_tag}**"
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ))
    
    elif fftype == "double":
        await bot.get_channel(CHANNELS[league]).send(embed=discord.Embed(
            color=0xFF0000,
            title=f"{team_one_tag} vs. {team_two_tag} - Reported Double Forfeit",
            description=f"**{gamemode} {league} League - Week {week}**\n**{team_one_tag}** and **{team_two_tag}** double FF'd"
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ))
    
    else:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `type`, given '{fftype}'\nType must be either 'single' or 'double'.",
            color=0xFF0000
        )); return

    await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Info",
        description="Report sent.",
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
