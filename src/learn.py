# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Learn
# // ---------------------------------------------------------------------

# this part of the code is really silly
# it was originally supposed to be rushed code to teach the chatbot
# but then i ended up making it official and now its silly and rushed
# and all over the place

# // ----  
import pychatbot
from helpers import general as helpers

# // ---- Variables
defaults = {}

# // ---- Functions
def addToDefaults(queries: list[str], answers: list[str]):
    for query in queries:
        defaults[query] = answers
        
def getDefaults():
    return defaults

def clearDefaults():
    defaults.clear()

def learn(responsesToLearn: dict[str, list[str]], chatbot: pychatbot.chatbot, source: str = "Built-In", data: dict[str, any] = {}):
    for query, responses in responsesToLearn.items():
        chatbot.knowledge.learn(
            query = query,
            responses = responses,
            source = source,
            data = data
        )

        helpers.prettyprint.info(f"✨ | Learned responses for: {query} (Source: {source})")
        
# // ---- Main
# // chatbot interests
# likes
addToDefaults(
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
addToDefaults(
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

# gender
addToDefaults(
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
addToDefaults(
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

addToDefaults(
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
addToDefaults(
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
addToDefaults(
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

addToDefaults(
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
addToDefaults(
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
        "sup chatbot",
        "i am",
        "my name is"
    ], 

    answers = [
        "Hello! How are you?",
        "Hey! How are we doing?",
        "Hi! What are you up to?",
        "Hello! What are you up to?"
    ]
)

# goodbyes
addToDefaults(
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