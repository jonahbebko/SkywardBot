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

@bot.slash_command(name = "dm", description = "Sends a message in dms to everyone with the pinged role")
async def hello(ctx):
    await ctx.respond("this shit dont work yet, give bot man joner some time")

@bot.slash_command(name = "casterinfo", description = "Sends a list of caster availability set by /setcasterinfo")
async def hello(ctx):
    await ctx.respond("this shit dont work yet, give bot man joner some time")

@bot.slash_command(name = "setcasterinfo", description = "Sets the message given by /casterinfo")
async def hello(ctx):
    await ctx.respond("this shit dont work yet, give bot man joner some time")

@bot.slash_command(name = "report", description = "Used to report match, sends the info to a designated channel")
async def hello(ctx):
    await ctx.respond("this shit dont work yet, give bot man joner some time")

@bot.slash_command(name = "requestcaster", description = "Used to request a caster, said caster is then pinged in a designated channel with the info")
async def hello(ctx):
    await ctx.respond("this shit dont work yet, give bot man joner some time")

with open("token.txt") as token:
    bot.run(token.read())