from discord.ext import commands
from random import *
from alive import alive
from datetime import *
from animelist import *
import pytz
import discord
import os
import asyncio

gif_list = ["https://www.icegif.com/wp-content/uploads/icegif-10.gif",
            "https://i.kym-cdn.com/photos/images/newsfeed/000/543/398/2f3.gif",
            "https://c.tenor.com/dXeGgnB4u_sAAAAM/dragon-woman-anime.gif",
            "https://giffiles.alphacoders.com/398/3987.gif",
            "https://static.zerochan.net/Gravity.Falls.full.2109794.gif",
            "https://giffiles.alphacoders.com/140/14018.gif",
            "https://acegif.com/wp-content/uploads/2020/07/anime-sleep.gif"]

# Initialize bot client
client = commands.Bot(command_prefix=".",
                      activity=discord.Activity(type=discord.ActivityType.watching, name="for .command"))


@client.event  # setup
async def on_ready():
    print("Chillin' bot is ready for her duty!")


@client.command(aliases=["commands"])  # shows command
async def command(ctx):
    command = {
        '.command': 'Show all commands',
        '.date': 'Show current date and time',
        '.anime': 'Somehow pick random anime',

    }
    c = discord.Embed(title="Commands", color=discord.Colour.random())
    for k, v in command.items():
        c.add_field(name=k, value=v, inline=False)
    c.set_thumbnail(url=choice(gif_list))
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
    ss = "not specified" if episode == "The movie" else season[anime]
    image = pic[anime]
    ranked = rank[anime]
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    embed.add_field(name="Genre", value=genre[anime], inline=False)
    embed.add_field(name="Season", value=ss, inline=True)
    embed.add_field(name="Length", value=episode, inline=True)
    embed.add_field(name=f"Ranked: #{ranked}", value="Check it out!", inline=False)

    embed.set_thumbnail(url=choice(gif_list))
    embed.set_image(url=image)
    embed.set_footer(text="Database references from `MyAnimelist.net`")

    await ctx.send(embed=embed)

alive()
TOKEN = os.environ.get('TOKEN')
client.run('ODc3NDI1Mzg0ODY0NTAxNzYw.YRycEQ.tqx3yhBer4BlOXxyLAcYpxLG0cY')
