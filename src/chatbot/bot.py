# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Chatbot Bot
# // ---------------------------------------------------------------------

# // ---- Imports
from . import knowledge

import difflib
import random
import spacy
from profanity_filter import ProfanityFilter

# // ---- Main
nlp = spacy.load("en_core_web_sm")

filter = ProfanityFilter(
    nlps = {
        "en" : spacy.load("en_core_web_sm")
    }
)

nlp.add_pipe(filter.spacy_component)

class bot:
    def __init__(self, name: str, knowledgePath: str = ""):
        # chatbot name
        self.name = name
        
        # knowledge
        fileName = ("/" if knowledgePath != "" else "") + f"{name.lower()}_knowledge.json"

        self.knowledge = knowledge(knowledgeFilePath = f"{knowledgePath}{fileName}")

        # default knowledge tags
        self.knowledge.addTag("NAME", name.capitalize())
        
    def __getMatch(self, query: str, cutoff: float|int = 0.6):
        knownQueries = [knownQuery for knownQuery in self.knowledge.data]
        matches = difflib.get_close_matches(query, knownQueries, 1, cutoff)
        
        if len(matches) > 0:
            return matches[0]
        
        return None
    
    def __getAnswer(self, question: str) -> str|None:
        return random.choice(self.knowledge.data.get(question, []))
        
    def respond(self, query: str) -> tuple[str|None, bool, str|None]:
        # profanity check
        if nlp(query)._.is_profane: # wtf is this syntax
            return None, False, "profanity"
        
        # get the remembered query
        knownQuery = self.__getMatch(query)
        
        # doesn't exist, so return
        if knownQuery is None:
            return None, False, "unknown_query"
        
        # get the answer for the query
        answer = self.__getAnswer(knownQuery)
        
        # can't find one, so return
        if answer is None:
            return None, False, "no_answer"
        
        # return the answer
        return answer, True, None