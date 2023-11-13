# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Teachings Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import pychatbot
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
    chatbot: pychatbot.chatbot = helpers.globals.get("chatbot")

    # // main command
    # slash command
    @tree.command(
        name = "teachings",
        description = "Displays everything you have taught the chatbot."
    )
    async def command(interaction: discord.Interaction):
        # get responses made by this person
        responses = chatbot.knowledge.getResponsesWithSource(interaction.user.id)
        
        # format them
        formattedQueries = [helpers.misc.truncateIfTooLong(discordHelpers.utils.stripHighlightMarkdown(response.getQuery()), 50) for response in responses][:25] if len(responses) > 0 else "None."
        responsesCreated = len(responses)
        
        # send
        interaction.response.send_message(
            embed = discordHelpers.embeds.info(f"You have taught the bot responses to the following {responsesCreated} queries:\n```{formattedQueries}```")
        )

# // start command
command()