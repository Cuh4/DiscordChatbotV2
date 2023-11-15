# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Views UI Init
# // ---------------------------------------------------------------------

# // Imports
import discord

from template import view as template
from .feedbackView import view as feedback
from .failedResponseView import view as failedResponse

# // Functions
def wrap(message: discord.Message, view: discord.ui.View):
    view.message = message
    return view