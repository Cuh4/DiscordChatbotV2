# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Unlearn Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import difflib

from gevent import idle

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
        name = "unlearn",
        description = "Remove a piece of knowledge from the bot by its ID."
    )
    @discord.app_commands.describe(
        id = "The ID of the knowledge.",
    )
    async def command(interaction: discord.Interaction, id: int):
        # check if the user running this command is the person who created the bot
        if not discordHelpers.utils.isCreator(client, interaction.user):
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure("Invalid permissions.")
            )
            
        # get knowledge
        knowledge = chatbot.knowledgeBase.getKnowledgeWithID(id)
        
        # check if it doesnt exist
        if knowledge is None:        
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure("A piece of knowledge with the specified ID could not be found.")
            )
        
        # remove it
        chatbot.knowledgeBase.unlearn(id)
        
        # reply
        knowledgeQuery = discordHelpers.utils.stripHighlightMarkdown(knowledge.getQuery()).replace("\n", "\\n")
        knowledgeResponse = discordHelpers.utils.stripHighlightMarkdown(knowledge.getResponse()).replace("\n", "\\n")
        
        return await interaction.response.send_message(
            embed = discordHelpers.embeds.success(f"**Successfully unlearned the specified knowledge.**\n```Query: {knowledgeQuery}```\n```Response: {knowledgeResponse}```")
        )

# // start command
command()