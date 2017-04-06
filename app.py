#!/usr/bin/env python
from Data import Database

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

import psycopg2
import urlparse

global name
global singletonObject
singletonObject = None

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def requestGame(req):
    originalRequest = req.get("originalRequest")
    data = originalRequest.get("data")
    sender = data.get("sender")
    id = sender.get("id")

    parameter = req.get("result").get("parameters").get("requestParam")
    print "-------------- " + parameter + " ------------"
    
    return {
        "speech" : "playing a game",
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "test-python"
    }

def connectDB():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
  ###  conn = psycopg2.connect(database="testpgdp", user="postgres", password="pgAdmin_postgreSQL", host="127.0.0.1", port="5432")
    print "Opened database successfully"
    return conn

def createTable(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE "USER"
           (ID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL);''')
    print "Table created successfully"

def createTable_Answers(conn):
    print "--------in Database createTable_Answers--------"
    cur = conn.cursor()
    cur.execute('''CREATE TABLE "AnswersOut"
            (ID SERIAL PRIMARY KEY NOT NULL,
            Answer TEXT NOT NULL);''')
    conn.commit()
    print "--------Table Answers created successfully--------"

def insertIntoDB(conn):
    cur = conn.cursor()

    cur.execute("INSERT INTO \"USER\" (ID,NAME,AGE) \
        VALUES (3, 'Mary', 82)");

    cur.execute("INSERT INTO \"USER\" (ID,NAME,AGE) \
        VALUES (4, 'Jack', 12)");

    conn.commit()
    print "Records created successfully";


def selectDB(conn):
    cur = conn.cursor()

    cur.execute("SELECT id, name from \"USER\"")
    rows = cur.fetchall()

    for row in rows:
        global name
        name = row[1]
        print "ID = ", row[0]
        print "NAME = ", row[1], "\n"

    print "Operation done successfully";
    return name
    
def requestDB(req):
    name = "Empty";
    
    conn = connectDB()
   ### createTable_Answers(conn)
    ###createTable(conn)
  ###  insertIntoDB(conn)
    
    print "before " + name
    name = selectDB(conn)
    print "after " + name

    conn.close()
    
    return {
        "speech" : name,
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "test-python"
    }

def requestEvent(req):
    
    return {
        "speech" : "",
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "test-python",
        "followupEvent":{
            "name":"test-event",
            "data":{
                "event":"inside event"
                }
            }
        }

def requestSingleton(req):
    global singletonObject

    if singletonObject is None:
        print "---- not singleton -----"
        singletonObject = "updated"
    print singletonObject
 
    return {
        "speech" : singletonObject,
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "test-python"
    }

def getRandomName(conn):
    cur = conn.cursor()

    cur.execute("SELECT * FROM \"USER\" OFFSET floor(random()*(SELECT COUNT(*) FROM \"USER\")) LIMIT 1")
    rows = cur.fetchall()

    for row in rows:
        global name
        name = row[1]
        print "ID = ", row[0]
        print "NAME = ", row[1], "\n"

    print "Operation done successfully";
    return name

def requestRandomName():
    name = "Empty";
    
    conn = connectDB()
    
    print "before " + name
    name = getRandomName(conn)
    print "after " + name

    conn.close()
    
    return {
        "speech" : name,
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "test-python"
    }

def makeWebhookResult(req):
    if req.get("result").get("action") == "request-game":
        return requestGame(req)
    elif req.get("result").get("action") == "get-from-db":
        return requestDB(req)
    elif req.get("result").get("action") == "test-event":
        return requestEvent(req)
    elif req.get("result").get("action") == "test-singleton":
        return requestSingleton(req)
    elif req.get("result").get("action") == "createDB":
        requestDB(req)
        conn = Database.Database()
        return conn.__createTables__()
    elif req.get("result").get("action") == "get-random-name":
        return requestRandomName()
    else:
        return {}



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
