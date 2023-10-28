# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Slash Commands Init
# // ---------------------------------------------------------------------

# // Imports
import discord
from discord.interactions import Interaction

from helpers import discord as discordHelpers
import chatbot as cbot
import learn

# // Main
def command(tree: discord.app_commands.CommandTree, chatbot: cbot.bot):
    # learn ui
    class failedUI(discord.ui.Modal, title = "Failed"):
        button = discord.ui.Button(
            label = "Something went wrong. Please try again.",
            emoji = "⚠",
            style = discord.ButtonStyle.danger
        )
    
    class learnUI(discord.ui.Modal, title = "Teach Chatbot"):
        queries = discord.ui.TextInput(
            label = "Queries (split by new line, exclude grammar)",
            style = discord.TextStyle.long,
            placeholder = "how are you"
        )
        
        answers = discord.ui.TextInput(
            label = "Answers (split by new line, include grammar)",
            style = discord.TextStyle.paragraph,
            placeholder = "I'm great!\nI'm decent.\nI'm alright!"
        )
        
        async def on_submit(self, interaction: Interaction):
            if self.answers.value == "" or self.queries.value == "":
                return await self.on_error(interaction, Exception())
            
            queries = self.queries.value.split("\n")
            answers = self.answers.value.split("\n")
            
            for query in queries:
                learn.learn(
                    data = {
                        query : answers
                    },
                    
                    bot = chatbot
                )
                
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.success("Successfully taught the chatbot.")
            )
        
        async def on_error(self, interaction: Interaction, _: Exception):
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.success("Failed to teach the chatbot.")
            )
    
    # slash command
    @tree.command(
        name = "learn",
        description = "Teach the chatbot a response for a query."
    )
    async def command(interaction: discord.Interaction):
        return await interaction.response.send_modal(learnUI())