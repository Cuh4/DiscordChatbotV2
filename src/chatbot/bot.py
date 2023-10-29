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
    def __init__(self, name: str, knowledgePath: str = "", confidence: float = 0.4):
        # chatbot name
        self.name = name
        
        # knowledge
        fileName = ("/" if knowledgePath != "" else "") + f"{name.lower()}_knowledge.json"

        self.knowledge = knowledge(knowledgeFilePath = f"{knowledgePath}{fileName}")

        # default knowledge tags
        self.knowledge.addTag("NAME", name.capitalize())
        
        # properties
        self.confidence = confidence
        
    def isTextProfane(self, string: str):
        return nlp(string)._.is_profane or string.find("https://") != -1 or string.find("http://") != -1
        
    def __simplifyText(self, string: str):
        punctuation = [*",.?;:-'!\""]
        
        for i in punctuation:
            string = string.replace(i, "")
            
        return string.lower()
        
    def __getMatch(self, query: str):
        matches = difflib.get_close_matches(query, self.knowledge.getAllQueries(), 1, self.confidence)
        
        if len(matches) > 0:
            return matches[0]
        
        return None
    
    def __getAnswer(self, query: str) -> str|None:
        return random.choice(self.knowledge.getAnswersForQuery(query))
        
    def respond(self, query: str) -> tuple[str|None, str|None, str|None, bool, str|None]:
        # simplify
        query = self.__simplifyText(query)
        
        # profanity check
        if self.isTextProfane(query): # wtf is this syntax
            return None, None, False, "profanity"
        
        # get the remembered query
        knownQuery = self.__getMatch(query)
        
        # doesn't exist, so return
        if knownQuery is None:
            return None, None, False, "unknown_query"
        
        # get the answer for the query
        answer = self.__getAnswer(knownQuery)
        
        # can't find one, so return
        if answer is None:
            return None, None, False, "no_answer"
        
        # return the answer
        return answer["answer"], answer["source"], knownQuery, True, None