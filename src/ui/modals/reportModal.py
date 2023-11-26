# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Report Modal UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import pychatbot
from ui.modals import template
from helpers import discord as discordHelpers
from helpers import general as helpers

# // ---- Main
# // UI
class modal(template):
    # // Main UI
    def __init__(self, message: discord.Message, chatbotResponse: pychatbot.chatbotResponse):
        # // init
        super().setup("Report Chatbot Response")
        
        # // properties
        self.message = message
        self.chatbotResponse = chatbotResponse

        # // ui
        # report message
        self.reportMessage = discord.ui.TextInput(
            label = "Report Message",
            placeholder = "Enter your report message here, e.g: 'The chatbot disrespected me!'",
            min_length = 10,
            max_length = 300,
            style = discord.TextStyle.paragraph
        )

        self.add_item(self.reportMessage)

    # // Callbacks
    async def on_submit(self, interaction: discord.Interaction):
        # expired, so ignore
        if interaction.is_expired():
            return
        
        # submit report
        await helpers.events.getSavedEvent("on_report").asyncFire(
            message = self.message,
            response = self.chatbotResponse,
            report = self.reportMessage.value,
            user = interaction.user
        )
        
        # send message
        return await interaction.response.send_message(
            embed = discordHelpers.embeds.success("Your report has been sent. :grin:"),
            ephemeral = True
        )

    async def on_error(self, interaction: discord.Interaction, _: Exception):
        return await interaction.response.send_message(
            embed = discordHelpers.embeds.failure("Failed to report."),
            ephemeral = True
        )