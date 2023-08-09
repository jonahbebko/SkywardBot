import discord #py-cord, not discord.py
import traceback, json
from discord.ext import commands
from datetime import datetime
from random import randint
from table2ascii import table2ascii as t2a, PresetStyle

LOG="""Last updated: July 25, 2023
SkywardBot is now deprecated. Feel free to use the other commands for fun!
Run `/report` in DMs to see where to submit reports.
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

json_commands = json.load(open("commands.json", "r"))

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
    print(f"{bot.user} is online in deprecation mode")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Skyward Series"))

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    if ctx.content.startswith('!!!send') and ctx.author.id == JONER:
        channel = bot.get_channel(int(ctx.content.split()[1]))
        await channel.send(' '.join(ctx.content.split()[2:]))
        await ctx.channel.send(f"Sent: {ctx.content.split()[1]} - {' '.join(ctx.content.split()[2:])}")
    elif ctx.content.startswith('!!!dm') and ctx.author.id == JONER:
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
    if ctx.content.startswith(",") and ctx.author.guild_permissions.administrator:
        bruh = ctx.content.split(" ")
        if len(bruh) == 1 and bruh[0][1:] in ["add", "delete", "edit"]:
            await ctx.channel.send(f"{'Three' if bruh[0][1:] == 'add' else 'Two'} arguments required."); return
        if len(bruh) != 1 and bruh[1][1:] in ["add", "delete", "edit", "list"]:
            await ctx.channel.send("pls don't do that :("); return
        match bruh[0]:
            case ",add":
                if bruh[1] in json_commands:
                    await ctx.channel.send("Command already exists.")
                else:
                    json_commands[ctx.content.split(" ")[1]] = " ".join(bruh[2:]).replace("\"", "\'")
                    await ctx.channel.send("Command added.")
            case ",delete":
                if bruh[1] in json_commands:
                    del json_commands[bruh[1]]
                    await ctx.channel.send("Command deleted.")
                else:
                    await ctx.channel.send("Command does not exist.")
            case ",edit":
                if bruh[1] in json_commands:
                    json_commands[bruh[1]] = " ".join(bruh[2:])
                    await ctx.channel.send("Command edited.")
                else:
                    json_commands[ctx.content.split(" ")[1]] = " ".join(bruh[2:])
                    await ctx.channel.send("Command does not exist, but added anyway.")
            case ',rename':
                if bruh[1] in json_commands:
                    json_commands[bruh[2]] = json_commands[bruh[1]]
                    del json_commands[bruh[1]]
                    await ctx.channel.send("Command renamed.")
                else:
                    await ctx.channel.send("Command does not exist.")
            case ",list":
                l = []
                for key, value in json_commands.items():
                    value = value.replace("```", "")
                    l.append(f"**,{key}**\n```{value[:100] + ('...' if len(value) > 100 else '')}```")
                await ctx.channel.send("\n".join(l))
            case _:
                if bruh[0][1:] in json_commands:
                    await ctx.channel.send(f"{ctx.author.display_name}: {json_commands[bruh[0][1:]]}")
                else:
                    await ctx.channel.send("Command does not exist.")
        json.dump(json_commands, open("commands.json", "w"))

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

**Match Reporting** ***[DEPRECATED]*** (Captains and DMs only)
`/report` - Report a match.
`/forfeit` - Report a forfeit.

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

@commands.cooldown(1, 90, commands.BucketType.channel)
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
            ), ephemeral=True
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
        ), ephemeral=True); return

@bot.slash_command(name="report", description="Used to report match, sends the info to a designated channel")
async def report(ctx):

    if not (ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664):
        await ctx.respond("This is a DMs-only command.", ephemeral=True); return
    
    await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Deprecated",
        description="The `/report` command is now deprecated, in favor of automated reporting through Google Sheets!\nScores are now reported in <#1104952742897782825>. A tutorial can be found in the pins of <#1023710972134838402>.",
        color=0xFF9179
    ))

@bot.slash_command(name="forfeit", description="Used to report a forfeit, sends the info to a designated channel.")
async def forfeit(ctx):

    if not (ctx.channel.type == discord.ChannelType.private or ctx.channel.id == 1031781423864090664):
        await ctx.respond(embed=discord.Embed(
            title="SkywardBot - Error",
            description="This is a DMs-only command.",
            color=0xFF0000
        ), ephemeral=True); return

    await ctx.respond(embed=discord.Embed(
        title="SkywardBot - Deprecated",
        description="The `/forfeit` command is now deprecated, in favor of automated reporting through Google Sheets!\nScores are now reported in <#1104952742897782825>. A tutorial can be found in the pins of <#1023710972134838402>.",
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
