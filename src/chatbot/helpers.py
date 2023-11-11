# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Chatbot Helpers
# // ---------------------------------------------------------------------

# // ---- Imports
import spacy
from profanity_filter import ProfanityFilter

# // ---- Variables
nlp = spacy.load("en_core_web_sm")

filter = ProfanityFilter(
    nlps = {
        "en" : spacy.load("en_core_web_sm")
    }
)

nlp.add_pipe(filter.spacy_component)

# // ---- Functions
def isTextProfane(string: str):
    return nlp(string)._.is_profane or string.find("https://") != -1 or string.find("http://") != -1

def clamp(num: float|int, min: float|int, max: float|int):
    if num < min:
        return min
    
    if num > max:
        return max
    
    return num