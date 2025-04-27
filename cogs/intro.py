import discord
from discord.ext import commands
from discord import app_commands

Intro_channel_id = 1364883858146984057  # 📇intro channel id

# Mapping hobbies to role names
Hobby_Roles = {
    'Gaming': "Gamer",
    'Developer': "Developer",
    'Artist': "Artist",
    'Musician': "Musician",
    'Cooking': "Cook",
    'Rider': "Rider",
    'Writer': "Writer",
}

class Intro(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='intro', description='Introduce yourself to the server')
    @app_commands.describe(
        name='Your name',
        socials="Your social media IDs",
        hobbies="List your hobbies separated by commas (e.g. Gaming, Developer, Artist)"
    )
    async def intro(
        self, 
        interaction: discord.Interaction, 
        name: str, 
        socials: str, 
        hobbies: str
    ):
        await interaction.response.defer(ephemeral=True)

        member = interaction.user

        # Correct get_role function
        # def get_matching_role(possible_roles):
        #     for role in member.roles:
        #         if role.name in possible_roles:
        #             return role.name
        #     return "Role not found"

        def get_matching_roles(possible_roles):
            matching = [role.name for role in member.roles if role.name in possible_roles]
            return matching if matching else ["Not Found"]

        # Role categories
        age_roles = ['18', '19', '20', '21', '22', '23', '24']
        batch_roles = ['Batch-5', 'Batch-6', 'Batch-7', 'Batch-8', 'Batch-9', 'Batch-10', '2022', '2023', '2024', '2025']
        specialization_roles = ['Bca Core', 'Web dev', 'AI-ML', 'Cyber Security', 'Cloud Computing', 'Data Science']

        # Gender handling
        gender = "Not Provided"
        if any(role.name == "Mummy ka 🐊" for role in member.roles):  #This is for male (I blame the guy who asked me to make the bot for this)
            gender = "Mummy ka 🐊"
        if any(role.name == "Papa ki 🧚🏻" for role in member.roles):   #This is for female
            gender = "Papa ki 🧚🏻"

        # Find roles
        age = get_matching_roles(age_roles)
        batch = get_matching_roles(batch_roles)
        specializations = get_matching_roles(specialization_roles)


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
            print(f"Nickname changed to {name}")
        except discord.Forbidden:
            print("Bot cannot change nickname, permission issue.")
        except discord.HTTPException as e:
            print(f"Failed to change nickname: {e}")


        # Build embed
        embed = discord.Embed(
            title="📇 Member Introduction",
            color=discord.Color.blurple()
        )
        age_display = ", ".join(age)
        batch_display = ", ".join(batch)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="👋 Name", value=name, inline=False)
        embed.add_field(name="🎂 Age", value=age_display, inline=True)
        embed.add_field(name="🚻 Gender", value=gender, inline=True)
        specialization_display = ", ".join(specializations) 
        embed.add_field(name="🛠️ Specialisation", value=specialization_display, inline=False)
        embed.add_field(name="🏫 Year", value=batch_display, inline=True)
        embed.add_field(name="🎯 Hobbies", value=hobbies_display, inline=False)
        embed.add_field(name="🌐 Socials", value=socials, inline=False)
        embed.set_footer(text=f"Welcome to the server {member.display_name}!")

        # Send intro
        intro_channel = interaction.guild.get_channel(Intro_channel_id)
        if intro_channel:
            await intro_channel.send(embed=embed)
            await interaction.followup.send("Your introduction has been successfully sent! ✅", ephemeral=True)
        else:
            await interaction.followup.send("Whoops, Intro channel not found!❌ Let the admin know.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Intro(bot))
