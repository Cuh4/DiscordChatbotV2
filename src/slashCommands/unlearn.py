# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Restart Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import chatbot as _chatbot
from helpers import general as helpers
from helpers import discord as discordHelpers

# // ---- Main
# // Command
def command(client: discord.Client, tree: discord.app_commands.CommandTree, bot: _chatbot.bot):
    # slash command
    @tree.command(
        name = "unlearn",
        description = "Removes the bot's knowledge on a query."
    )
    @discord.app_commands.describe(
        query = "The query to remove from the bot's knowledge.",
        removal_limit = "The amount of queries to remove that match your desired query."
    )
    async def command(interaction: discord.Interaction, query: str, removal_limit: int = 1):
        # check if the user running this command is the person who created the bot
        if not discordHelpers.utils.isCreator(client, interaction.user):
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure("Invalid permissions.")
            )
        
        # unlearn stuffs
        removedQueries = []

        for knownQuery in bot.knowledge.data.copy().keys():
            # check if removed enough queries
            if len(removedQueries) >= removal_limit:
                break
            
            # if this query matches the desired query, remove it
            if knownQuery.lower().find(query.lower()) != -1:
                bot.knowledge.unlearn(knownQuery)
                removedQueries.append(knownQuery)
        
        # reply
        formattedRemovedQueries = discordHelpers.utils.stripHighlightMarkdown("- " + "\n- ".join(removedQueries)) if len(removedQueries) >= 1 else "N/A"
        
        return await interaction.response.send_message(
            embed = discordHelpers.embeds.success(f"**Successfully unlearned responses to the following queries:**\n```{formattedRemovedQueries}```")
        )
        
    return tree.get_command("unlearn")