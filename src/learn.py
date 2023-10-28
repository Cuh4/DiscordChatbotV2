# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import chatbot
from helpers import general as helpers

# // ---- Variables
data = {}

# // ---- Functions
def add(query: list[str]|str, answers: list[str]):
    global data
    
    if isinstance(query, list):
        # add multiple
        for i in query:
            data[i] = answers
    else:
        # add once
        data[query] = answers

def learn(bot: chatbot.bot):
    for query, answers in data.items():
        helpers.prettyprint.info(f"✨| Learning responses for: {query}")
        bot.knowledge.learn(query, answers)
        helpers.prettyprint.success(f"⭐ | Learned responses for: {query}")
        
# // ---- Main
# // information relating to the bot
# name
add(
    query = [
        "whats your name",
        "what are you called"
    ],
    
    answers = [
        "I am [NAME]. What is your name?",
        "My name is [NAME].",
        "I go by [NAME]."
    ]
)

add(
    query = [
        "my name is",
        "i am"
    ],
    
    answers = [
        "Nice to meet you!",
        "Great to meet you!",
        "Awesome!"
    ]
)

# owner
add(
    query = [
        "who created you",
        "who is your creator",
        "who are your parents"
    ],
    
    answers = [
        "[AUTHOR] created me.",
        "I was created by [AUTHOR]."
    ]
)

# gender
add(
    query = [
        "what is your gender",
        "are you a girl",
        "are you a guy",
        "are you a boy",
        "are you a woman",
        "are you a man",
        "what is your sex"
    ],
    
    answers = [
        "I am a [GENDER].",
        "I'm [GENDER]. You?"
    ]
)

add(
    query = [
        "i am a man",
        "i am a guy",
        "i am a girl",
        "i am a boy",
        "i am a woman",
        "my gender is",
        "my sex is"
    ],
    
    answers = [
        "Nice!",
        "Splendid!",
        "Awesome!"
    ]
)

# // general conversation (greetings, goodbyes, small talk)
# "how are you"
add(
    query = [
        "how are you",
        "how are you doing",
        "hru",
        "hyd",
        "how are you feeling"        
    ],
 
    answers = [
        "I'm good! How about you?",
        "I'm doing alright. You?",
        "I'm doing great. You?",
        "Could be better. How about you?"
    ]
)

add(
    query = [
        "doing good",
        "doing great",
        "doing awesome",
        "doing fantastic",
    ],
    
    answers = [
        "Awesome to hear!",
        "Glad to hear!",
        "That's amazing!"
    ]
)

# "what are you up to"
add(
    query = [
        "im up to",
        "im doing"
    ],
    
    answers = [
        "Nice! Keep it up!",
        "Great! Have fun!"
    ]
)

# "where are you"
add(
    query = [
        "where are you",
        "where do you live",
        "where are you located"
    ],
    
    answers = [
        "I don't live anywhere. I'm a bot, silly.",
        "I'm not a human, so I can't really live anywhere.",
        "I'm a bot, silly.",
        "I live in a... computer?"
    ]
)

add(
    query = [
        "i live in",
        "im located"
    ],
    
    answers = [
        "Be careful sharing that information online!",
        "Be careful with what you say on here.",
        "Awesome, but be careful with what you share on here.",
        "Nice, but it's probably a good idea to not share your location with others."
    ]
)

# greetings
add(
    query = [
        "hi",
        "hello",
        "sup",
        "whatup",
        "what's up",
        "hey",
        "howdy",
        "wassup"
    ], 

    answers = [
        "Hello! How are you?",
        "Hey! How are we doing?",
        "Hi! What are you up to?",
        "Hello! What are you up to?"
    ]
)

# goodbyes
add(
    query = [
        "bye",
        "goodbye",
        "cya",
        "see ya",
        "see you"
    ],
    
    answers = [
        "Bye! Have a good one!",
        "See you!",
        "Cya!"
    ]
)

add(
    query = [
        "you?",
        "how about you?",
        "and you?"
    ],
    
    answers = [
        "Sorry, could you provide more information? I can't remember conversations well.",
        "Could you provide more information?",
        "Sorry, what do you mean?"
    ]
)