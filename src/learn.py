# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Learn
# // ---------------------------------------------------------------------

# this part of the code is really silly
# it was originally supposed to be rushed code to teach the chatbot
# but then i ended up making it official and now its silly and rushed
# and all over the place

# // ----  
import chatbot
from helpers import general as helpers

# // ---- Variables
data = {}

# // ---- Functions
def add(queries: list[str]|str, answers: list[str]):
    global data
    
    if isinstance(queries, list):
        # add multiple
        for i in queries:
            data[i] = answers
    else:
        # add once
        data[queries] = answers
        
def get():
    return data

def clear():
    data.clear()

def learn(dataToLearn: dict[str, list[str]], bot: chatbot.bot, source: str = "Built-In"):
    for query, answers in dataToLearn.items():
        bot.knowledge.learn(query, answers, source)
        helpers.prettyprint.info(f"✨ | Learned responses for: {query} (Source: {source})")
        
# // ---- Main
# // information relating to the bot
# name
add(
    queries = [
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
    queries = [
        "my name is",
        "i am"
    ],
    
    answers = [
        "Nice to meet you!",
        "Great to meet you!",
        "Awesome!"
    ]
)

# likes
add(
    queries = [
        "what do you like",
        "what are your likes",
        "what is your favourite"
    ],
    
    answers = [
        "I personally love talking to idiots.",
        "I'm an avid enjoyer of communicating with others.",
        "I quite like talking to others.",
        "I like technology to be honest.",
        "Personally, I enjoy technology and messing around with it."
    ]
)

# dislikes
add(
    queries = [
        "what do you dislike",
        "what are your dislikes",
        "what is your least favourite"
    ],
    
    answers = [
        "I don't like eating... because I can't. Haha.",
        "I'm not a big fan of grass.",
        "I absolutely despise the Die Hard movies."
    ]
)

# owner
add(
    queries = [
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
    queries = [
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
    queries = [
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
    queries = [
        "how are you",
        "how are you doing",
        "hru",
        "hyd",
        "how are you feeling",
        "hows it going",
        "hows going"
    ],
 
    answers = [
        "I'm good! How about you?",
        "I'm doing alright. You?",
        "I'm doing great. You?",
        "Could be better. How about you?"
    ]
)

add(
    queries = [
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
    queries = [
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
    queries = [
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
    queries = [
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
    queries = [
        "hi",
        "hello",
        "sup",
        "whatup",
        "what's up",
        "hey",
        "howdy",
        "wassup",
        "good evening",
        "good night",
        "good morning",
        "hello [NAME]",
        "hello chatbot",
        "hi chatbot",
        "hey chatbot",
        "sup chatbot"
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
    queries = [
        "bye",
        "goodbye",
        "cya",
        "see ya",
        "see you",
        "have a good one",
        "good night"
    ],
    
    answers = [
        "Bye! Have a good one!",
        "See you!",
        "Cya!"
    ]
)