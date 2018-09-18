#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging
from datetime import datetime
import pytz

__author__ = "Jason Cantrell"
__license__ = "Apache v2"
__email__ = "cantrell.jm@gmail.com"
__version__ = "1.0"


# Spark/Webex Teams incoming webhook URL. For more information see https://developer.webex.com/webhooks-explained.html
WXTEAMS = ''

@app.route("/endpoint/wxteams", methods=['POST'])
@app.route("/endpoint/wxteams/<HOOKID>", methods=['POST','PUT'])
@app.route("/endpoint/wxteams/<HOOKID>/<RESOURCEID>", methods=['POST','PUT'])
def wxteams(HOOKID=None,RESOURCEID=None):
    """
    Send messages to Spark/Webex Teams. If HOOKID is not present, requires WXTEAMS defined as 'https://api.ciscospark.com/v1/webooks/incoming/<HOOKID>
    """
    # Prefer URL parameters to WXTEAMS
    if HOOKID is not None:
        URL = 'https://api.ciscospark.com/v1/webhooks/incoming/' + HOOKID
    elif not WXTEAMS or not 'https://api.ciscospark.com/v1/webhooks/incoming' in WXTEAMS:
        return ("WXTEAMS parameter must be set properly, please edit the shim!", 500, None)
    else:
        URL = WXTEAMS

    a = parse(request)

    try:
        if ('alertId' in a):
            timezone = pytz.timezone('America/Chicago')
            d = datetime.fromtimestamp(int(a['startDate'] / 1000.0)).replace(tzinfo=timezone)
            alertTime = d.strftime('%Y-%m-%d %H:%M:%S')

            message = "Resource Name: {resourceName}\n" \
                      "Timestamp: {alertTime}\n" \
                      "Status: {status}\n" \
                      "Info: {info}".format(resourceName=a['resourceName'],
                                            alertTime=alertTime,
                                            status=a['status'],
                                            info=a['info']
                                            )
            payload = {
                "text": message
            }
    except:
        logging.exception("Can't create new payload. Check code and try again.")
        raise

    return callapi(URL, 'post', json.dumps(payload))