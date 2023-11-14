# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Config
# // ---------------------------------------------------------------------

# // discord bot
botToken = "" # token of your discord bot. create a bot here: https://discord.com/developers/applications'. be sure to enable message content intents
activityText = "you." # in discord, this becomes: "Watching you."

# // chatbot specific
allowProfanity = False # whether or not to allow the bot to send messages that contain profanity, and whether or not to interact with messages that contain profanity
chatCooldown = 4 # cooldown given to each user. if a user tries to talk to the bot during the cooldown of {chatCooldown} seconds, the user will be ignored

# // ids
loadingEmoji = "<a:loadingv2:1167901026687393812>" # emoji to use for loading response message. use "\:(emoji name):" (eg: "\:some_custom_emoji:") in discord to get an emoji's id
responseReportsChannelID = 1234567 # if a user presses the "report response" button for a response, it will show up in the channel with this id

# // character limits
maxResponseLength = 700 # character limit of bot response
maxQueryLength = 150 # character limit of user messages

# [!!] Rename to config.py [!!]