import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import webserver

# Load environment variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
if token is None:
    raise ValueError("DISCORD_TOKEN not found in environment variables.")

# Setup logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Enable intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create custom bot class
class MyBot(commands.Bot):
    async def on_ready(self):
        print(f"Syncing commands to guild...")
        guild = discord.Object(id=1364880687185788950) #guild ID
        await self.tree.sync(guild=guild)
        # Uncomment for global sync (takes longer)
        await self.tree.sync()
        print(f"Commands synced successfully.")
        await self.change_presence(activity=discord.Game(name="with the API"))
        print(f'Logged in as {self.user}')

# Instantiate the bot
bot = MyBot(command_prefix=".", intents=intents)

# Load cogs
async def setup_hook():
    await bot.load_extension("cogs.intro")
    await bot.load_extension("cogs.assign")
bot.setup_hook = setup_hook

# Simple test command
@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")

# Run webserver and bot
webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
