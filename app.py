#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

import mysql.connector


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
    
    return {
        "speech" : "playing a game",
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "prof-3abqarino"
    }

def requestDB(req):
    db = mysql.connector.connect(host="localhost",    # your host, usually localhost                               
                     user="root",         # your username                                                      
                     passwd="phpMyAdmin_MySQL",  # your password                                               
                     db="python-db")        # name of the data base
    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("SELECT * FROM user")

    # print all the first cell of all the rows
    name = "Empty";
    for row in cur.fetchall():
        print (row[1])
        name = row[1]

    db.close()               
    return {
        "speech" : name,
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "prof-3abqarino"
    }

def makeWebhookResult(req):
    if req.get("result").get("action") == "request-game":
        return requestGame(req)
    elif req.get("result").get("action") == "get-from-db":
        return requestDB(req)
    else:
        return {}



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
