# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Failed Response UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

from ui.views import template
from ui import modals
from ui.views import response

# // ---- Main
# // UI
class view(template):
    # // Main UI
    def __init__(self):
        # // init
        super().__init__(timeout = 30)

        # // class properties
        self.responseView = response(None, None) # this is only being created to extract the buttons and plop it in this view
        
        # // teach button
        # create button
        self.teachButton = self.responseView.teachButton
    
        # add
        self.add_item(self.teachButton)

        # // discord invite button
        # create button
        self.inviteButton = self.responseView.inviteButton
        
        # add
        self.add_item(self.inviteButton)