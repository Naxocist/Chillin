from discord.ext import commands
from bs4 import BeautifulSoup
from random import *
from datetime import *
from animelist import *
import pytz
import discord
import requests
import asyncio
import os

gif_list = ["https://www.icegif.com/wp-content/uploads/icegif-10.gif",
            "https://i.kym-cdn.com/photos/images/newsfeed/000/543/398/2f3.gif",
            "https://c.tenor.com/dXeGgnB4u_sAAAAM/dragon-woman-anime.gif",
            "https://giffiles.alphacoders.com/398/3987.gif",
            "https://static.zerochan.net/Gravity.Falls.full.2109794.gif",
            "https://giffiles.alphacoders.com/140/14018.gif",
            "https://acegif.com/wp-content/uploads/2020/07/anime-sleep.gif"]

client = commands.Bot(command_prefix=".",
                      activity=discord.Activity(type=discord.ActivityType.watching, name="for .help"))

client.remove_command('help')


def get_anime_name(specify):
    possible = []
    if not specify:
        return choice(animes)

    specify_list = specify.lower().split()
    for g in genre:
        if all(ele in g for ele in specify_list):
            possible.append(animes[genre.index(g)])

    return choice(possible)


@client.event
async def on_ready():  # Ready
    print("Chillin' bot is ready for her duty!")


@client.command(aliases=['a'])  # random anime [optional genre]
async def anime(ctx, *, specify=""):
    anime = get_anime_name(specify)

    g_list = genre[animes.index(anime)]
    g_list.insert(4, "\n")
    g_value = ' '.join([f"`{g.capitalize()}`" for g in g_list])

    title = anime[:anime.index(":")] + '\n' + ">" + anime[anime.index(":") + 1:] if ':' in anime and len(anime) > 30 \
        else anime

    embed = discord.Embed(title=title, colour=discord.Colour.random())

    episode = "`Movie`" if ep[anime] == '1' else f"`{ep[anime]}`" + " episodes"
    ss = "not specified" if episode == "The movie" else season[anime]
    image = pic[anime]
    ranked = rank[anime]
    url = link[anime]
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    embed.add_field(name="Genre", value=g_value, inline=False)
    embed.add_field(name="Season", value=f"`{ss}`", inline=True)
    embed.add_field(name="Length", value=episode, inline=True)
    embed.add_field(name=f"Ranked: #`{ranked}`", value=f"[Check it out!]({url})", inline=False)

    embed.set_image(url=image)
    msg = await ctx.send(embed=embed)
    await discord.Message.add_reaction(msg, "📬")


@client.command(aliases=["ah"])
@commands.is_nsfw()
async def animehentai(ctx):
    anime = choice(nsfw)
    embed = discord.Embed(title=f"{anime}", url=link[anime], colour=discord.Colour.random())

    episode = "`1` ep" if ep[anime] == '1' else f"`{ep[anime]}`" + " epa"
    ss = "not specified" if episode == "The movie" else season[anime]
    image = pic[anime]
    ranked = rank[anime]
    g_list = nsfw_genre[nsfw.index(anime)]
    g_list.insert(4, "\n")
    g_value = ' '.join([f"`{g.capitalize()}`" for g in g_list])
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    embed.add_field(name="Genre", value=g_value, inline=False)
    embed.add_field(name="Season", value=f"`{ss}`", inline=True)
    embed.add_field(name="Length", value=episode, inline=True)
    embed.add_field(name=f"`{ranked}`", value="-"*40, inline=False)

    embed.set_image(url=image)

    msg = await ctx.send(embed=embed)
    await discord.Message.add_reaction(msg, "📬")
    await discord.Message.add_reaction(msg, "🔥")
    await discord.Message.add_reaction(msg, "💪")


