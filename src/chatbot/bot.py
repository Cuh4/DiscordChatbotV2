# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Chatbot Bot
# // ---------------------------------------------------------------------

# // ---- Imports
from . import knowledge
from . import helpers

import difflib
import random

# // ---- Main
class bot:
    def __init__(self, name: str, knowledgePath: str = "", confidence: float = 0.4, allowProfanity: bool = True):
        # chatbot name
        self.name = name
        
        # knowledge
        fileName = ("/" if knowledgePath != "" else "") + f"{name.lower()}_knowledge.json"

        self.knowledge = knowledge(knowledgeFilePath = f"{knowledgePath}{fileName}")

        # default knowledge tags
        self.knowledge.addTag("NAME", name.capitalize())
        
        # properties
        self.confidence = helpers.clamp(confidence, 0, 1)
        self.profanityAllowed = allowProfanity
        
    # // helpers
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
            return matches[0], confidence / self.confidence
        
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
        savedResponse = self.__getResponse(knownQuery)
        
        # can't find one, so return
        if savedResponse is None:
            return response(
                isSuccessful = False,
                reasonForFailure = "no_answer"
            )
            
        # check for profanity
        if helpers.isTextProfane(savedResponse["text"]) and not self.profanityAllowed:
            return response(
                isSuccessful = False,
                reasonForFailure = "profanity"
            )
        
        # return the answer
        return response(
            savedResponse["text"],
            savedResponse["source"],
            knownQuery,
            confidence
        )
        
class response:
    def __init__(self, text: str = None, source: str = None, query: str = None, responseConfidence: float|int = None, *, isSuccessful: bool = True, reasonForFailure: str = ""):
        self.__text = text
        self.__source = source
        self.__query = query
        self.__responseConfidence = responseConfidence
        
        self.__success = isSuccessful
        self.__failureReason = reasonForFailure
        
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