# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Restart Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import os

from modules import general as helpers
from modules import discord as discordHelpers

# // ---- Main
# // create command
def command():
    # // get vars
    # discord-related
    client: discord.Client = helpers.globals.get("client")
    tree: discord.app_commands.CommandTree = helpers.globals.get("commandTree")
    
    # // main command
    # slash command
    @tree.command(
        name = "restart",
        description = "Restarts the bot."
    )
    async def command(interaction: discord.Interaction):
        # check if the user running this command is the person who created the bot
        if not discordHelpers.utils.isCreator(client, interaction.user):
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure("Invalid permissions.")
            )
        
        # restart the bot
        await interaction.response.send_message(
            embed = discordHelpers.embeds.load("Restarting...")
        )
        
        os.system("start py main.py")
        exit(0)

# // start command
command()