import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv 
import os 
import random
import asyncio
import webserver


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
if token is None:
    raise ValueError("DISCORD_TOKEN not found in environment variables.")


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

#Manually enable the intent/s here to do anything you wanna do
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    guild = discord.Object(id=1365276830524772362)
    await bot.tree.sync(guild = guild)              #global sync takes over an hour to sync
    # await bot.tree.sync()                        #uncomment this line to sync globally
    await bot.change_presence(activity=discord.Game(name="with the API"))
    print(f'We have logged in as {bot.user}')

@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
