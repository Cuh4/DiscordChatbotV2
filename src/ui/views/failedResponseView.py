# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Failed Response UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import ui

# // ---- Main
# // UI
class view(ui.views.view):
    # // Main UI
    def __init__(self):
        # // init
        super().__init__(timeout = 30)
        
        # // class properties
        self.message: discord.Message = None # purely for intellisense
        self.feedbackView = ui.views.feedback(None, None) # this is only being created to extract the buttons and plop it in this view
        
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