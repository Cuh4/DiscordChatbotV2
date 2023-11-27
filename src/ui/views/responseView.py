# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Response View UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import random

from modules import pychatbot
from ui.views import template
from ui import modals

# // ---- Main
# // UI
class view(template):
    # // Main UI
    def __init__(self, response: pychatbot.chatbotResponse, userMessage: discord.Message):
        # // init
        super().setup()
        
        # // class properties
        self.chatbotResponse = response
        self.userMessage = userMessage
        
        # // teach button
        # create button
        self.teachButton = discord.ui.Button(
            label = random.choice(["Teach Me A Response"]),
            style = discord.ButtonStyle.green,
            emoji = "👩‍🏫"
        )

        # callback
        self.teachButton.callback = self.teachButtonCallback
        
        # add
        self.add_item(self.teachButton)
        
        # // report response button
        # create button
        self.reportButton = discord.ui.Button(
            label = "Report Response",
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
    async def teachButtonCallback(self, interaction: discord.Interaction):
        return await interaction.response.send_modal(modals.teach())
    
    async def reportButtonCallback(self, interaction: discord.Interaction):
        # to prevent more reports coming in
        self.reportButton.disabled = True

        await self.message.edit(
            view = self
        )

        # notify user that the report has been sent        
        await interaction.response.send_modal(modals.report(
            self.userMessage,
            self.chatbotResponse
        ))