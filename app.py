#!/usr/bin/env python
from Data import Database

import urllib
import requests
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
    parameter = "hello game"
    print "-------------- " + parameter + " ------------"
    
    return {
        "speech" : "",
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "test-python",
        "followupEvent":{
            "name":"param",
            "data":{
                "event":parameter
                }
            }
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

def insertIntoDB(conn, Name, age):
    cur = conn.cursor()

   ### cur.execute("INSERT INTO \"USER\" (ID,NAME,AGE) \
   ###     VALUES (3, 'Mary', 82)");

   ### cur.execute("INSERT INTO \"USER\" (ID,NAME,AGE) \
   ###     VALUES (4, 'Jack', 12)");

   ### cur.execute("INSERT INTO \"USER\" (ID,NAME,AGE) \
   ###     VALUES (5, " + "'" + Name + "'" + ", " + (str)(age) + ")");

   ### cur.execute('''INSERT INTO "USER" (ID,NAME,AGE) \
   ###     VALUES (8, ''' + "'" + Name + "'" + ", " + (str)(age) + ")");

    cur.execute('''INSERT INTO "USER" (ID,NAME,AGE) \
        VALUES (8, ''' + "'" + Name + "'" + ", " + (str)(age) + ")" + " ON CONFLICT (ID) DO NOTHING");

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
    insertIntoDB(conn, "Haya`s", 20)
    
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

def requestUserName(req):
    originalRequest = req.get("originalRequest")
    data = originalRequest.get("data")
    sender = data.get("sender")
    id = sender.get("id")
    access_token = "EAASr1ZCrcjQkBADfZCmEo87CLaDUTy9pDWWn8CZCX45ekEcHxbk459jAcGnyGENSZBbcNuSLgRGjToh3MXPUYeqZBlEwEtl3yVinBBFdxdssk1Ga2n7zTfKLMiiXsuU35H3KsPrISHmaDbsSZAoa6PQes8V2sqBRVJZAEYOqIZB5vwZDZD"
    rs = urllib.urlopen("https://graph.facebook.com/v2.6/" + id + "?fields=first_name&access_token=" + access_token)
    name = json.load(rs).get("first_name")
    print(name)
    return {
        "speech": "",
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "username",
        "followupEvent": {"name": "username-event", "data": {"user": name}}
        }

def addMenu():
    access_token = "EAASr1ZCrcjQkBADfZCmEo87CLaDUTy9pDWWn8CZCX45ekEcHxbk459jAcGnyGENSZBbcNuSLgRGjToh3MXPUYeqZBlEwEtl3yVinBBFdxdssk1Ga2n7zTfKLMiiXsuU35H3KsPrISHmaDbsSZAoa6PQes8V2sqBRVJZAEYOqIZB5vwZDZD"
    url = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + access_token
    values = {
  "persistent_menu":[{ "locale":"default", "composer_input_disabled":False, "call_to_actions":[{ "title":"My Account", "type":"nested", "call_to_actions":[{ "title":"reqGame", "type":"postback", "payload":"PAYBILL_PAYLOAD" }, { "title":"History", "type":"postback", "payload":"HISTORY_PAYLOAD"  },  { "title":"Contact Info",  "type":"postback", "payload":"CONTACT_INFO_PAYLOAD"  }  ] }, { "type":"web_url", "title":"Latest News", "url":"http://petershats.parseapp.com/hat-news", "webview_height_ratio":"full" } ] }, { "locale":"zh_CN", "composer_input_disabled":False } ]
  }

    r = requests.post(url, data = values, headers={'Content-type': 'application/json'})
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')
    print "--------------------->>>>>>>>>>>>>>" + "<<<<<<<<<<<<--------------------"


def deleteMenu():
    access_token = "EAASr1ZCrcjQkBADfZCmEo87CLaDUTy9pDWWn8CZCX45ekEcHxbk459jAcGnyGENSZBbcNuSLgRGjToh3MXPUYeqZBlEwEtl3yVinBBFdxdssk1Ga2n7zTfKLMiiXsuU35H3KsPrISHmaDbsSZAoa6PQes8V2sqBRVJZAEYOqIZB5vwZDZD"
    url = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + access_token
    values = { "fields":[ "persistent_menu" ] }

    r = requests.delete(url, data = values, headers={'Content-type': 'application/json'})
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')
    print "--------------------->>>>>>>>>>>>>>" + "SUCCESS" + "<<<<<<<<<<<<--------------------"


def replyMenu(req):
    data = req
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("postback"):
                    # user clicked/tapped "postback" button in earlier message
                    message_text = messaging_event["postback"]["payload"]
                    # the button's payload
                    #log("Inside postback")
                    message_text = message_text.lower()
                    sender_id = messaging_event["sender"]["id"]
                    if (message_text == "PAYBILL_PAYLOAD"):
                        send_message(sender_id, "Yay! This button works!")


def makeWebhookResult(req):
    print "-------------DOWN IS REQUEST START------------"
    print req
    print "-------------UP IS REQUEST END------------"
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
    elif req.get("result").get("action") == "req-username":
        return requestUserName(req)
    elif req.get("result").get("action") == "addMenu":
        return addMenu()
    elif req.get("result").get("action") == "deleteMenu":
        return deleteMenu()
    else:
        return {}



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
