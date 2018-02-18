from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-ce1f7efa-0bda-11e8-8ffb-b29a975517c3'
pnconfig.publish_key = 'pub-c-b43f4454-c2c0-4587-aa51-a6785db8406f'
pnconfig.ssl = True

#initialize pubnub with configuration settings
pubnub = PubNub(pnconfig)

