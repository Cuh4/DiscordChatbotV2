# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Teach Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import chatbot as _chatbot # do not add two "_" !! it fucks things up because of how python treats private methods or something i dont know
import ui
from helpers import general as helpers

from . import register

# // ---- Main
@register
def command():
    # // get vars
    # discord-related
    tree: discord.app_commands.CommandTree = helpers.globals.get("commandTree")

    # // main command
    # slash command
    @tree.command(
        name = "teach",
        description = "Teach the chatbot responses for queries."
    )
    async def command(interaction: discord.Interaction):
        return await interaction.response.send_modal(ui.modals.teach())
    
    return tree.get_command("teach")