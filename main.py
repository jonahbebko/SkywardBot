import discord #py-cord, not discord.py
from datetime import datetime

LOG="""Last updated: February 10, 2023
- Changed ballchasers to ballchasing (whoops)
- Fixed lowercase bug in /report and /forfeit
- Added ballchasing link validity check
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

async def error_embed(ctx, e):
    await ctx.respond(embed=discord.Embed(
        title="Error!",
        description="Something went wrong!\nThe error has been logged and DM'd to Jonah.",
        color=0xFF0000
    ))
    server = bot.get_guild(991005374314328124)
    for member in server.members:
        if ROLES["dev"] in [role.id for role in member.roles]:
            await member.send(f"SOMETHING WENT WRONG FUCKFACE\n{e}")

def catch_errors(func):
    async def wrapper(ctx):
        try:
            return await func(ctx)
        except Exception as e:
            print(e)
            await error_embed(ctx, e)
    return wrapper

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

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1031781423864090664)
    await channel.send(f"{member} joined at {datetime.now()}")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1031781423864090664)
    await channel.send(f"{member} left at {datetime.now()}")

@bot.slash_command(name="help", description="Show list of commands.")
async def help(ctx):
    await ctx.respond(embed=discord.Embed(title="SkywardBot - Help", description="""**Admin-Only**
`/dm <role> <message>` - Sends a message in dms to everyone with the pinged role.

**Casters** (DMs only)
`/casterinfo` - Get a list of casters and their availability through UNU.

**Match Reporting** (Captains and DMs only)
`/report <league> <gamemode> <week> <ID> <score-score> <ID> [ballchasing]` - Report a match.
`/forfeit <league> <gamemode> <week> <ID> <ID> <type> [ballchasing]` - Report a forfeit.

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

@bot.slash_command(name="cxrrxnt", description="cxrrxnt")
async def cxrrxnt(ctx):
    await ctx.respond("https://cdn.discordapp.com/attachments/1031781423864090664/1078482799343976489/attachment.png")

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
@catch_errors
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
@catch_errors
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
@catch_errors
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
@catch_errors
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
    discord.Option(name="ballchasing", description="Ballchasing link (optional)", type=str, required=False)
])
@catch_errors
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

    if ("ballchasing.com/" not in str(ballchasing)) and (ballchasing != None):
        await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Error",
        description=f"Ballchasing link must be valid and point to a replay.",
        color=0xFF0000
    )); return

    await bot.get_channel(1025198171435049032).send(embed=discord.Embed(
        color=0xFF9179,
        title=f"{team_one_tag} vs. {team_two_tag} - Reported Match",
        description=f"**{gamemode} {league} League - Week {week}**\n{who_won} with a score of **{score}**" \
            + (f"\n[**Ballchasing link**]({ballchasing})" if ballchasing else "")
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
    discord.Option(name="ballchasing", description="Ballchasing link (optional)", type=str, required=False)
])
@catch_errors
async def forfeit(ctx, league, gamemode, week, team_one_tag, team_two_tag, fftype, ballchasing=None):

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
    league = league.capitalize()

    if gamemode not in ["2v2", "3v3"]:
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"**Error** in parameter `gamemode`, given '{gamemode}'\n" + \
                "Gamemode must be one of the following: `2v2`, `3v3`",
            color=0xFF0000
        )); return

    try: int(week)
    except: await ctx.respond(f"**Error** in parameter `week`, given '{week}'\nWeek must be a number."); return

    if ("ballchasing.com/" not in str(ballchasing)) and (ballchasing != None):
            await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description=f"Ballchasing link must be valid and point to a replay.",
            color=0xFF0000
        )); return

    if fftype == "single":
        await bot.get_channel(1025198171435049032).send(embed=discord.Embed(
            color=0xFF0000,
            title=f"{team_one_tag} vs. {team_two_tag} - Reported Single Forfeit",
            description=f"**Week {week}**\n**{team_one_tag}** FF'd against **{team_two_tag}**" \
                + (f"\n[**Ballchasing link**]({ballchasing})" if ballchasing else "")
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar
        ))
    
    elif fftype == "double":
        await bot.get_channel(1025198171435049032).send(embed=discord.Embed(
            color=0xFF0000,
            title=f"{team_one_tag} vs. {team_two_tag} - Reported Double Forfeit",
            description=f"**{gamemode} {league} League - Week {week}**\n**{team_one_tag}** and **{team_two_tag}** double FF'd" \
                + (f"\n[**Ballchasing link**]({ballchasing})" if ballchasing else "")
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
