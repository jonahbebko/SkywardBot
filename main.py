"""

LIST OF COMMANDS:

/dm <role> <message> (admin only)
sends a message in dms to everyone with the pinged role

/casterinfo (dms only)
sends a list of caster availability set by /setcasterinfo

/setcasterinfo <message> (admin only)
sets the message given by /setcasterinfo

/report <week> <ID> <score-score> <ID> (dms only)
used to report match, sends the info to a designated channel or gsheet

/casterrequest <ID> <day> <time> (dms only)
used to request a caster, said caster is then pinged in a designated channel with the info

/flipout
responds with kissy face emoji

/benjamin
responds with benjamin

"""

import discord

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is online")

@bot.slash_command(name = "flipout", description = "flipout")
async def hello(ctx):
    await ctx.respond("flipout :kissing_heart:")

@bot.slash_command(name = "benjamin", description = "benjamin")
async def hello(ctx):
    await ctx.respond("benjamin :flushed:")

with open("token.txt") as token:
    bot.run(token.read())