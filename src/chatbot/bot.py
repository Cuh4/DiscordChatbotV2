# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Chatbot Bot
# // ---------------------------------------------------------------------

# // ---- Imports
from . import knowledge

import difflib
import random
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

# // ---- Main
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
        
    def __simplifyText(self, string: str):
        punctuation = [*",.?;:-'!\""]
        
        for i in punctuation:
            string = string.replace(i, "")
            
        return string.lower()
        
    def __getQuery(self, query: str, *, overrideConfidence: int|float = None) -> str|None:
        # find a response for this query
        matches = difflib.get_close_matches(query, self.knowledge.getAllQueries(), 6, overrideConfidence or self.confidence)

        if len(matches) > 0:
            return matches[0]
        
        # since we found nothing, let's try again with a lower confidence
        if overrideConfidence and overrideConfidence < self.confidence / 6: # took too many tries, so lets just give up
            return
        
        newConfidence = (overrideConfidence if overrideConfidence else self.confidence) / 1.25
        return self.__getQuery(query = query, overrideConfidence = newConfidence)
    
    def __getResponse(self, query: str) -> str|None:
        return random.choice(self.knowledge.getAnswersForQuery(query))
        
    def respond(self, query: str):
        # simplify
        query = self.__simplifyText(query)
        
        # get the remembered query
        knownQuery = self.__getQuery(query)

        # doesn't exist, so return
        if knownQuery is None:
            return response(
                isSuccessful = False,
                reasonForFailure = "no_query"
            )
        
        # get a response for the query
        answer = self.__getResponse(knownQuery)
        
        # can't find one, so return
        if answer is None:
            return response(
                isSuccessful = False,
                reasonForFailure = "no_answer"
            )
        
        # return the answer
        return response(
            answer["text"],
            answer["source"],
            knownQuery
        )
        
class response:
    def __init__(self, text: str = None, source: str = None, query: str = None, *, isSuccessful: bool = True, reasonForFailure: str = ""):
        self.text = text
        self.source = source
        self.query = query
        
        self.success = isSuccessful
        self.failureReason = reasonForFailure