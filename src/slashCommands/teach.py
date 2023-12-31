# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Teach Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import ui
from modules import general as helpers

# // ---- Main
# // create command
def command():
    # // get vars
    # discord-related
    tree: discord.app_commands.CommandTree = helpers.globals.get("commandTree")

    # // main command
    # slash command
    @tree.command(
        name = "teach",
        description = "Teaches the chatbot responses for queries."
    )
    async def command(interaction: discord.Interaction):
        return await interaction.response.send_modal(ui.modals.teach())

# // start command
command()