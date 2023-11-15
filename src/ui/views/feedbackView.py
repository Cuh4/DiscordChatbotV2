# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Feedback View UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import random

import pychatbot
import ui

# // ---- Main
# // UI
class view(ui.views.view):
    # // Main UI
    def __init__(self, response: pychatbot.chatbotResponse, userMessage: discord.Message):
        # // init
        super().__init__(timeout = 30)
        
        # // class properties
        self.chatbotResponse = response
        self.message: discord.Message = None # purely for intellisense
        self.userMessage = userMessage
        
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
            self.userMessage,
            self.chatbotResponse
        ))