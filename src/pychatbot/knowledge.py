# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] PyChatbot Knowledge
# // ---------------------------------------------------------------------

# // ---- Imports
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
        
    # // main methods
    def createDatabaseSchema(self):
        cursor = self.__getCursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Knowledge (
            query TEXT PRIMARY KEY,
            responses TEXT,
            source TEXT,
            data TEXT
        )""") # responses is a json list, data is a json dict
        
        self.__commit()

    def getAllQueries(self) -> list[str]:
        cursor = self.__getCursor()
        allData = cursor.execute("SELECT query FROM Knowledge")
        queries = self.__fetchAllOfColumn(0, allData)

        return queries
    
    def getResponsesWithSource(self, source: str):
        # execute sql stuffs
        cursor = self.__getCursor()
        data = cursor.execute("SELECT * FROM Knowledge WHERE source = ?", [source]).fetchall()
        
        # return
        return [response(__response[0], json.loads(__response[1]), __response[2], json.loads(__response[3])) for __response in data]

    def getResponsesForQuery(self, query: str):
        # execute sql stuffs
        cursor = self.__getCursor()
        data = cursor.execute("SELECT * FROM Knowledge WHERE query = ?", [query]).fetchone()
        
        # return
        return response(data[0], json.loads(data[1]), data[2], json.loads(data[3]))
    
    def unlearn(self, query: str):
        self.__getCursor().execute("DELETE FROM Knowledge WHERE query = ?", [query])
        self.__commit()
        
    def learn(self, query: str, responses: list[str], source: str, *, data: dict[str, any] = {}):
        # save query and responses
        cursor = self.__getCursor()
        cursor.execute("INSERT OR IGNORE INTO Knowledge VALUES (?, ?, ?, ?)", [query, json.dumps(responses), source, json.dumps(data)])
        
        self.__commit()
        
class response:
    def __init__(self, query: str, responses: list[str], source: str, data: dict[str, any]):
        self.__responses = responses
        self.__source = source
        self.__data = data
        self.__query = query
        
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