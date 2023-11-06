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
    def __init__(self, bot: chatbot.bot, response: chatbot.response):
        # // init
        super().__init__()
        
        # // class properties
        self.bot = bot
        self.botResponse = response
        
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
        self.reportButton = discord.ui.Button(
            label = "Report response",
            style = discord.ButtonStyle.red,
            emoji = "🤬"
        )

        # callback
        self.reportButton.callback = self.reportButtonCallback
        
        # add
        self.add_item(self.reportButton)
        
    # // Callbacks
    async def feedbackButtonCallback(self, interaction: discord.Interaction):
        return await interaction.response.send_modal(ui.modals.teach(self.bot))
    
    async def reportButtonCallback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed = discordHelpers.embeds.success("Successfully reported this bot response."),
            ephemeral = True
        )
        
        await helpers.events.getSavedEvent("report_response").asyncFire(interaction.user, self.botResponse)