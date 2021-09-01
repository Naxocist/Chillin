import pytz
import discord
import asyncio
from random import *
from alive import alive
from datetime import *
from animelist import *

command = {
    '.date': 'Show current date.',
    '.anime': 'Random an anime for u. :)',
}
bot = discord.Client()


async def on_ready():
    print("Chillin' is ready for his duty.")


@bot.event
async def on_message(message):
    send = message.channel.send
    msg = message.content.lower()
    if message.author == bot.user:
        return

    if msg.startswith(".command"):
        s = ""
        for i in command:
            s += i + "  :  " + command[i] + "\n"
        async with message.channel.typing():
            await asyncio.sleep(0.25)
        await send(s)

    if msg in [".dat", ".date"]:  # date function
        async with message.channel.typing():
            await asyncio.sleep(0.5)
        now = datetime.now(pytz.timezone('Asia/Bangkok'))
        await send(str(now.strftime("```css\n Date : %A, %d %b %Y %H:%M%p```")))

    if message.content.startswith(".anime"):  # Random Anime
        i = list(animes.items())
        anime = choice(i)[0]
        e = ["(o´▽`o)", "(¯▿¯)", "(˙꒳​˙)"]
        a1 = choice(e)
        e.pop(e.index(a1))
        a2 = choice(e)

        embed = discord.Embed(title=f"{anime}",
                              url=f"{link[anime]}",
                              colour=discord.Colour.random())

        embed.set_author(name=message.author.display_name,
                         icon_url=message.author.avatar_url)

        g = genre[anime].replace("[", " ").replace("]", " ").replace("\'", " ")
        embed.add_field(name="Genre", value=g, inline=False)

        episode = "The Movies" if ep[anime] == '1' else  f"Episodes : {ep[anime]}"

        embed.add_field(name=episode, value="\u200b", inline=True)

        embed.set_image(url=f"{pic[anime]}")

        r = rank[anime]
        r = "Invalid" if r == "" else r
        embed.add_field(name=f"Rank : {r}", value="\u200b", inline=True)
        embed.set_footer(text="Bot developed by Naxocist")
        await send(embed=embed)


alive()
bot.run('ODc3NDI1Mzg0ODY0NTAxNzYw.YRycEQ.qLrJI_seoWMFxZ6dk3O83pCY568')
