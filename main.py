import discord #py-cord, not discord.py
import traceback, sys
from discord.ext import commands
from datetime import datetime
from random import randint
from table2ascii import table2ascii as t2a, PresetStyle

LOG="""Last updated: July 14, 2023
- `/report` checks for valid week number or playoff abbreviation
- No longer says "The application did not respond" when submitting a report
- `team_tag` changed to `team_name`
- cooldowns for most general usage commands
As always, check `/source` to see the most recent commits!
"""

NORATIO_CHANNELS = [
    1022240859598618667,
    1028759095802613821,
    1054580545067155516,
    991656468258508840,
    1087840813091917916,
    1084898882804252712,
    1072274227471859712,
    991020848766926949,
    1055651522966474814,
    991645524837027870,
    1022883762356363345,
    1095863844347334707,
    1054572208258830416,
    991642137512906822,
    1084244657623535726,
    1021998533806661722,
    1023710972134838402,
    1104574435895296000,
    1034667026385489932
]
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
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f'Slow down! Use this command again in **{round(error.retry_after,1)}s.**', ephemeral=True)
    else:
        description = error.__class__.__name__ + ': ' + str(error)
        await ctx.respond('Something went wrong. The error has been reported to the developers.\n`{error}`', ephemeral=True)
        await bot.get_user(JONER).send(embed=discord.Embed(
            title="SkywardBot - Uncaught Exception",
            description=description+f'\nUser: {ctx.author}\nCommand: {ctx.envoked_with}\n'+''.join(traceback.StackSummary.extract(traceback.walk_stack(None)).format()),
            color=0xFF0000
            )
        )

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
    elif ctx.content.startswith('!!!dm'):
        if ctx.content.split()[1] in USERALISES:
            user = bot.get_user(USERALISES[ctx.content.split()[1]])
        else:
            user = bot.get_user(int(ctx.content.split()[1]))
        await user.send(' '.join(ctx.content.split()[2:]))
        await ctx.channel.send(f"Sent: {ctx.content.split()[1]} - {' '.join(ctx.content.split()[2:])}")
    elif isinstance(ctx.channel, discord.DMChannel):
        channel = bot.get_channel(1130487355426492446)
        await channel.send(f"From: {ctx.author.name} ({ctx.author.id}) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nMessage: {ctx.content}")
    if "ratio" in ctx.content.lower() and ctx.channel.id not in NORATIO_CHANNELS:
        if randint(0, 1):
            await ctx.add_reaction("⬆️")
        else:
            await ctx.add_reaction("⬇️")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1031781423864090664)
    await channel.send(f":white_check_mark: {member.name} ({member.id}) joined at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1031781423864090664)
    await channel.send(f":no_entry_sign: {member.name} ({member.id}) left at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@commands.cooldown(1, 30, commands.BucketType.channel)
@bot.slash_command(name="help", description="Show list of commands.")
async def help(ctx):
    await ctx.respond(embed=discord.Embed(title="SkywardBot - Help", description="""**Admin-Only**
`/dm <role> <message>` - Sends a message in dms to everyone with the pinged role.

**Casters** (DMs only)
`/casterinfo` - Get a list of casters and their availability through UNU.

**Match Reporting** (Captains and DMs only)
`/report <league> <gamemode> <week> <team1> <score-score> <team2> [ballchasing]` - Report a match.
`/forfeit <league> <gamemode> <week> <team1> <team2> <type>` - Report a forfeit.

**Misc**
`/flipout` - flipout
`/benjamin` - benjamin
`/ping` - Check bot latency (my wifi is fine).

**Bot**
`/help` - Show this message.
`/log` - See recent changes to SkywardBot.
`/source` - Get a link to the GitHub source code for SkywardBot.
`/bug <anonymous> <message>` - Report a bug (or funny meme) to joner himself.
`/suggest <anonymous> <message>` - Suggest a few feature or improvement.

Admins can use any command regardless of role exclusivity.""", color=0xFF9179))

@commands.cooldown(1, 30, commands.BucketType.channel)
@bot.slash_command(name="ping", description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(embed=discord.Embed(
        title="Pong!",
        description=f"Pong! Latency is {str(1000.0*bot.latency)[:5]}ms.",
        color=0xFF9179
    ))

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.slash_command(name="flipout", description="flipout")
async def flipout(ctx):
    await ctx.respond("flipout :kissing_heart:")

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.slash_command(name="benjamin", description="benjamin")
async def benjamin(ctx):
    await ctx.respond("benjamin :flushed:")

@commands.cooldown(1, 30, commands.BucketType.channel)
@bot.slash_command(name="source", description="Get a link to the GitHub source code for SkywardBot.")
async def source(ctx):
    await ctx.respond(embed=discord.Embed(title="SkywardBot - Source Code", description="You can view the source code of SkywardBot here:\nhttp://github.com/jonahbebko/SkywardBot", color=0xFF9179))

@commands.cooldown(1, 30, commands.BucketType.channel)
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

@commands.cooldown(1, 30, commands.BucketType.channel)
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
    discord.Option(name="team_one", description="Tag of the first team", required=True),
    discord.Option(name="score", description="Score of the match", required=True),
    discord.Option(name="team_two", description="Tag of the second team", required=True),
    discord.Option(name="ballchasing", description="Ballchasing link (optional)", required=False)
])
async def report(ctx, league, gamemode, week, team_one, score, team_two, ballchasing=None):

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

    try:
        int(week)
    except:
        if week not in ["WC", "QF", "SF", "GF"]:
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
        who_won = f"**{team_one}** won against **{team_two}**"
    elif temp[0] < temp[1]:
        who_won = f"**{team_one}** lost to **{team_two}**"
    else:
        who_won = f"**{team_one}** and **{team_two}** tied"

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
                "Or, upload images! All images must be in ONE message and can be either links or attachments.",
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
    
    else:

        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Info",
            description="Report sent.",
            color=0xFF9179
        ))
    
    await bot.get_channel(CHANNELS[league]).send(embed=discord.Embed(
        color=0xFF9179,
        title=f"{team_one} vs. {team_two} - Reported Match",
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
    discord.Option(name="team_one", description="Name of the first team (if single FF, this is the FFing team)",required=True),
    discord.Option(name="team_two", description="Name of the second team", required=True),
    discord.Option(name="fftype", description="Type of forfeit", required=True, choices=[
        discord.OptionChoice(name="Single Forfeit", value="single"),
        discord.OptionChoice(name="Double Forfeit", value="double")
    ])
])
async def forfeit(ctx, league, gamemode, week, team_one, team_two, fftype):

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

    try:
        int(week)
    except:
        if week not in ["WC", "QF", "SF", "GF"]:
            await ctx.respond(embed=discord.Embed(
                title="SkywardBot - Error",
                description=f"**Error** in parameter `week`, given '{week}'\nWeek must be a number or valid playoff abbreviation.",
                color=0xFF0000
            )); return
    
    if fftype == "single":
        await bot.get_channel(CHANNELS[league]).send(embed=discord.Embed(
            color=0xFF0000,
            title=f"{team_one} vs. {team_two} - Reported Single Forfeit",
            description=f"**{gamemode} {league.capitalize()} League - Week {week}**\n**{team_one}** FF'd against **{team_two}**"
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ))
    
    elif fftype == "double":
        await bot.get_channel(CHANNELS[league]).send(embed=discord.Embed(
            color=0xFF0000,
            title=f"{team_one} vs. {team_two} - Reported Double Forfeit",
            description=f"**{gamemode} {league} League - Week {week}**\n**{team_one}** and **{team_two}** double FF'd"
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
