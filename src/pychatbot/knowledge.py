# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] PyChatbot Knowledge
# // ---------------------------------------------------------------------

# // ---- Imports
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
        self.fullPath = os.path.join(self.databasePath, self.databaseName)

        # connect to db
        self.database = sqlite3.connect(self.databasePath)
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
            source TEXT
            data TEXT
        )""") # responses is a json list, data is a json dict
        
        self.__commit()

    def getAllQueries(self):
        cursor = self.__getCursor()
        allData = cursor.execute("SELECT query FROM Knowledge")

        return self.__fetchAllOfColumn(0, allData)
    
    def getResponsesForQuery(self, query: str) -> list[dict[str, str]]:
        cursor = self.__getCursor()
        allData = cursor.execute("SELECT responses FROM Knowledge WHERE query=?", (query))
        
        return self.__fetchAllOfColumn(0, allData)
    
    def unlearn(self, query: str):
        self.__getCursor().execute("DELETE FROM Knowledge WHERE query=?", (query))
        self.__commit()
        
    def learn(self, query: str, responses: list[str], source: str, *, data: dict[str, any] = {}):
        # save query and responses
        cursor = self.__getCursor()
        cursor.execute("INSERT INTO Knowledge VALUES (?, ?, ?, ?)", (query, json.dumps(responses), source, json.dumps(data)))
        
        self.__commit()