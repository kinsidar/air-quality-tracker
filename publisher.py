from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.pubnub import SubscribeListener
from pubnub.exceptions import PubNubException
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.callbacks import SubscribeCallback
import threading
import urllib
import json
import sys

#AQICN API info and JSON structure at: http://aqicn.org/json-api/doc/
lat = "37.78"
lon = "-122.4"
aqicn_api_token = "214e3324769450fc0bc5688dac030affbc4d48a1"
url = "https://api.waqi.info/feed/geo:" + lat + ";" + lon + "/?token=" + aqicn_api_token
aqi = ""
city = ""
time = ""

#initialize pubnub
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'your sub key here'
pnconfig.publish_key = 'your pub key here'
pnconfig.ssl = True
pnconfig.uuid = 'aqi publisher'

pubnub = PubNub(pnconfig)

class myListener(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print("connected")

    def presence(self, pubnub, presence):
        #publish aqi when subscriber connects
        if aqi == "":
            aqi_call()
        publish_aqi()

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
    #check if subscriber is present. If true, get and publish aqi
    pubnub.here_now()\
        .channels('aqi')\
        .include_uuids(True)\
        .async(here_now_callback)
    threading.Timer(60, aqi_call_loop).start()

def aqi_call():
    try:
        response = urllib.request.urlopen(url)
    except:
        sys.exit("url error")

    data = json.loads(response.read())
    global aqi, city, time
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
        sys.exit("Pubnub publish exception", e)

def here_now_callback(result, status):
    global aqi
    if status.is_error():
        sys.exit("here now callback error")
    #get aqi data and publish if there is a subscriber(excluding publisher)
    for channel_data in result.channels:
        #publish aqi if aqi value changes and there is a subscriber present
        if channel_data.occupancy > 1:
            prev_aqi = aqi
            aqi_call()
            if aqi != prev_aqi:
                publish_aqi()

if __name__ == "__main__":
   main()