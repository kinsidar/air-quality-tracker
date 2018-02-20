from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.pubnub import SubscribeListener
from pubnub.exceptions import PubNubException
from pubnub.enums import PNStatusCategory
# import threading
import urllib, json

#get aqi info from aqicn API
lat = "37.7"
lon = "-122.1"
aqicn_token = "214e3324769450fc0bc5688dac030affbc4d48a1"
url = "https://api.waqi.info/feed/geo:" + lat + ";" + lon + "/?token=" + aqicn_token
response = urllib.urlopen(url)
data = json.loads(response.read())

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-ce1f7efa-0bda-11e8-8ffb-b29a975517c3'
pnconfig.publish_key = 'pub-c-b43f4454-c2c0-4587-aa51-a6785db8406f'
pnconfig.ssl = True

#initialize pubnub with configuration settings
pubnub = PubNub(pnconfig)

my_listener = SubscribeListener()
pubnub.add_listener(my_listener)

pubnub.subscribe().channels('aqi').execute()
my_listener.wait_for_connect()
print('connected')  

pubnub.publish().channel('aqi').message({
    'aqi': data['data']['aqi']
}).sync()

result = my_listener.wait_for_message_on('aqi')
print(result.message)

pubnub.unsubscribe().channels('awesomeChannel').execute()
my_listener.wait_for_disconnect()

print('unsubscribed')

# def set_interval():
#     pubnub.publish().channel('aqi').message({
#         'aqi': 'over 9000',
#         'co2': 21
#     }).sync()
#     threading.Timer(10.0, set_interval).start()

# threading.Timer(10.0, set_interval).start()
# print("end of message")

