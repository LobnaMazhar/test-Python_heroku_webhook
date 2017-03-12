#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response


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


def requestUserName(req):
    originalRequest = req.get("originalRequest")
    data = originalRequest.get("data")
    sender = data.get("sender")
    id = sender.get("id")
    access_token = "EAAOSFv52vZAYBAFnqlPlZAsGuUdVGrrjaktAkZAbBoFZAFEWhPIM0rqL8BSXCPPfjjipakdjZCNWZCPVOWUcZBEiFAhfSNPZBbNY3ExCZAw9bzdnpWic0ZCwdUwCS43hwZCNRVZBZCMsZAWD5EnHbqPR4YeBvK41ZCcDBUTNKlUUqmSpCYmwwZDZD"
    rs = urllib.urlopen("https://graph.facebook.com/v2.6/" + id + "?fields=first_name&access_token="+ access_token)
    name = json.load(rs).get("first_name")
    print(name)
    return {
        "speech" : "",
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "prof-3abqarino",
        "followupEvent": {"name":"c_event","data":{"user":name}}
    }

def makeWebhookResult(req):
    if req.get("result").get("action") == "request-game":
        return requestUserName(req)
    else:
        return {}



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
