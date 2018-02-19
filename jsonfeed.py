import urllib, json

lat = "37.7"
lon = "-122.1"
aqicn_token = "214e3324769450fc0bc5688dac030affbc4d48a1"

url = "https://api.waqi.info/feed/geo:" + lat + ";" + lon + "/?token=" + aqicn_token

response = urllib.urlopen(url)
data = json.loads(response.read())
print("pollutants & weather conditions\n")

#json structure at: http://aqicn.org/json-api/doc/
print(data['data']['aqi'])


