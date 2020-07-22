import requests
import argparse
import json
import os
from requests.auth import HTTPDigestAuth

# Initiate wowza api arguments 
parser = argparse.ArgumentParser(description='''Used this tool for manage wowza from rest api''')
parser.add_argument("-n", "--name", action='store', help='enter action')
args = parser.parse_args()
name = args.name

# Credentials
wowza_host = os.environ['WOWZA_HOST']
user_name = os.environ['API_USER']
user_pass = os.environ['API_PASSWORD']
application_name = "live"

# Load channel list file
channel_path = "/home/faisal/projects/live/" # path of channel_list.json file
channel_file = f"{channel_path}/channel_list.json"
with open(channel_file, "r") as variable:
    data = json.load(variable)

# wowza functions to list all available stream file  
def get_list():
    url = f"http://{wowza_host}:8087/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/{application_name}/streamfiles"
    a = requests.get(url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, auth=HTTPDigestAuth(user_name, user_pass))
    b = json.loads(a.content)
    print(json.dumps(b, indent = 4, sort_keys=True))
    
# wowza functions to create new stream file 
def create_stream(stream_name, channel_ip):
    base_ip = "10.1.1.31"
    body = {
   "name": f"{stream_name}",
   "serverName": "_defaultServer_",
   "uri": f"udp://{base_ip}@{channel_ip}"
    }

    url = f"http://{wowza_host}:8087/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/{application_name}/streamfiles"
    a = requests.post(url, data=body, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, auth=HTTPDigestAuth(user_name, user_pass))
    b = json.loads(a.content)
    print(json.dumps(b, indent = 4, sort_keys=True))

# wowza functions to publish channels
def connect_stream(stream_name):    
    url = f"http://{wowza_host}:8087/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/{application_name}/streamfiles/{stream_name}/actions/connect?connectAppName={application_name}&appInstance=_definst_&mediaCasterType=rtp"
    a = requests.put(url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, auth=HTTPDigestAuth(user_name, user_pass))
    b = json.loads(a.content)
    stream_url = "http://66.210.244.230:1935/{application_name}/{stream_name}.stream/playlist.m3u8"
    print(json.dumps(b, indent = 4, sort_keys=True))
    
# wowza functions to disconnect ruuning channel
def disconnect_stream(stream_name):
    url = f"http://{wowza_host}:8087/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/{application_name}/instances/_definst_/incomingstreams/{stream_name}.stream/actions/disconnectStream"
    a = requests.put(url, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, auth=HTTPDigestAuth(user_name, user_pass))
    b = json.loads(a.content)
    print(json.dumps(b, indent = 4, sort_keys=True))

# wowza functions to parmanently remove any channel
def remove_stream(stream_name):
    url = f"http://{wowza_host}:8087/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/{application_name}/streamfiles/{stream_name}"
    a = requests.delete(url, headers={'Accept': 'application/json'}, auth=HTTPDigestAuth(user_name, user_pass))
    b = json.loads(a.content)
    print(json.dumps(b, indent = 4, sort_keys=True))

if __name__ == '__main__':
    print("#",60 * "=","#")
    print(15 * " ", 'Starting Wowza Automation Execution')
    print("#",60 * "=","#")
    
    if name == "list":
        get_list()
    
    elif name == "create":
        create_stream(stream_name, channel_ip)
        
    elif name == "createall":        
        for key, value in data.items():
            print("\n")
            stream_name = key
            print(stream_name)
            channel_ip = value
            print(channel_ip)
            create_stream(stream_name, channel_ip)
        
    elif name == "connect":
        connect_stream()
        
    elif name == "disconnect":
        disconnect_stream()
        
    elif name == "delete":
        remove_stream()
    
    else:
        print('''Oops! Something went wrong \n
To get help run following command:
python wowza.py --help \n''')

