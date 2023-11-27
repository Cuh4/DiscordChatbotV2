# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Response Embed UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

from modules import pychatbot
from modules import discord as discordHelpers
from modules import general as helpers

# // ---- Main
# // UI
def embed(chatbot: pychatbot.chatbot, text: str, source: str, responseConfidence: float|int, knowledgeID: int, icon_url: str):
    responseEmbed = discord.Embed(
            description = f"> :speech_balloon: | `{chatbot.name}` | **{text}**",
            color = discord.Colour.from_rgb(125, 255, 125)
        )
        
    responseEmbed.set_footer(text = f"Response from {source} | Response Confidence: {round(responseConfidence * 100, 1)}% | Knowledge ID: {knowledgeID}", icon_url = icon_url)
    return responseEmbed