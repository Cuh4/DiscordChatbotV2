# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Feedback View UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import random
import chatbot

import ui

# // ---- Main
class view(discord.ui.View):
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
        async def feedbackButtonCallback(self, interaction: discord.Interaction, button: discord.ui.Button):
            return await interaction.response.send_modal(ui.modals.teach(bot))
        
        self.feedbackButton.callback = feedbackButtonCallback
        
        # add
        self.add_item(self.feedbackButton)