@client.command(aliases=["d"])
@commands.is_nsfw()
async def doujin(ctx, code=""):
    code = code.strip()
    if code:
        url = 'https://nhentai.net/g/' + code
    else:
        url = "https://nhentai.net/random/"
    async with ctx.typing():
        request = requests.get(url).text
        soup = BeautifulSoup(request, 'html.parser')
        await asyncio.sleep(0.25)

    error = soup.find("div", class_="container error")
    if error:
        green = randint(1, 150)
        embed = discord.Embed(title="We don't know that sauce!", description="> May be `typos` somewhere?",
                              color=discord.Colour.from_rgb(225, green, 0))
        await ctx.send(embed=embed)
    else:
        pic = soup.find("img", class_="lazyload")['data-src']
        name = soup.find("span", class_="pretty").text
        id = soup.find("h3", id="gallery_id").text
        embed = discord.Embed(title=name, url=f"https://nhentai.net/g/{id[1:]}", color=discord.Colour.random())

        if code:
            embed.add_field(name=f"Sauce `{code}` delivered!", value="Verified Sauce! Here you go.")
        else:
            embed.add_field(name=f"Random sauce => `{id}` delivered!", value="`There you go!`")

        embed.set_image(url=pic)
        msg = await ctx.send(embed=embed)
        await discord.Message.add_reaction(msg, "📬")
        await discord.Message.add_reaction(msg, "🔞")


# @client.command(aliases=["fn"])
# async def fanart(ctx, character):

#
# @client.command(aliases=["pop", "p"])
# async def popular(ctx):
#     url = "https://myanimelist.net/"
#     async with ctx.typing():
#         request = requests.get(url).text
#         soup = BeautifulSoup(request, 'html.parser')
#         await asyncio.sleep(0.25)


@client.command(aliases=['dat'])  # date function
async def date(ctx):
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    text = str(now.strftime("%A, %d %b %Y %H:%M %p"))
    d = discord.Embed(title=text, color=discord.Colour.random())
    async with ctx.typing():
        await asyncio.sleep(0.5)
    await ctx.send(embed=d)


@client.command(pass_context=True, aliases=["commands", "command"])
async def help(ctx):
    embed = discord.Embed(title="Commands prefix: `.`", color=discord.Colour.random())
    embed.set_thumbnail(url=choice(gif_list))

    embed.add_field(name='`anime | a [optional genre seperated by space]`  📬',
                    value='> Somehow pick random anime for YOU!')
    embed.add_field(name='`date | dat`  🕒', value='> Show current date and time', inline=False)

    embed.add_field(name='`animehentai | ah ⚠`', value='> Random rated Hentai :underage:', inline=True)
    embed.add_field(name='`doujin | d [sauce number] ⚠`', value='> Doujin based on nhentai :bookmark_tabs:', inline=True)

    invite = "https://discord.com/api/oauth2/authorize?client_id=877425384864501760&permissions=137439300672&scope=bot"
    server = "https://discord.gg/3sAYuxc3aF"
    me = "Naxocist#2982"

    embed.add_field(name="`⚠` >> NSFW text channel", value="\u200b", inline=False)
    embed.add_field(name="`📬` >> save the result..", value="-"*70)
    embed.add_field(name="Contact", value=f"[Invite!]({invite}) | [Server]({server})\nDeveloper: `{me}` ", inline=False)
    async with ctx.typing():
        await asyncio.sleep(0.25)
    await ctx.send(embed=embed)


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    if reaction.emoji == "📬":
        await reaction.message.add_reaction("✅")
        await user.send(embed=reaction.message.embeds[0])


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.NSFWChannelRequired):
        nsfw_warn = "⚠ This is not `N S F W` channel!"
        await ctx.send(embed=discord.Embed(title=nsfw_warn, color=discord.Colour.from_rgb(225, 225, 0)))
    if isinstance(error, commands.errors.CommandInvokeError):
        genre_warn = "Invalid Genre!"
        await ctx.send(embed=discord.Embed(title=genre_warn, description="> May be `typos` somewhere?", color=discord.Colour.from_rgb(225, 225, 0)))

TOKEN = os.environ.get('TOKEN')
client.run(TOKEN)
# client.run('ODg0Njk1Mjg2MDcxNTg2ODU3.YTcOsQ.WL5NqEvyozbxHjMevICJOSnKMro')
