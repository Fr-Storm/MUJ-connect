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

# Set up logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Manually enable the intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Subclass commands.Bot
class MyBot(commands.Bot):
    async def on_ready(self):
        print(f"Syncing to guild...")
        guild = discord.Object(id=1364880687185788950)
        await self.tree.sync(guild=guild)  # Sync with the specific guild
        # Uncomment the next line for global sync (takes longer)
        await self.tree.sync()
        print(f'Commands synced successfully.')
        await self.change_presence(activity=discord.Game(name="with the API"))
        print(f'We have logged in as {self.user}')

# Create an instance of the subclassed bot
bot = MyBot(command_prefix=".", intents=intents)

# Setup hook
async def setup_hook():
    await bot.load_extension("cogs.intro")  # Load the intro cog
bot.setup_hook = setup_hook

@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")


webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
