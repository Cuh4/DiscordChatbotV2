# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Teach Modal UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import config
from helpers import general as helpers
from helpers import discord as discordHelpers
import pychatbot
import learn

# // ---- Main
# // UI
class modal(discord.ui.Modal):
    # // Main UI
    def __init__(self):
        # // init
        super().__init__(title = "Teach Chatbot")

        # // ui
        # queries input
        self.queries = discord.ui.TextInput(
            label = "Queries (split by new line, exclude grammar)",
            style = discord.TextStyle.paragraph,
            placeholder = "how are you",
            min_length = 5,
            max_length = 1000
        )
        self.add_item(self.queries)

        # answers input
        self.answers = discord.ui.TextInput(
            label = f"Answers (split by new line, include grammar)",
            style = discord.TextStyle.paragraph,
            placeholder = f"Each answer has a character limit of {config.maxResponseLength}.\nI'm great!\nI'm alright!",
            min_length = 5,
            max_length = 1000
        )
        self.add_item(self.answers)

    # // Callbacks
    async def on_submit(self, interaction: discord.Interaction):
        if helpers.misc.doesStringOnlyContainLetter(self.queries.value, " ") or helpers.misc.doesStringOnlyContainLetter(self.answers.value, " "):
            return await self.on_error(interaction, Exception())
        
        if interaction.is_expired():
            return
        
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
            bot = helpers.globals.get("chatbot"),
            source = interaction.user.id,
            data = {
                "is_created_by_discord_user" : True,
                "cached_username" : interaction.user.name,
                "user_id" : interaction.user.id
            }
        )

        # set up text
        filteredAnswers = discordHelpers.utils.stripHighlightMarkdown("- " + "\n- ".join(answers)) if len(answers) >= 1 else "N/A"
        filteredQueries = discordHelpers.utils.stripHighlightMarkdown("- " + "\n- ".join(queries)) if len(queries) >= 1 else "N/A"
        
        # censor text if needed
        filteredAnswers = pychatbot.helpers.censorProfaneText(filteredAnswers)
        filteredQueries = pychatbot.helpers.censorProfaneText(filteredQueries)
        
        # send success message
        return await interaction.response.send_message(
            embed = discordHelpers.embeds.success(f"**The bot will now reply with:**\n```{helpers.misc.truncateIfTooLong(filteredAnswers, 200)}```\n**to:**\n```{helpers.misc.truncateIfTooLong(filteredQueries, 200)}```")
        )

    async def on_error(self, interaction: discord.Interaction, _: Exception):
        return await interaction.response.send_message(
            embed = discordHelpers.embeds.failure("Failed to teach the chatbot."),
            ephemeral = True
        )