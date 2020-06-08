from utils.message_broker import WebexTeamsMessageBroker, StdOutMessageBroker
from utils.commands import CommandFactory
from utils.parse import parse

from dnacentersdk import api

dnac_api = api.DNACenterAPI(base_url='https://sandboxdnac2.cisco.com:443', username='devnetuser',password='Cisco123!')
webex_broker = WebexTeamsMessageBroker("blub")
std_out_broker = StdOutMessageBroker()

cf = CommandFactory(dnac_api, std_out_broker)


# Start adding commands here
# Step 1: Define a function that will be called when our command is reached
def get_details_command(dnac, args):
    devices = []
    if len(args.keys()) == 0:
        devices = dnac.devices.get_device_list().response
    else:
        devices = dnac.devices.get_device_list(**args).response

    ret = "### List of Devices\n"
    for d in devices:
        ret += "* {} running {} (mgt-ip: {}, status: {}, id: {})\n".format(d['series'],
                                                                           d['softwareType'],
                                                                           d['managementIpAddress'],
                                                                           d['reachabilityStatus'],
                                                                           d['id']
                                                                          )

    return ret
# Step 2: Add the command to our list of available commands
cf.create_command('list_devices', get_details_command)

def get_device_details(dnac, args):
    device_details = dnac.devices.get_device_by_id(**args).response

    ret = "### Details on Device \n"
    for k, v in device_details.items():
        ret += "* {} -> {}\n".format(k, v)

    return ret

cf.create_command('get_device_details', get_device_details)

while True:
    input_cmd = input("Please give a command: ")
    if input_cmd == "ESC":
        break
    cmd, args = parse(input_cmd)
    cf.run_command(cmd, args)
