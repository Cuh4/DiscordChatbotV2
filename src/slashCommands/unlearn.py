# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Restart Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import discord.app_commands

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
    async def command(interaction: discord.Interaction, query: str, removalLimit: int = 1):
        # check if the user running this command is the person who created the bot
        if not discordHelpers.utils.isCreator(client, interaction.user):
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure("Invalid permissions.")
            )
        
        # unlearn stuffs
        removedQueries = []

        for knownQuery in bot.knowledge.data.keys():
            # check if removed enough queries
            if len(removedQueries) >= removalLimit:
                break
            
            # if this query matches the desired query, remove it
            if knownQuery.lower().find(query.lower()) != -1:
                bot.knowledge.unlearn(knownQuery)
                removedQueries.append(knownQuery)
        
        # reply
        formattedRemovedQueries = discordHelpers.utils.stripHighlightMarkdown("- " + "\n- ".join(removedQueries))
        
        return await interaction.response.send_message(
            embed = discordHelpers.embeds.success(f"**Successfully unlearned responses to the following queries:**\n```{formattedRemovedQueries}```")
        )
        
    return tree.get_command("unlearn")