import os

from utils.message_broker import WebexTeamsMessageBroker, StdOutMessageBroker
from utils.commands import CommandFactory
from utils.parse import parse

from dnacentersdk import api
from webexteamssdk import WebexTeamsAPI

from flask import Flask, request, jsonify

dnac_api = api.DNACenterAPI(base_url="https://sandboxdnac2.cisco.com:443",
                            username="devnetuser",
                            password="Cisco123!"
                           )

webex_broker = WebexTeamsMessageBroker(os.environ['WEBEX_TEAMS_ACCESS_TOKEN'])
std_out_broker = StdOutMessageBroker()
app = Flask(__name__)
webex_api = WebexTeamsAPI(access_token=os.environ['WEBEX_TEAMS_ACCESS_TOKEN'])

cf = CommandFactory(dnac_api, webex_broker)

# Add commands here
# Step 1: Write a function that deals with this command
def list_devices_command(dnac, args):
    devices = []
    if len(args.keys()) == 0:
        devices = dnac.devices.get_device_list().response
    else:
        devices = dnac.devices.get_device_list(**args).response

    ret = "### List of Devices\n"
    for d in devices:
        ret += "* {} running {} (mgmt-ip: {}, status: {}, id: {})\n".format(d['series'],
                                                                          d['softwareType'],
                                                                          d['managementIpAddress'],
                                                                          d['reachabilityStatus'],
                                                                          d['id']
                                                                         )
    return ret

# Step 2: Add the command to our list of available commands
cf.create_command('list_devices', list_devices_command)

def get_device_details_command(dnac, args):
    device_details = dnac.devices.get_device_by_id(**args).response

    ret = "### Details on Device \n"

    for k, v in device_details.items():
        ret += "* {}: {}\n".format(k, v)

    return ret

cf.create_command('get_device_details', get_device_details_command)

# This part deals with receiving messages from webex teams
@app.route('/webex/message', methods=['POST'])
def webex_message():
    raw_json = request.get_json()
    data = raw_json['data']
    if not webex_api.people.me().id == data['personId']:
        # Check that this is not a message by the bot itself
        message = webex_api.messages.get(data['id'])

        text = message.text

        # Get raw command string - Webex Teams bots are mentioned in the beginning
        command_string = " ".join(str(text).lower().split(" ")[1:])

        # Set target to our source room id
        webex_broker.set_target_id(data['roomId'])
        # Parse the command string and trigger a return
        cmd, args = parse(command_string)
        cf.run_command(cmd, args)

    return jsonify({'success': True})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6020, debug=True)
