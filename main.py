from pprint import pprint
import requests

import json

city_name = input("Name of city: ")

url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=233fb10f061739fe6ced65c5f60ec5da".format(city_name)

weather_data = requests.get(url).json()
country_code = weather_data["sys"]["country"]

if country_code == "US" or country_code == "LR" or country_code == "MM":
    url+="&units=imperial"
else:
    url+="&units=metric"

print(url)
weather_data = requests.get(url).json()

_json = open("countrycodes.json","r") #countrycodes is a json I created utilizing the data from https://pkgstore.datahub.io/core/country-list/data_json/data/8c458f2d15d9f2119654b29ede6e45b8/data_json.json
countrycodes = json.loads(_json.read())

country_name = countrycodes[country_code]
print(weather_data['name']+"\n"+country_name)

pprint(weather_data)
