import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from discord.ext import tasks

Intro_channel_id = 1364883858146984057  # 📇intro channel id
intro_data_file = "intro_data.json"

async def save_intro_message(guild_id, user_id, message_id):
    """Save the intro message ID to a JSON file."""
    if os.path.exists(intro_data_file):
        data = {}
    else:
        with open(intro_data_file, "r") as f:
            data = json.load(f)
    
    if str(guild_id) not in data:
        data[str(guild_id)] = {}
    
    data[str(guild_id)][str(user_id)] = message_id

    with open(intro_data_file, "w") as f:
        json.dump(data, f, intend = 4)

async def get_intro_message(guild_id, user_id):
    """Get the intro message ID from the JSON file."""
    if not os.path.exists(intro_data_file):
        return None
    
    with open(intro_data_file, "r") as f:
        data = json.load(f)

    return data.get(str(guild_id), {}).get(str(user_id))

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
        hobbies="List your hobbies separated by commas (e.g. Gaming, Developer, Artist, Cooking, Rider, Writer, Musician)"
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

        def get_matching_roles(possible_roles):
            matching = [role.name for role in member.roles if role.name in possible_roles]
            return matching if matching else ["Not Found"]

        # Role categories
        age_roles = ['18', '19', '20', '21', '22', '23', '24']
        batch_roles = ['Batch-5', 'Batch-6', 'Batch-7', 'Batch-8', 'Batch-9', 'Batch-10', '2022', '2023', '2024', '2025']
        specialization_roles = ['Bca Core', 'Web dev', 'AI-ML', 'Cyber Security', 'Cloud Computing', 'Data Science']

        # Gender handling
        gender = "Not Provided"
        if any(role.name == "Mummy ka 🐊" for role in member.roles):
            gender = "Mummy ka 🐊"
        if any(role.name == "Papa ki 🧚🏻" for role in member.roles):
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
            if role_name: #only process hobby if corresponding role exists
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
            intro_message = await intro_channel.send(embed=embed)
            await save_intro_message(interaction.guild.id, member.id, intro_message.id)
            await interaction.followup.send("Your introduction has been successfully sent! ✅", ephemeral=True)
        else:
            await interaction.followup.send("Whoops, Intro channel not found!❌ Let the admin know.", ephemeral=True)
            
            
            '''Updating intro message on role change'''
        @commands.Cog.listener()
        async def on_member_update(self, before, after):
            if before.roles == after.roles:
                return  # No role changes, ignore

            intro_message_id = await get_intro_message(after.guild.id, after.id)
            if not intro_message_id:
                return  # No intro message to edit

            # Rebuild the embed
            gender = "Not Provided"
            if any(role.name == "Mummy ka 🐊" for role in after.roles):
                gender = "Male"
            elif any(role.name == "Papa ki 🧚🏻" for role in after.roles):
                gender = "Female"

            # Similar logic for age, batch, specialization
            age = get_matching_roles(after, ['18', '19', '20', '21', '22', '23', '24'])
            batch = get_matching_roles(after, ['Batch-5', 'Batch-6', 'Batch-7', 'Batch-8', 'Batch-9', 'Batch-10', '2022', '2023', '2024', '2025'])
            specialization = get_matching_roles(after, ['Bca Core', 'Web dev', 'AI-ML', 'Cyber Security', 'Cloud Computing', 'Data Science'])

            intro_channel = after.guild.get_channel(Intro_channel_id)
            if intro_channel is None:
                return

            try:
                message = await intro_channel.fetch_message(intro_message_id)

                # Rebuild the embed
                updated_embed = discord.Embed(
                    title="📇Member introduction",
                    color=discord.Color.blurple()
                )
                updated_embed.set_thumbnail(url=after.avatar.url)
                updated_embed.add_field(name="👋 Name", value=after.display_name, inline=False)
                updated_embed.add_field(name="🎂 Age", value=", ".join(age) if age else "Not Found", inline=True)
                updated_embed.add_field(name="🚻 Gender", value=gender, inline=True)
                updated_embed.add_field(name="🛠️ Specialisation", value=", ".join(specialization) if specialization else "Not Found", inline=False)
                updated_embed.add_field(name="🏫 Year", value=", ".join(batch) if batch else "Not Found", inline=True)
                updated_embed.add_field(name="🎯 Hobbies", value="(No hobbies update)", inline=False)
                updated_embed.add_field(name="🌐 Socials", value="(No socials update)", inline=False)
                updated_embed.set_footer(text = f"Welcome to the server {after.display_name}!")

                await message.edit(embed=updated_embed)

            except discord.NotFound:
                pass  # Message might have been deleted
            except Exception as e:
                print(f"Failed to update intro: {e}")

        # Helper for multiple roles
        def get_matching_roles(member, role_names):
            return [role.name for role in member.roles if role.name in role_names]        
        







async def setup(bot):
    await bot.add_cog(Intro(bot))
