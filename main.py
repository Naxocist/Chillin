from discord.ext import commands
from random import *
from alive import alive
from datetime import *
from animelist import *
import pytz
import discord
import asyncio
import os

# Initialize bot client
client = commands.Bot(command_prefix=".",
                      activity=discord.Activity(type=discord.ActivityType.watching, name="for .command"))


@client.event  # setup
async def on_ready():
    print("Chillin' bot is ready for her duty!")


@client.command()  # shows command
async def command(ctx):
    command = {
        '.help': 'Display all command',
        '.date': 'Show current date.',
        '.anime': 'Random an anime for u. :)',

    }
    c = discord.Embed(title="Commands", color=discord.Colour.dark_blue())

    for k, v in command.items():
        c.add_field(name=k, value=v)
        
    await ctx.send(embed=c)


@client.command(aliases=['dat'])  # date function
async def date(ctx):
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    text = str(now.strftime("%A, %d %b %Y %H:%M %p"))
    d = discord.Embed(title=text, color=discord.Colour.random())
    await ctx.send(embed=d)


@client.command(aliases=['ani', 'anim', 'a'])  # random anime
async def anime(ctx):
    i = list(animes.items())
    anime = choice(i)[0]

    embed = discord.Embed(title=f"{anime}", url=f"{link[anime]}",
                          colour=discord.Colour.random())

    episode = "The movie" if ep[anime] == '1' else ep[anime]+" episodes"
    ss = season[anime]

    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    embed.add_field(name="Length", value=episode, inline=True)
    embed.add_field(name="Season", value=ss, inline=True)

    embed.set_thumbnail(url=f"{pic[anime]}")

    embed.set_footer(text="Bot developed by Naxocist")

    await ctx.send(embed=embed)


# @client.command()
# async def grab(ctx):


alive()
TOKEN = os.environ.get('TOKEN')
client.run(TOKEN)
