# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] PyChatbot Chatbot
# // ---------------------------------------------------------------------

# // ---- Imports
from . import knowledge
from . import helpers

import difflib
import random

# // ---- Main
class chatbot:
    def __init__(self, name: str, knowledgePath: str = "", confidence: float = 0.4, allowProfanity: bool = True, customKnowledge: "knowledge" = None):
        # chatbot name
        self.name = name
        
        # knowledge
        self.knowledge = customKnowledge or knowledge(name, knowledgePath)

        # default knowledge tags
        self.knowledge.addTag("NAME", name.capitalize())
        
        # properties
        self.confidence = helpers.clamp(confidence, 0, 1)
        self.profanityAllowed = allowProfanity
        
    # // helpers
    def __getQuery(self, query: str, *, overrideConfidence: int|float = None) -> tuple[str, float|int]|tuple[None, None]:
        # find a response for this query
        confidence = overrideConfidence or self.confidence
        matches = difflib.get_close_matches(query, self.knowledge.getAllQueries(), 6, confidence)

        if len(matches) > 0:
            match = matches[0]
            return match, difflib.SequenceMatcher(None, query, match).ratio() # note: might want to use "quick_ratio" since "ratio" is apparently computationally expensive
        
        # since we found nothing, let's try again with a lower confidence
        if overrideConfidence and overrideConfidence <= self.confidence / 6: # took too many tries (or confidence is 0), so lets just give up
            return None, None
        
        newConfidence = confidence / 1.25 # lower confidence slightly
        query, responseConfidence = self.__getQuery(query = query, overrideConfidence = newConfidence)
    
        return query, responseConfidence
    
    def __getResponse(self, query: str) -> str|None:
        return random.choice(self.knowledge.getResponsesForQuery(query))
        
    # // methods
    def respond(self, query: str):
        # simplify
        query = helpers.simplifyText(query)
        
        # get the remembered query
        knownQuery, responseConfidence = self.__getQuery(query)

        # doesn't exist, so return
        if knownQuery is None:
            return response(
                self,
                isSuccessful = False,
                reasonForFailure = "no_query"
            )
        
        # get a response for the query
        savedResponse = self.__getResponse(knownQuery)
        
        # can't find one, so return
        if savedResponse is None:
            return response(
                self,
                isSuccessful = False,
                reasonForFailure = "no_answer"
            )
            
        # check for profanity
        if helpers.isTextProfane(savedResponse["text"]) and not self.profanityAllowed:
            return response(
                self,
                isSuccessful = False,
                reasonForFailure = "profanity"
            )
        
        # return the answer
        return response(
            self,
            savedResponse["text"],
            savedResponse["source"],
            knownQuery,
            responseConfidence,
            savedResponse["data"]
        )
        
class response:
    def __init__(self, parent: "chatbot", text: str = "", source: str = "", query: str = "", responseConfidence: float|int = 0, data: dict[str, any] = None, *, isSuccessful: bool = True, reasonForFailure: str = ""):
        self.__chatbot = parent
        
        self.__text = text
        self.__source = source
        self.__query = query
        self.__responseConfidence = responseConfidence
        
        self.__success = isSuccessful
        self.__failureReason = reasonForFailure
        self.__savedData = data
        
    def getSavedData(self):
        return self.__savedData
        
    def getChatbot(self):
        return self.__chatbot
        
    def getText(self):
        return self.__text
    
    def getSource(self):
        return self.__source
        
    def getQuery(self):
        return self.__query
    
    def getResponseConfidence(self):
        return self.__responseConfidence
    
    def isSuccessful(self):
        return self.__success
    
    def getFailureReason(self):
        return self.__failureReason