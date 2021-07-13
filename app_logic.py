from pprint import pprint
import requests
import json

city_name = input("Name of city: ")

url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=233fb10f061739fe6ced65c5f60ec5da".format(city_name)

while True:
    try:
        weather_data = requests.get(url).json()
        country_code = weather_data["sys"]["country"]
        break
    except KeyError as InvalidCity:
        print("Invalid city name")
        city_name = input("Name of city: ")
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=233fb10f061739fe6ced65c5f60ec5da".format(city_name)

if country_code == "US" or country_code == "LR" or country_code == "MM":
    url+="&units=imperial"
else:
    url+="&units=metric"

print(url)
weather_data = requests.get(url).json()

_json = open("data/countrycodes.json","r") #countrycodes is a json I created utilizing the data from https://pkgstore.datahub.io/core/country-list/data_json/data/8c458f2d15d9f2119654b29ede6e45b8/data_json.json
countrycodes = json.loads(_json.read())

city = weather_data['name']+", "+countrycodes[country_code]
location = "("+str(weather_data['coord']['lat'])+"°, "+str(weather_data['coord']['lon'])+"°)"
weather = weather_data['weather']
weather_descriptions = []
weather_icons = []
i = 0
for data in weather:
    weather_descriptions.append(data['description'])
    weather_icons.append(data['icon'])
    i+=1

print(weather_descriptions)
print(weather_icons)
pprint(weather_data)