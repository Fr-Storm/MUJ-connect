import discord
from discord.ext import commands
from discord import app_commands
import json
import os

Intro_channel_id =   # Put your intro channel ID here

# Helper to get intro message ID
async def get_intro_message(guild_id, user_id):
    if not os.path.exists("intros.json"):
        return None

    with open("intros.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return None

    return data.get(str(guild_id), {}).get(str(user_id))


class Assign(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Check for permission: Manage Nicknames
    @app_commands.checks.has_permissions(manage_nicknames=True)
    @app_commands.command(name="assign", description="Assign a gender role and update intro embed")
    @app_commands.describe(
        user="The user to assign the role to",
        gender_role="Choose a gender role to assign",
        message_id="Optional (but preferred): Message ID of intro embed (if not provided, bot will auto find)"
    )
    @app_commands.choices(gender_role=[
        app_commands.Choice(name="Male", value="Male"),
        app_commands.Choice(name="Female", value="Female")
    ])
    async def assign(self, interaction: discord.Interaction, user: discord.Member, gender_role: app_commands.Choice[str], message_id: str = None):
        await interaction.response.defer(ephemeral=True)

        # Prevent giving second gender role
        conflicting_roles = ["Male", "Female"]
        user_current_gender_roles = [r.name for r in user.roles if r.name in conflicting_roles]

        if user_current_gender_roles:
            await interaction.followup.send(f"{user.mention} already has a gender role ({user_current_gender_roles[0]}). Cannot assign another one. ❌", ephemeral=True)
            return

        # Give the selected gender role
        role = discord.utils.get(interaction.guild.roles, name=gender_role.value)
        if not role:
            await interaction.followup.send(f"Role `{gender_role.value}` not found!", ephemeral=True)
            return

        try:
            await user.add_roles(role)
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to assign that role.", ephemeral=True)
            return

        # Get message ID
        if message_id is None:
            message_id = await get_intro_message(interaction.guild.id, user.id)
            if not message_id:
                await interaction.followup.send("Couldn't find intro message for the user.", ephemeral=True)
                return

        intro_channel = interaction.guild.get_channel(Intro_channel_id)
        if intro_channel is None:
            await interaction.followup.send("Intro channel not found!", ephemeral=True)
            return

        try:
            message = await intro_channel.fetch_message(int(message_id))
        except discord.NotFound:
            await interaction.followup.send("Intro message not found!", ephemeral=True)
            return

        # Update the embed
        embed = message.embeds[0]
        if not embed:
            await interaction.followup.send("No embed found in intro message!", ephemeral=True)
            return

        updated_embed = embed.copy()

        found = False
        for idx, field in enumerate(updated_embed.fields):
            if field.name == "🚻 Gender":
                updated_embed.set_field_at(idx, name=field.name, value=gender_role.value, inline=field.inline)
                found = True
                break

        if not found:
            updated_embed.add_field(name="🚻 Gender", value=gender_role.value, inline=True)

        await message.edit(embed=updated_embed)

        await interaction.followup.send(f"Successfully assigned `{gender_role.value}` role and updated intro embed for {user.mention} ✅", ephemeral=True)

    # Custom error handling
    @assign.error
    async def assign_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You don't have permission to use this command. ❌", ephemeral=True)
        else:
            raise error  # Re-raise other errors normally


# Setup
async def setup(bot):
    await bot.add_cog(Assign(bot))
