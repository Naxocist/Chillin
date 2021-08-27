import sqlite3
import pytz
import discord
import os
import asyncio
from random import *
from alive import alive
from datetime import *

def add(i):
  conn = sqlite3.connect('anime.db')
  c = conn.cursor()
  c.execute(f"INSERT INTO animes VALUES ('{i}')")
  print(f"Added {i}")
  conn.commit()
  conn.close()


def remove(id):
  conn = sqlite3.connect('anime.db')
  c = conn.cursor()
  c.execute(f"DELETE from animes WHERE rowid={id}")
  conn.commit()
  conn.close()

def show_list():
  conn = sqlite3.connect('anime.db')
  c = conn.cursor()
  c.execute("SELECT rowid, * FROM animes")

  r=[i[1] for i in c.fetchall()]
  print(r)
  return r


command = {
  '.date':'Show current date.',
  '.anime':'Random an anime for u. :)',
  '.addanime':'Add an anime in random list.',
  '.list':'Show all animes in database.'
  }
bot = discord.Client()

async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for date"))

@bot.event
async def on_message(message):
    send=message.channel.send

    msg = message.content.lower()
    if message.author == bot.user:
        return

    if msg.startswith(".command"):
        s=""
        for i in command:
          s+=i+"  :  "+command[i]+"\n"
        async with message.channel.typing():
          await asyncio.sleep(0.25)
        await send(s)

    if msg in [".dat", ".date"]: #date function
        async with message.channel.typing():
          await asyncio.sleep(0.5)
        now = datetime.now(pytz.timezone('Asia/Bangkok'))
        await send(now.strftime("`📅 %A, %d %b %Y %H:%M%p `"))
    
    if msg.startswith(".anime"): # Random Anime
        e = ["╰(▔∀▔)╯", "( Φ ω Φ )"]
        a1 = choice(e);e.pop(e.index(a1));a2 = choice(e)
        title = f"`{a1}  Random Anime  {a2}`"
        l = len(title)
        if l%2==0:c = len(title)/2
        else:c = len(title)/2+0.5
        ans = "‎‎ "*int(c)

        async with message.channel.typing():
          await asyncio.sleep(0.5)

        await send(f"{title}\n")
        
        await send(ans + f"⥅  `{choice(show_list()).capitalize()}`  ⥆")

    if msg.startswith(".addanime"): # Add Anime in List
        i=msg.replace(".addanime", "")
        i=i.strip()
        add(i);print(i)
        await send(f"Added {i}!")


    if msg.startswith(".list"):
        db = show_list()
        async with message.channel.typing():
          await asyncio.sleep(0.25)
        await send(f"`{db}`")

    if msg.startswith(".remove"):
        i=msg.replace(".remove", "")
        remove(i)
        await send("Remove Successfully!")

    # Index function
alive()
bot.run('ODc3NDI1Mzg0ODY0NTAxNzYw.YRycEQ.qLrJI_seoWMFxZ6dk3O83pCY568')
