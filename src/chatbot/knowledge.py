# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Chatbot Knowledge
# // ---------------------------------------------------------------------

# // ---- Imports
import json
import os

# // ---- Main
class knowledge:
    def __init__(self, knowledgeFilePath: str):
        # properties
        self.path = knowledgeFilePath
        self.tags = {}
        
        # create knowledge file if it doesnt exist
        if not self.fileExists():
            self.save({})
            
        # keep data stored
        self.data = self.read()
        
    def __tagName(self, name: str):
        return f"[{name}]"
        
    def addTag(self, tagName: str, tag: str):
        self.tags[self.__tagName(tagName)] = tag
        
    def removeTag(self, tagName: str):
        self.tags.pop(self.__tagName(tagName))
        
    def getAllQueries(self):
        return list(self.data.keys())
    
    def getResponsesForQuery(self, query: str) -> list[dict[str, str]]:
        return self.data.get(query, [])
    
    def unlearn(self, query: str):
        self.data.pop(query, None)
        self.save(self.data)
        
    def learn(self, query: str, responses: list[str], source: str):
        # tags system
        responses = responses.copy() # prevent modifying original
    
        for index, __response in enumerate(responses):
            for tagName, tag in self.tags.items():
                __response = __response.replace(tagName, tag)
                
            responses[index] = {
                "source" : source,
                "text" : __response
            }
        
        # retrieve saved knowledge
        data = self.read()
        
        # get all responses for the specified query
        responsesFromData = data.get(query, responses)
        
        # add the new responses if they aren't already added
        for __response in responses:
            if __response not in responsesFromData: # prevent adding two of the same response
                responsesFromData.append(__response)
            
        data[query] = responsesFromData # apply changes
        
        # save changes
        self.save(data)
        self.data = data
        
    def save(self, data: dict):
        with open(self.path, "w") as file:
            json.dump(
                obj = data,
                fp = file,
                indent = 6
            )
            
    def read(self) -> dict[str, list[str]]:
        with open(self.path, "r") as file:
            return json.load(
                fp = file
            )
            
    def fileExists(self):
        return os.path.exists(self.path)