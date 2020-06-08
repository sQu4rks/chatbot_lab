from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI

import os
import datetime

app = Flask(__name__)
api = WebexTeamsAPI(access_token=os.environ['WEBEX_TEAMS_ACCESS_TOKEN'])

ROOM_ID = os.environ['ROOM_ID']
DNAC_URL = "https://sandboxdnac2.cisco.com/"

@app.route('/dnac/event', methods=['POST'])
def dnac_event():
    """ Receive dnac webhook event and convert it into a Webex message"""
    dnac_notification = request.json
    
    title_emojii = "📢"

    if dnac_notification['category'] == "ALERT":
        title_emojii = "🚨"
    elif dnac_notification['category'] == "WARNING":
        title_emojii = "⚠️"
    
    # construct the team message
    teams_message = "## {} {}\n".format(title_emojii, dnac_notification['details']['Assurance Issue Name'])
    teams_message += "* Severity: {}\n".format(dnac_notification['severity'])
    teams_message += "* Category: {}\n".format(dnac_notification['category'])
    teams_message += "* Timestamp: {}\n".format(str(datetime.datetime.fromtimestamp(int(dnac_notification['timestamp'] / 1000)).strftime('%Y-%m-%d %H:%M:%S')))
    teams_message += "* Issue Name: {}\n".format(dnac_notification['details']['Assurance Issue Name'])
    teams_message += "* Issue Description: {}\n".format(dnac_notification['details']['Assurance Issue Details'])
    teams_message += "* Issue Status: {}\n".format(dnac_notification['details']['Assurance Issue Status'])
    teams_message += "\n\nGet more information [here]({})".format(dnac_notification['ciscoDnaEventLink'])

    api.messages.create(roomId=ROOM_ID, markdown=teams_message)

    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6010, debug=True)