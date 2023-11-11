# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Restart Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import chatbot as _chatbot
import difflib
from helpers import general as helpers
from helpers import discord as discordHelpers

# // ---- Main
# // create command
def command():
    # // get vars
    # discord-related
    client: discord.Client = helpers.globals.get("client")
    tree: discord.app_commands.CommandTree = helpers.globals.get("commandTree")

    # other
    chatbot: _chatbot.bot = helpers.globals.get("chatbot")

    # // main command
    # match quality choices
    matchQualityChoices = [
        discord.app_commands.Choice(
            name = "High",
            value = 0.9
        ),
        
        discord.app_commands.Choice(
            name = "Medium",
            value = 0.7
        ),
        
        discord.app_commands.Choice(
            name = "Low",
            value = 0.5
        )
    ]

    # slash command
    @tree.command(
        name = "unlearn",
        description = "Removes the bot's knowledge on a query."
    )
    @discord.app_commands.describe(
        query = "The query to remove from the bot's knowledge.",
        match_quality = "Decides how close a query must match to your desired query when unlearning.",
        removal_limit = "The amount of queries to remove that match your desired query."
    )
    @discord.app_commands.choices(match_quality = matchQualityChoices)
    async def command(interaction: discord.Interaction, query: str, match_quality: discord.app_commands.Choice[float] = matchQualityChoices[0].value, removal_limit: int = 1):
        # check if the user running this command is the person who created the bot
        if not discordHelpers.utils.isCreator(client, interaction.user):
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure("Invalid permissions.")
            )
        
        # unlearn stuffs
        removedQueries = []

        for knownQuery in chatbot.knowledge.data.copy().keys(): # copy knowledge data to prevent getting the "dict changed size bla bla" error
            # check if removed enough queries
            if len(removedQueries) >= removal_limit:
                break
            
            # if this query matches the desired query, remove it
            match = difflib.SequenceMatcher(None, knownQuery.lower(), query.lower()).quick_ratio()
    
            if match >= match_quality.value:
                chatbot.knowledge.unlearn(knownQuery)
                removedQueries.append(knownQuery + f" [{round(match * 100, 1)}% match]")
        
        # reply
        formattedRemovedQueries = discordHelpers.utils.stripHighlightMarkdown("- " + "\n- ".join(removedQueries)) if len(removedQueries) >= 1 else "N/A"
        
        return await interaction.response.send_message(
            embed = discordHelpers.embeds.success(f"**Successfully unlearned responses to the following queries:**\n```{formattedRemovedQueries}```")
        )
        
    return tree.get_command("unlearn")

# // start command
command()