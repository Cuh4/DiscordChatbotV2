# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] PyChatbot Knowledge
# // ---------------------------------------------------------------------

# // ---- Imports
import time
import random
import json
import os
import sqlite3

from . import helpers

# // ---- Main
class knowledge:
    def __init__(self, name: str, knowledgePath: str):
        # properties
        self.name = name

        self.databaseName = helpers.pathSafeName(name) + ".db"
        self.databasePath = knowledgePath
        self.fullPath = os.path.abspath(os.path.join(self.databasePath, self.databaseName))

        # connect to db
        self.database = sqlite3.connect(self.fullPath)
        self.createDatabaseSchema()
        
    # // helpers
    def __getCursor(self):
        return self.database.cursor()
    
    def __commit(self):
        return self.database.commit()
    
    def __fetchAllOfColumn(self, columnIndex: int, allData: list):
        return [data[columnIndex] for data in allData]
    
    def __toResponse(self, data: list):
        return response(data[0], json.loads(data[1]), data[2], json.loads(data[3]), data[4]) # query, responses (list), source, custom data, timestamp
        
    # // main methods
    def createDatabaseSchema(self):
        cursor = self.__getCursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Knowledge (
            query TEXT PRIMARY KEY,
            responses TEXT,
            source TEXT,
            data TEXT,
            timestamp REAL
        )""") # responses is a json list, data is a json dict
        
        self.__commit()

    def getAllQueries(self) -> list[str]:
        cursor = self.__getCursor()
        allData = cursor.execute("SELECT query FROM Knowledge")
        queries = self.__fetchAllOfColumn(0, allData)

        return queries
    
    def getResponsesWithSource(self, source: str) -> list["response"]:
        # execute sql stuffs
        cursor = self.__getCursor()
        responses = cursor.execute("SELECT * FROM Knowledge WHERE source = ?", [source]).fetchall()
        
        # return
        return [self.__toResponse(__response) for __response in responses]

    def getResponsesForQuery(self, query: str)  -> list["response"]:
        # execute sql stuffs
        cursor = self.__getCursor()
        __response = cursor.execute("SELECT * FROM Knowledge WHERE query = ?", [query]).fetchone()
        
        # return
        return self.__toResponse(__response)
    
    def unlearn(self, query: str):
        self.__getCursor().execute("DELETE FROM Knowledge WHERE query = ?", [query])
        self.__commit()
        
    def learn(self, query: str, responses: list[str], source: str, *, data: dict[str, any] = {}):
        # save query and responses
        cursor = self.__getCursor()
        cursor.execute("INSERT OR IGNORE INTO Knowledge VALUES (?, ?, ?, ?, ?)", [query, json.dumps(responses), source, json.dumps(data), time.time()])
        
        self.__commit()
        
class response:
    def __init__(self, query: str, responses: list[str], source: str, data: dict[str, any], timestamp: float):
        self.__responses = responses
        self.__source = source
        self.__data = data
        self.__query = query
        self.__timestamp = timestamp
        
    def getResponses(self):
        return self.__responses
    
    def getRandomResponse(self):
        responses = self.getResponses()
    
        if len(responses) <= 0:
            return
        
        return random.choice(responses)
    
    def getSource(self):
        return self.__source
    
    def getData(self):
        return self.__data
    
    def getQuery(self):
        return self.__query
    
    def getTimestamp(self):
        return self.__timestamp