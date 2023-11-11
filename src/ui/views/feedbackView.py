# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Feedback View UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import random

import chatbot
import ui
from helpers import general as helpers
from helpers import discord as discordHelpers

# // ---- Main
# // UI
class view(discord.ui.View):
    # // Main UI
    def __init__(self, response: chatbot.response, message: discord.Message):
        # // init
        super().__init__(timeout = 15)
        
        # // class properties
        self.bot = helpers.globals.get("chatbot")
        self.chatbotResponse = response
        self.message: discord.Message = None # purely for intellisense
        self.userMessage = message
        
        # // feedback button
        # create button
        self.feedbackButton = discord.ui.Button(
            label = random.choice(["Teach me a response"]),
            style = discord.ButtonStyle.green,
            emoji = "👩‍🏫"
        )

        # callback
        self.feedbackButton.callback = self.feedbackButtonCallback
        
        # add
        self.add_item(self.feedbackButton)
        
        # // report response button
        # create button
        self.reportButton = discord.ui.Button(
            label = "Report response",
            style = discord.ButtonStyle.red,
            emoji = "🤬"
        )

        # callback
        self.reportButton.callback = self.reportButtonCallback
        
        # add
        self.add_item(self.reportButton)
        
        # // discord invite button
        # create button
        self.inviteButton = discord.ui.Button(
            style = discord.ButtonStyle.link,
            label = "Support Server",
            url = "https://discord.gg/2HR2awsdSt",
            emoji = "😎"
        )
        
        # add
        self.add_item(self.inviteButton)
        
    # // Discord Callbacks
    async def on_timeout(self):
        # disable items
        for item in self.children:
            # disable all buttons
            if isinstance(item, discord.ui.Button):
                # ignore url buttons
                if item.style == discord.ButtonStyle.url:
                    continue
                
                # disable button
                item.disabled = True
    
        # save changes
        return await self.message.edit(
            view = self
        )
        
    # // Custom Callbacks
    async def feedbackButtonCallback(self, interaction: discord.Interaction):
        return await interaction.response.send_modal(ui.modals.teach())
    
    async def reportButtonCallback(self, interaction: discord.Interaction):
        # to prevent more reports coming in
        self.reportButton.disabled = True

        await self.message.edit(
            view = self
        )

        # notify user that the report has been sent        
        await interaction.response.send_modal(ui.modals.report(
            self.message,
            self.chatbotResponse
        ))