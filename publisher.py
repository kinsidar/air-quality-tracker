from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
# from pubnub.pubnub import SubscribeListener
from pubnub.exceptions import PubNubException
from pubnub.enums import PNStatusCategory
import threading

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-ce1f7efa-0bda-11e8-8ffb-b29a975517c3'
pnconfig.publish_key = 'pub-c-b43f4454-c2c0-4587-aa51-a6785db8406f'
pnconfig.ssl = True

#initialize pubnub with configuration settings
pubnub = PubNub(pnconfig)

# my_listener = SubscribeListener()
# pubnub.add_listener(my_listener)

def set_interval():
    pubnub.publish().channel('aqi').message({
        'aqi': 'over 9000',
        'co2': 21
    }).sync()
    threading.Timer(10.0, set_interval).start()

threading.Timer(10.0, set_interval).start()

# pubnub.subscribe().channels('aqi').execute()
# my_listener.wait_for_connect()
# print('connected')

# result = my_listener.wait_for_message_on('aqi')
# print(result.message)
# print("end of message")









# class MyListener(SubscribeCallback):
#     def status(self, pubnub, status):
#         if status.category == PNStatusCategory.PNDisconnectedCategory:
#             pubnub.publish().channel('aqi').message({'aqi': 'over 9000', 'co2': 21 }).sync()
    
#     def message(self, pubnub, message):
#         pass
    
#     def presence(self, pubnub, presence):
#         pass

# my_istener = MyListener()

# pubnub.add_listener(my_istener)

# pubnub.subscribe().channels('aqi').execute()


# pubnub.subscribe().channels('my_channel').execute()

# try:
#     envelope = pubnub.publish().channel('my_channel').message({
#         'name': 'Kinsa',
#         'online': True
#     }).sync()
#     print('publish timetoken: %d' % envelope.result.timetoken)
# except PubNubException as e:
#     print(e)

