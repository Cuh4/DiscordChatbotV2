# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Discord Utils
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

# // ---- Functions
# // Permissions/Roles
def isCreator(client: discord.Client, user: discord.User):
    return client.application.owner.id == user.id

def isAdministrator(member: discord.Member):
    return member.guild_permissions.administrator

def hasRole(member: discord.Member, role_id):
    if member.get_role(role_id):
        return True
    
    return False

# // String
def truncateIfTooLong(inp: str, max: int, endPartIfLong: str = ""):
    if len(inp) > max:
        return inp[0:max - len(endPartIfLong)] + endPartIfLong

    return inp

def fullyFilter(msg: str):
    return msg.replace("`", "\\`").replace("*", "\\*").replace("~", "\\~").replace("_", "\\_")

def formattedName(user: discord.User):
    return user.name if user.discriminator == "0" else f"{user.name}#{user.discriminator}" # supports discord's new username system

def memberMention(user: discord.User):
    return f"<@{user.id}>"

def channelMention(channel: discord.TextChannel|discord.VoiceChannel|discord.ForumChannel):
    return f"<#{channel.id}>"

# // Other
def isMentioned(mentionedUsers: list[discord.User], who: discord.User):
    for i in mentionedUsers:
        if i == who:
            return True