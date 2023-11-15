# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Failed Response UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

from ui.views import template
from ui import modals
from ui.views import feedback

# // ---- Main
# // UI
class view(template):
    # // Main UI
    def __init__(self):
        # // init
        super().__init__(timeout = 30)
        
        # // class properties
        self.message: discord.Message = None # purely for intellisense
        self.feedbackView = feedback(None, None) # this is only being created to extract the buttons and plop it in this view
        
        # // feedback button
        # create button
        self.feedbackButton = self.feedbackView.feedbackButton
    
        # add
        self.add_item(self.feedbackButton)

        # // discord invite button
        # create button
        self.inviteButton = self.feedbackView.inviteButton
        
        # add
        self.add_item(self.inviteButton)