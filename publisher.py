from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.pubnub import SubscribeListener
from pubnub.exceptions import PubNubException
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.callbacks import SubscribeCallback
import threading
import urllib, json, sys

#AQICN API info and JSON structure at: http://aqicn.org/json-api/doc/
lat = "37.7"
lon = "-122.1"
aqicn_api_token = "214e3324769450fc0bc5688dac030affbc4d48a1"
url = "https://api.waqi.info/feed/geo:" + lat + ";" + lon + "/?token=" + aqicn_api_token
aqi = ""
city = ""
time = ""

#initialize pubnub
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-ce1f7efa-0bda-11e8-8ffb-b29a975517c3'
pnconfig.publish_key = 'pub-c-b43f4454-c2c0-4587-aa51-a6785db8406f'
pnconfig.ssl = True
pnconfig.uuid = 'aqi publisher'

pubnub = PubNub(pnconfig)

class myListener(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print("connected")

    def presence(self, pubnub, presence):
        print(presence.uuid)
        aqi_call()

def main():
    #add listener
    my_listener = myListener()
    pubnub.add_listener(my_listener)
    #subscribe to presnce 
    pubnub.subscribe()\
        .channels("aqi")\
        .with_presence()\
        .execute()

    aqi_call_loop()
    
def aqi_call_loop():
    aqi_call()
    threading.Timer(1500, aqi_call_loop).start()


# def here_now_callback(result, status):
#     if status.is_error():
#         print("here now callback error")
#         return
#     for channel_data in result.channels:
#         print("---")
#         print("channel: %s" % channel_data.channel_name)
#         print("occupancy: %s" %channel_data.occupancy)
#     for occupant in channel_data.occupants:
#         print("uuid: %s, state: %s" % (occupant.uuid, occupant.state))

def aqi_call():
    try:
        response = urllib.request.urlopen(url)
    except:
        sys.exit("url error")

    data = json.loads(response.read())
    aqi = data['data']['aqi']
    city = data['data']['city']['name']
    time = data['data']['time']['s']

def publish_aqi():
    try:
        pubnub.publish().channel('aqi').message({
            'aqi': aqi,
            'city': city,
            'time': time
        }).sync()
    except PubNubException as e:
        handle_exception(e)

    # pubnub.here_now()\
    # .channels('aqi')\
    # .include_uuids(True)\
    # .async(here_now_callback)

if __name__ == "__main__":
   main()