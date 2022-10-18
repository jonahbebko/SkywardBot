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
from datetime import datetime

with open('ids.json') as f:
    ids = json.load(f)

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is online")

@bot.slash_command(name = "ping", description = "Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {str(1000.0*bot.latency)[:5]}ms.")

@bot.slash_command(name = "flipout", description = "flipout")
async def flipout(ctx):
    await ctx.respond("flipout :kissing_heart:")

@bot.slash_command(name = "benjamin", description = "benjamin")
async def benjamin(ctx):
    await ctx.respond("benjamin :flushed:")

@bot.slash_command(name = "dm", description = "Sends a message in dms to everyone with the pinged role.")
async def dm(ctx, role: discord.Role, message: str):
    if ctx.author.guild_permissions.administrator:
        await ctx.respond(f"Sending message to all members with role **\"{role}\"** (ID: {role.id})...")
        for member in role.members:
            await member.send(message)
        await ctx.send("Sent.")
    else:
        await ctx.respond("You must be an administrator to use this command.")
        today = datetime.now().strftime("%m/%d/%y %H:%M:%S")
        with open("log.txt", "w+") as logf:
            logf.write(f"[{today}] {ctx.author} attempted to use /dm on role \"{role}\" with message \"{message}\"")
        print(f"[{today}] {ctx.author} attempted to use /dm on role \"{role}\" with message \"{message}\"")

@bot.slash_command(name = "casterinfo", description = "Sends a list of caster availability.")
async def casterinfo(ctx):
    if ctx.channel.type == discord.ChannelType.private:
        await ctx.respond(embed=discord.Embed(
            color=0x429B97,
            title="Caster Info",
            description="<:dot:1031708752140832768> You can see caster availability [here!](https://docs.google.com/spreadsheets/d/1YfXo1ehAI8GDIiwG6dI09_In2VbxX7TjwBLA0Lgs430/edit?usp=sharing)"
        ))
    else:
        await ctx.respond("This is a DMs-only command.")

@bot.slash_command(name = "report", description = "Used to report match, sends the info to a designated channel.")
async def report(ctx, week: int, team_one_tag: str, score: str, team_two_tag: str):
    if ctx.channel.type == discord.ChannelType.private:
        temp = [int(i) for i in score.split("-")]

        if temp[0] > temp[1]:
            who_won = f"**{team_one_tag}** won against **{team_two_tag}**"
        elif temp[0] < temp[1]:
            who_won = f"**{team_one_tag}** lost to **{team_two_tag}**"
        else:
            who_won = f"**{team_one_tag}** and **{team_two_tag}** tied"

        await bot.get_channel(1025198171435049032).send("<@&1022316227131080797>", embed=discord.Embed(
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

@bot.slash_command(name = "requestcaster", description = "Used to request a caster, said caster is then pinged in a designated channel with the info.")
async def requestcaster(ctx, day: str, time: str):
    if ctx.channel.type == discord.ChannelType.private:
        await ctx.respond(
            "Please enter the number cooresponding to the caster you would like to request:\n",
            embed=discord.Embed(
                color=0x429B97,
                title="Caster Request Numbers",
                description="\n".join([f"{i+1}. {caster}" for i, caster in enumerate(ids)])
            )
        )
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
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

with open("token.txt") as token:
    bot.run(token.read())