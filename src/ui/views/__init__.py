# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Views UI Init
# // ---------------------------------------------------------------------

# // Imports
import discord
from .feedbackView import view as feedback

# // Functions
def wrap(message: discord.Message, view: discord.ui.View):
    view.message = message
    return view