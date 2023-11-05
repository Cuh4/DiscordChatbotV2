# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Feedback View UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import random
import chatbot

import ui

# // ---- Main
# // UI
class view(discord.ui.View):
    # // Main UI
    def __init__(self, bot: chatbot.bot):
        # // init
        super().__init__()
        
        # // feedback button
        # create button
        self.feedbackButton = discord.ui.Button(
            label = random.choice(["Funky response?", "Invalid response?", "Incorrect response?", "Bad response?", "Inconvenient response?"]),
            style = discord.ButtonStyle.danger,
            emoji = "⚠"
        )

        # callback
        self.feedbackButton.callback = self.feedbackButtonCallback
        
        # add
        self.add_item(self.feedbackButton)
        
    # // Callbacks
    async def feedbackButtonCallback(self, interaction: discord.Interaction, button: discord.ui.Button):
        return await interaction.response.send_modal(ui.modals.teach(bot))