# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Teach Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
from discord.interactions import Interaction

from helpers import general as helpers
from helpers import discord as discordHelpers
import chatbot as __chatbot
import config
import learn

# // ---- Main
# // UI
class teachModal(discord.ui.Modal):
    def __init__(self, chatbot: __chatbot.bot):
        self.chatbot = chatbot

        self.queries = discord.ui.TextInput(
            label = "Queries (split by new line, exclude grammar)",
            style = discord.TextStyle.paragraph,
            placeholder = "how are you",
            min_length = 5
        )

        self.answers = discord.ui.TextInput(
            label = f"Answers (split by new line, include grammar)",
            style = discord.TextStyle.paragraph,
            placeholder = f"Each answer has a character limit of {config.maxResponseLength}.\nI'm great!\nI'm alright!",
            min_length = 5
        )
        
        super().__init__(title = "Teach Chatbot")

    async def on_submit(self, interaction: Interaction):
        if helpers.misc.doesStringOnlyContainLetter(self.queries.value, " ") or helpers.misc.doesStringOnlyContainLetter(self.answers.value, " "):
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
            bot = self.chatbot,
            source = f"@{discordHelpers.utils.formattedName(interaction.user)}"
        )

        # response
        filteredAnswers = discordHelpers.utils.stripMarkdown("- " + "\n- ".join(answers))
        filteredQueries = discordHelpers.utils.stripMarkdown("- " + "\n- ".join(queries))
        
        return await interaction.response.send_message(
            embed = discordHelpers.embeds.success(f"**The bot will now reply with:**\n```{helpers.misc.truncateIfTooLong(filteredAnswers, 200)}```\n**to:**\n```{helpers.misc.truncateIfTooLong(filteredQueries, 200)}```")
        )

    async def on_error(self, interaction: Interaction, _: Exception):
        return await interaction.response.send_message(
            embed = discordHelpers.embeds.failure("Failed to teach the chatbot.")
        )

# // Command
def command(client: discord.Client, tree: discord.app_commands.CommandTree, chatbot: __chatbot.bot):
    # slash command
    @tree.command(
        name = "teach",
        description = "Teach the chatbot responses for queries."
    )
    async def command(interaction: discord.Interaction):
        return await interaction.response.send_modal(teachModal(chatbot))
    
    return tree.get_command("teach")