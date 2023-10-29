# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Teach Slash Command
# // ---------------------------------------------------------------------

# // Imports
import discord
from discord.interactions import Interaction

from helpers import general as helpers
from helpers import discord as discordHelpers
import chatbot as cbot
import config
import learn

# // Main
def command(client: discord.Client, tree: discord.app_commands.CommandTree, chatbot: cbot.bot):
    # learn ui
    class teachUI(discord.ui.Modal, title = "Teach Chatbot"):
        queries = discord.ui.TextInput(
            label = "Queries (split by new line, exclude grammar)",
            style = discord.TextStyle.paragraph,
            placeholder = "how are you",
            min_length = 5
        )
        
        answers = discord.ui.TextInput(
            label = f"Answers (split by new line, include grammar)",
            style = discord.TextStyle.paragraph,
            placeholder = f"Each answer has a character limit of {config.maxResponseLength}.\nI'm great!\nI'm alright!",
            min_length = 5
        )
        
        async def on_submit(self, interaction: Interaction):
            if helpers.misc.isStringEmpty(self.queries.value) or helpers.misc.isStringEmpty(self.answers.value):
                return await self.on_error(interaction, Exception())
            
            # get needed vars
            queries = self.queries.value.split("\n")
            answers = self.answers.value.split("\n")
            
            # pack both vars into a dict
            toLearn = {}
            
            for i in queries:
                toLearn[i] = answers
            
            # teach the chatbot
            learn.learn(
                dataToLearn = toLearn,
                bot = chatbot,
                source = "@" + discordHelpers.utils.formattedName(interaction.user)
            )
                
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.success("Successfully taught the chatbot.")
            )
        
        async def on_error(self, interaction: Interaction, _: Exception):
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure("Failed to teach the chatbot.")
            )
    
    # slash command
    @tree.command(
        name = "teach",
        description = "Teach the chatbot responses for queries."
    )
    async def command(interaction: discord.Interaction):
        return await interaction.response.send_modal(teachUI())
    
    return tree.get_command("teach")