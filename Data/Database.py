import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

import psycopg2
import urlparse

class Database:
    connection = None
    
    def __init__(self):
        print "--------in Database __init__--------"
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
        )
        print "--------Opened database successfully--------"

    def __createTables__(self):
        print "--------in Database createTables--------"
        self.createTable_Answers()
        self.createTable_Keywords()
        self.createTable_Answers_Keywords()
        self.createTable_Synonyms()
        self.createTable_Questions_Answers()
        print "--------Tables created successfully--------"

        conn.close()
        
        return {
        "speech" : "Created tables",
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "create-database"
        }

    def __deleteTables__(self):
        print "--------in Database deleteTables--------"
        self.deleteTable_Answers_Keywords()
        self.deleteTable_Answers()
        self.deleteTable_Synonyms()
        self.deleteTable_Keywords()
        self.deleteTable_Questions_Answers()
        print "--------Tables deleted successfully--------"


    def createTable_Answers(self):
        print "--------in Database createTable_Answers--------"
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Answers"
               (ID SERIAL PRIMARY KEY NOT NULL,
               Answer TEXT NOT NULL);''')
        print "--------Table Answers created successfully--------"

    def deleteTable_Answers(self):
        print "--------in Database deleteTable_Answers--------"
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Answers";''')
        print "--------Table Answers deleted successfully--------"


    def createTable_Keywords(self):
        print "--------in Database createTable_Keywords--------"
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Keywords"
               (ID SERIAL PRIMARY KEY NOT NULL,
               Keyword TEXT NOT NULL,
               Category TEXT NOT NULL);''')
        print "--------Table Keywords created successfully--------"

    def deleteTable_Keywords(self):
        print "--------in Database deleteTable_Keywords--------"
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Keywords";''')
        print "--------Table Keywords deleted successfully--------"


    def createTable_Answers_Keywords(self):
        print "--------in Database createTable_Answers_Keywords--------"
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Answers_Keywords"
               (Answer_ID INT NOT NULL,
               Keyword_ID INT NOT NULL,
               FOREIGN KEY (Answer_ID) REFERENCES "Answers"(ID),
               FOREIGN KEY (Keyword_ID) REFERENCES "Keywords"(ID),
               PRIMARY KEY(Answer_ID, Keyword_ID));''')
        print "--------Table Answers_Keywords created successfully--------"

    def deleteTable_Answers_Keywords(self):
        print "--------in Database deleteTable_Answers_Keywords--------"
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Answers_Keywords";''')
        print "--------Table Answers_Keywords deleted successfully--------"


    def createTable_Synonyms(self):
        print "--------in Database createTable_Synonyms--------"
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Synonyms"
               (Key_ID INT NOT NULL,
               Synonym TEXT NOT NULL,
               FOREIGN KEY (Key_ID) REFERENCES "Keywords"(ID),
               PRIMARY KEY(Key_ID, Synonym));''')
        print "--------Table Synonyms created successfully--------"

    def deleteTable_Synonyms(self):
        print "--------in Database deleteTable_Synonyms--------"
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Synonyms";''')
        print "--------Table Synonyms deleted successfully--------"


    def createTable_Questions_Answers(self):
        print "--------in Database createTable_Questions_Answers--------"
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Questions_Answers"
               (ID SERIAL PRIMARY KEY NOT NULL,
               Question TEXT NOT NULL,
               Answer_1 TEXT NOT NULL,
               Answer_2 TEXT NOT NULL,
               Answer_3 TEXT NOT NULL,
               Correct_AnswerID INT NOT NULL);''')
        print "--------Table Questions_Answers created successfully--------"


    def deleteTable_Questions_Answers(self):
        print "--------in Database deleteTable_Questions_Answers--------"
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Questions_Answers";''')
        print "--------Table Questions_Answers deleted successfully--------"
