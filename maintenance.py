import discord

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

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

@bot.slash_command(name="help", description="Sends a list of commands.")
async def help(ctx):
    await ctx.respond("SkywardBot is currently under maintenance, please try again later.")

@bot.slash_command(name="log", description="See the recent updates for SkywardBot.")
async def log(ctx):
    await ctx.respond("SkywardBot is currently under maintenance, please try again later.")

@bot.slash_command(name="reportbug", description="Report a bug to joner himself.")
async def reportbug(ctx):
    await ctx.respond("SkywardBot is currently under maintenance, please try again later.")

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