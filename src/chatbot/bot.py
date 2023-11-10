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

def clamp(num: float|int, min: float|int, max: float|int):
    if num < min:
        return min
    
    if num > max:
        return max
    
    return num

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
        self.confidence = clamp(confidence, 0, 1)
        
    def __simplifyText(self, string: str):
        punctuation = [*",.?;:-'!\""]
        
        for i in punctuation:
            string = string.replace(i, "")
            
        return string.lower()
        
    def __getQuery(self, query: str, *, overrideConfidence: int|float = None) -> str|None:
        # find a response for this query
        confidence = overrideConfidence or self.confidence
        matches = difflib.get_close_matches(query, self.knowledge.getAllQueries(), 6, confidence)

        if len(matches) > 0:
            return matches[0], confidence
        
        # since we found nothing, let's try again with a lower confidence
        if overrideConfidence and overrideConfidence <= self.confidence / 6: # took too many tries (or confidence is 0), so lets just give up
            return None, None
        
        newConfidence = confidence / 1.25 # lower confidence slightly
        query, responseConfidence = self.__getQuery(query = query, overrideConfidence = newConfidence)
    
        return query, responseConfidence
    
    def __getResponse(self, query: str) -> str|None:
        return random.choice(self.knowledge.getResponsesForQuery(query))
        
    def respond(self, query: str):
        # simplify
        query = self.__simplifyText(query)
        
        # get the remembered query
        knownQuery, confidence = self.__getQuery(query)

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
            knownQuery,
            confidence
        )
        
class response:
    def __init__(self, text: str = None, source: str = None, query: str = None, responseConfidence: float|int = None, *, isSuccessful: bool = True, reasonForFailure: str = ""):
        self.text = text
        self.source = source
        self.query = query
        self.responseConfidence = responseConfidence
        
        self.success = isSuccessful
        self.failureReason = reasonForFailure
        
    def getText(self):
        return self.text
    
    def getSource(self):
        return self.source
        
    def getQuery(self):
        return self.query
    
    def getResponseConfident(self):
        return self.responseConfidence
    
    def isSuccessful(self):
        return self.success, self.failureReason