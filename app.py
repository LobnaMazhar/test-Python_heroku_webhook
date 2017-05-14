#!/usr/bin/env python
from Data import Database

import urllib
import requests
import json
import os

import hashlib
import hmac

from flask import Flask
from flask import request
from flask import make_response

import psycopg2
import urlparse

import time
from threading import Timer

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

@app.route('/webhooknotify', methods=['POST','GET'])
def webhookNotify():
    print "NOTIFYING"
    notifyUser();

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

    call_to_actions_submenu = [{
              "title":"Pay Bill",
              "type":"postback",
              "payload":"PAYBILL_PAYLOAD"
            },
            {
              "title":"History",
              "type":"postback",
              "payload":"HISTORY_PAYLOAD"
            },
            {
              "title":"Contact Info",
              "type":"postback",
              "payload":"CONTACT_INFO_PAYLOAD"
            },
            {
              "title":"Request game",
              "type":"postback",
              "payload":"reqGame"
            }]
    
    call_to_actions_menu = [{
          "title":"My Account",
          "type":"nested",
          "call_to_actions":json.dumps(call_to_actions_submenu, ensure_ascii=False)
        },
        {
          "type":"web_url",
          "title":"Latest News",
          "url":"http://petershats.parseapp.com/hat-news",
          "webview_height_ratio":"full"
        }]
    
    presistent_menu = [{
      "locale":"default",
      "composer_input_disabled":True,
      "call_to_actions":json.dumps(call_to_actions_menu, ensure_ascii=False)
    },
    {
      "locale":"zh_CN",
      "composer_input_disabled":False
    }]
    
    values = {}
    values["persistent_menu"] = json.dumps(presistent_menu, ensure_ascii=False)

    r = requests.post(url, data = values, headers={'Content-type': 'application/json'})
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')
    print "--------------------->>>>>>>>>>>>>>" + "<<<<<<<<<<<<--------------------"


def deleteMenu():
    access_token = "EAASr1ZCrcjQkBADfZCmEo87CLaDUTy9pDWWn8CZCX45ekEcHxbk459jAcGnyGENSZBbcNuSLgRGjToh3MXPUYeqZBlEwEtl3yVinBBFdxdssk1Ga2n7zTfKLMiiXsuU35H3KsPrISHmaDbsSZAoa6PQes8V2sqBRVJZAEYOqIZB5vwZDZD"
    url = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + access_token

    fields = ["persistent_menu"]
    values = {}
    values["fields"] = json.dumps(fields, ensure_ascii=False)
    

    r = requests.delete(url, data = values, headers={'Content-type': 'application/json'})
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')
    print "--------------------->>>>>>>>>>>>>>" + "SUCCESS" + "<<<<<<<<<<<<--------------------"


def notifyUser():
    print "---------------------CALLLING NOTIFY USER------------------------"
    
    access_token = "EAASr1ZCrcjQkBADfZCmEo87CLaDUTy9pDWWn8CZCX45ekEcHxbk459jAcGnyGENSZBbcNuSLgRGjToh3MXPUYeqZBlEwEtl3yVinBBFdxdssk1Ga2n7zTfKLMiiXsuU35H3KsPrISHmaDbsSZAoa6PQes8V2sqBRVJZAEYOqIZB5vwZDZD"
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + access_token

    userID = "1034552696650591"

    paramRecipient = { "id": userID }
    paramMessage = { "text": "hello, world! --OWN app" }
    requestJSON = {}
    requestJSON["recipient"] = json.dumps(paramRecipient, ensure_ascii=False)
    requestJSON["message"] = json.dumps(paramMessage, ensure_ascii=False)
    
    r = requests.post(url, data = requestJSON, headers={'Content-type': 'application/json'})
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')
    print "--------------------->>>>>>>>>>>>>>" + "<<<<<<<<<<<<--------------------"

def notifyMeSomeTimes(req):
    print "---------------------CALLLING NOTIFY ME------------------------"
    notify = True
    if req.get("result").get("action") == "notify_start":
        notify = True
    elif req.get("result").get("action") == "notify_stop":
        print "---------------------END OF NOTIFICATIONS------------------------"
        notify = False

    i=0;
    while notify:
        print "---------------------" + str(i) + "------------------------"
        i = i+1;
        Timer(60, notifyUser, ()).start()


def genAppSecretProof(app_secret, access_token):
    h = hmac.new (
        app_secret.encode('utf-8'),
        msg=access_token.encode('utf-8'),
        digestmod=hashlib.sha256
    )
    return h.hexdigest()

def getId_pages():
    app_secret = "fe692bf9bce1664e2dbe5cf8af0e5db9"
    access_token="EAACEdEose0cBAK3xy0srLgllZCYTWKZAOUUZCL06BBmozGcOyvmgytVEAPFA0yZAS9iOYW9PhLkpCHelUN4PM8otbTyC5aANr3f8FRykybHGNaJujkMPipVFd2vAZAQWWZAaZCtbazbLZCVL8XSDd5QApI2ntICGMN2ZAFyw5UKzZCXF7oWwqPQtxUdHp9m96pADAIWamviqndZBgZDZD"
    appsecret_proof = genAppSecretProof(app_secret, access_token)
    print("appsecret_proof --- ")
    print(appsecret_proof)
    
    url = "https://graph.facebook.com/v2.6/me?fields=ids_for_pages&access_token=" + access_token ### + "&appsecret_proof=" + appsecret_proof

    r = requests.get(url)
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')
    print "--------------------->>>>>>>>>>>>>>" + "<<<<<<<<<<<<--------------------"

def getAppScopedID(req):
    access_token="EAASr1ZCrcjQkBACkZA2QzbgaqeAFOH2CZAiGJkyFAYZAgrWzyXdRWXBLMLgDiZAFVL2YL17WM4gA2oeZBaDspgZBETqzARYJtWVSnjqNlrUZAgs8iRT9CSHQUhpI4ZA42YAmhFSTDinxWGvZAz8FpMU5EvqVdVok86qF01d1opiumfSbZB4XSlTQUiAvPxj7OR2Gh3a6fP62ol0nwZDZD"
    
    mid = req.get("originalRequest").get("data").get("message").get("mid")

    url = "https://graph.facebook.com/v2.9/" + mid + "?access_token=" + access_token + "&fields=from"
    r = requests.get(url)
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')
    print(r.get("from").get("id"))
    print "--------------------->>>>>>>>>>>>>>" + "<<<<<<<<<<<<--------------------"
    
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
    elif req.get("result").get("action") == "notify_start" or req.get("result").get("action") == "notify_stop":
        return notifyMeSomeTimes(req)
    elif req.get("result").get("action") == "id_pages":
        return getId_pages()
    elif req.get("result").get("action") == "appScopedID":
        return getAppScopedID(req)
    else:
        return {}



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
