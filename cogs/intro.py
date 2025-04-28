import discord
from discord.ext import commands
from discord import app_commands
import json
import os

Intro_channel_id =   # Put your intro channel ID here

# Hobby -> Role Mapping (Change them as per your need)
Hobby_Roles = {
    'Gaming': "Gamer",
    'Developing': "Developer",
    'Artist': "Artist",
    'Musician': "Musician",
    'Cooking': "Cook",
    'Rider': "Rider",
    'Writing': "Writer",
}

# Function to save intro message ID to a JSON file
async def save_intro_message(guild_id, user_id, message_id):
    if not os.path.exists("intros.json"):
        with open("intros.json", "w") as f:
            json.dump({}, f)

    with open("intros.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    if str(guild_id) not in data:
        data[str(guild_id)] = {}

    data[str(guild_id)][str(user_id)] = message_id

    with open("intros.json", "w") as f:
        json.dump(data, f, indent=4)

# Function to get intro message ID from a JSON file
async def get_intro_message(guild_id, user_id):
    if not os.path.exists("intros.json"):
        with open("intros.json", "w") as f:
            json.dump({}, f)

    with open("intros.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    return data.get(str(guild_id), {}).get(str(user_id))

# Helper to get matching roles
def get_matching_roles(member, role_names):
    return [role.name for role in member.roles if role.name in role_names]

class Intro(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='intro', description='Introduce yourself to the server')
    @app_commands.describe(
        name='Your name',
        socials="Your social media IDs",
        hobbies="List your hobbies separated by commas (e.g. Gaming, Developing, Artist, Musician, Cooking, Rider, Writing)"
    )
    async def intro(self, interaction: discord.Interaction, name: str, socials: str, hobbies: str):
        await interaction.response.defer(ephemeral=True)

        member = interaction.user

        # Role categories
        age_roles = ['18', '19', '20', '21', '22', '23', '24']
        batch_roles = ['Batch-5', 'Batch-6', 'Batch-7', 'Batch-8', 'Batch-9', 'Batch-10', '2022', '2023', '2024', '2025']
        specialization_roles = ['Bca Core', 'Web dev', 'AI-ML', 'Cyber Security', 'Cloud Computing', 'Data Science']

        # Gender detection
        gender = "Not Provided"
        if any(role.name == "Male" for role in member.roles):
            gender = "Male"
        elif any(role.name == "Female" for role in member.roles):
            gender = "Female"

        # Get roles
        age = get_matching_roles(member, age_roles)
        batch = get_matching_roles(member, batch_roles)
        specialization = get_matching_roles(member, specialization_roles)

        # Handle hobbies
        hobby_list = [hobby.strip() for hobby in hobbies.split(',')]
        hobby_roles_to_add = []

        for hobby in hobby_list:
            role_name = Hobby_Roles.get(hobby)
            if role_name:
                role = discord.utils.get(member.guild.roles, name=role_name)
                if role and role not in member.roles:
                    hobby_roles_to_add.append(role)

        if hobby_roles_to_add:
            await member.add_roles(*hobby_roles_to_add)

        hobbies_display = ", ".join(hobby_list) if hobby_list else "None Selected"

        # Set nickname
        try:
            await member.edit(nick=name)
        except (discord.Forbidden, discord.HTTPException):
            pass

        # Build the embed
        embed = discord.Embed(
            title="📇 Member Introduction",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="👋 Name", value=name, inline=False)
        embed.add_field(name="🎂 Age", value=", ".join(age) or "Not Found", inline=True)
        embed.add_field(name="🚻 Gender", value=gender, inline=True)
        embed.add_field(name="🛠️ Specialisation", value=", ".join(specialization) or "Not Found", inline=False)
        embed.add_field(name="🏫 Year", value=", ".join(batch) or "Not Found", inline=True)
        embed.add_field(name="🎯 Hobbies", value=hobbies_display, inline=False)
        embed.add_field(name="🌐 Socials", value=socials, inline=False)
        embed.set_footer(text=f"Welcome to the server {member.display_name}!")

        intro_channel = interaction.guild.get_channel(Intro_channel_id)
        if intro_channel:
            intro_message = await intro_channel.send(embed=embed)
            await save_intro_message(interaction.guild.id, member.id, intro_message.id)
            await interaction.followup.send("Your introduction has been successfully sent! ✅", ephemeral=True)
        else:
            await interaction.followup.send("Whoops, Intro channel not found!❌ Let the admin know.", ephemeral=True)

# Setup function
async def setup(bot):
    await bot.add_cog(Intro(bot))
