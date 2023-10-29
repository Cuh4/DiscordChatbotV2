# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Restart Slash Command
# // ---------------------------------------------------------------------

# // Imports
import discord
from discord import app_commands
import os

from helpers import discord as discordHelpers
import config

# // Main
def command(client: discord.Client, tree: discord.app_commands.CommandTree):
    # slash command
    @app_commands.command(
        name = "restart",
        description = "Restart the bot."
    )
    async def command(interaction: discord.Interaction):
        # check if the user running this command is the person who created the bot
        if not discordHelpers.utils.isCreator(client, interaction.user):
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure(f"Invalid permissions.")
            )
        
        # restart the bot
        await interaction.response.send_message(
            embed = discordHelpers.embeds.success(f"{config.loadingEmoji} Restarting...")
        )
        
        os.system("start py main.py")
        exit(0)