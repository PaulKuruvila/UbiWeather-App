from pprint import pprint
import requests

city_name = input('Name of city: ')

state_code = input('State code: ')

url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&appid=233fb10f061739fe6ced65c5f60ec5da&units=imperial'.format(city_name,state_code)

print(url)

weather_data = requests.get(url).json()

pprint(weather_data)

print("Hello World!")