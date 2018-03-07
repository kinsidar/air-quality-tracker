![Demo Img](img/aqigauge.gif)

![python ver](https://img.shields.io/pypi/pyversions/Django.svg)

## Air quality index(AQI) display using [pubnub](https://www.pubnub.com/) and [epoch](http://epochjs.github.io/epoch/)

## To Run:
    - Add your PubNub publish and subscribe keys to publisher.py and subscriber.html
    - Run publisher.py
    - Open Subscriber.html in your browser

## Publisher
    - Checks for AQI every 15 minutes, publishes new AQI info if users present in channel
    - Publishes AQI info when a new subscriber connects to the channel
