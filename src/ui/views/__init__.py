# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Views UI Init
# // ---------------------------------------------------------------------

# // Imports
import discord

from .template import view as template
from .responseView import view as response
from .failedResponseView import view as failedResponse

# // Functions
def wrap(message: discord.Message, view: discord.ui.View):
    view.message = message
    return view