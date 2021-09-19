import discord
from discord.ext import commands
from random import *
from data_process import *
import asyncio
import os

gif_list = ["https://c.tenor.com/c3ks1DYnyr4AAAAC/anime-anime-girl.gif",
            "https://c.tenor.com/czmwFLhXJQ0AAAAC/anime-i-dont-know.gif",
            "https://c.tenor.com/ZINgFAwKh1QAAAAC/anime-love.gif",
            "https://c.tenor.com/Am61DGzxpGoAAAAC/anime-laughing.gif",
            "https://c.tenor.com/mkunLNebofwAAAAC/anime-headbang.gif",
            "https://c.tenor.com/H63Kb7qg8HoAAAAC/anime-chainsaw.gif",
            "https://c.tenor.com/0XNOlxxAFvcAAAAC/chuunibyou-anime.gif",
            "https://c.tenor.com/MyhZzxE8vsQAAAAC/cute-eat.gif",
            "https://c.tenor.com/FwQaJEGLhskAAAAC/cute-cat.gif",
            "https://c.tenor.com/io_R8mA_oUgAAAAC/satania-anime.gif",
            "https://c.tenor.com/jgFVzr3YeJwAAAAC/date-a-live-rage.gif",
            "https://c.tenor.com/rnhV3fu39f8AAAAC/eating-anime.gif",
            "https://c.tenor.com/UShPTojhFIkAAAAi/french-france-gun.gif",
            "https://c.tenor.com/wOCOTBGZJyEAAAAC/chikku-neesan-girl-hit-wall.gif",
            "https://c.tenor.com/FGLllO3BGxMAAAAC/baseball-body.gif",
            "https://c.tenor.com/TPaJW2RZyIYAAAAC/anime-dodge.gif"]

client = commands.Bot(command_prefix=".")

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
    title = anime[:anime.index(":")] + '\n' + ">" + anime[anime.index(":") + 1:] if ':' in anime and len(anime) > 30 \
        else anime
    embed = discord.Embed(title=title, colour=discord.Colour.random())

    g_list = genre[animes.index(anime)]
    g_list.insert(4, "\n")
    g_value = ' '.join([f"`{g.capitalize()}`" for g in g_list])
    
    episode = "`Movie`" if ep[anime] == '0' else f"`{ep[anime]}`" + " episodes"
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
    r_possible = []
    reaction_dict = {"Magic": "✨", "Action": "⚔", "Romance": "💗", "Supernatural": "🌪️", "Comedy": "😝",
                     "Drama": "🎭", "Kids": "🧒", "School": "🏫", "Fantasy": "🐉", "Cars": "🏎", "Sports": "🏀",
                     "Sci-fi": "🧪", "Game": "🎮", "Music": "🎶", "Superpower": "🦸", "Military": "🪖"}
    for g, r in reaction_dict.items():
        if g in g_value:
            r_possible.append(r)
    await discord.Message.add_reaction(msg, choice(r_possible)) if r_possible else \
        await discord.Message.add_reaction(msg, "🔥")


@client.command(pass_context=True, aliases=["commands", "command"])
async def help(ctx):  # help function
    page= "Page"
    invite = "https://discord.com/api/oauth2/authorize?client_id=877425384864501760&permissions=137439308864&scope=bot"
    server = "https://discord.gg/3sAYuxc3aF"
    me = "Naxocist#2982"

    p1 = discord.Embed(title="Just to mention the `SYMBOLS`...", color=discord.Colour.green())
    p1.set_thumbnail(url=choice(gif_list))
    p1.add_field(name="You can keep this anime in DM!", value="> 📬", inline=True)
    p1.add_field(name="Contact", value=f"[Invite!]({invite}) | [Server]({server})\n`{me}` ", inline=False)
    p1.set_footer(text=page + f" 1/2")

    p2 = discord.Embed(title="Commands", color=discord.Colour.green())
    p2.set_thumbnail(url=choice(gif_list))
    p2.add_field(name=f"`.anime | .a [genre(s)]`", value="> Pick a random anime... \uD83D\uDCEC", inline=False)
    p2.set_footer(text=page + f" 2/2")

    async with ctx.typing():
        await asyncio.sleep(0.25)

    msg = await ctx.send(embed=p1)
    await discord.Message.add_reaction(msg, "◀")
    await discord.Message.add_reaction(msg, "▶")
    pages = [p1, p2]
    i = 0

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀", "▶"]

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)  # stops the loop 60 sec
            if str(reaction.emoji) == "▶" and i != 1:
                i += 1
                await msg.edit(embed=pages[i])
                await msg.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀" and i > 0:
                i -= 1
                await msg.edit(embed=pages[i])
                await msg.remove_reaction(reaction, user)

            else:
                await msg.remove_reaction(reaction, user)

        except asyncio.TimeoutError:  # TimeOut
            await msg.delete()
            await ctx.message.delete()
            break


@client.event
async def on_reaction_add(reaction, user):  # check reaction
    if user == client.user:
        return
    if reaction.emoji == "📬":
        await reaction.message.add_reaction("✅")
        await user.send(embed=reaction.message.embeds[0])


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
       
    if isinstance(error, commands.errors.NSFWChannelRequired):
        nsfw_warn = "⚠ This is not `N S F W` channel!"
        await ctx.send(embed=discord.Embed(title=nsfw_warn, color=discord.Colour.from_rgb(225, 225, )))

    else:
        typos = "Typos anywhere?"
        await ctx.send(embed=discord.Embed(title=typos,
                                           description="> Type correctly next time..", 
                                           color=discord.Colour.red()))

TOKEN = os.environ.get('TOKEN')
client.run(TOKEN) 
# client.run("ODg0Njk1Mjg2MDcxNTg2ODU3.YTcOsQ.jWgPgeX8lVOr4rNzdAncn1EOk80")
