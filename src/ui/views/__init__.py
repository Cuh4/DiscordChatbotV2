# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Views UI Init
# // ---------------------------------------------------------------------

# // Imports
import discord
from .feedbackView import view as feedback
from .failedResponseView import view as failedResponse

# // Functions
def wrap(message: discord.Message, view: discord.ui.View):
    view.message = message
    return view

class view(discord.ui.View):
    async def on_timeout(self):
        # disable items
        for item in self.children:
            # disable all buttons
            if isinstance(item, discord.ui.Button):
                # ignore url buttons
                if item.style == discord.ButtonStyle.url:
                    continue
                
                # disable button
                item.disabled = True
    
        # save changes
        return await self.message.edit(
            view = self
        )