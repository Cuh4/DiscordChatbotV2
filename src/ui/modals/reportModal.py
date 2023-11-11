# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Report Modal UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import chatbot as _chatbot
from events import events
from helpers import discord as discordHelpers
from helpers import general as helpers

# // ---- Main
# // UI
class modal(discord.ui.Modal):
    # // Main UI
    def __init__(self, message: discord.Message, chatbotResponse: _chatbot.response):
        # // init
        super().__init__(title = "Report Response")
        
        # // properties
        self.message = message
        self.chatbotResponse = chatbotResponse

        # // ui
        # report type
        self.reportType = discord.ui.Select(
            options = [
                discord.SelectOption(
                    label = "Response is inappropriate",
                    emoji = "😢"
                ),
                
                discord.SelectOption(
                    label = "Response is hurtful",
                    emoji = "😡"
                ),
                
                discord.SelectOption(
                    label = "Response doesn't match",
                    emoji = "🤔",
                    default = True
                )
            ],

            max_values = 3,
            placeholder = "not_matching"
        )

        self.add_item(self.reportType)

    # // Callbacks
    async def on_submit(self, interaction: discord.Interaction):
        # expired, so ignore
        if interaction.is_expired():
            return
        
        # submit report
        await events.on_report.asyncFire({
            "message" : self.message,
            "response" : self.chatbotResponse,
            "reasons" : self.reportType.values
        })
        
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