import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix=".", 
                    activity=discord.Activity(type=discord.ActivityType.watching, name="for .help"))

client.remove_command('help')

if __name__ == "__main__":
    client.load_extension('utilities')
    client.load_extension('events')
    
    TOKEN = os.environ.get('TOKEN')
    client.run(TOKEN) 
