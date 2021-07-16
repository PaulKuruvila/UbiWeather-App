from pprint import pprint
import requests
import json
import tkinter as tk
from tkinter import *#filedialog, Text, messagebox, simpledialog, Entry
#import os

root = tk.Tk()
root.title("UbiWeather - Weather Anywhere and Everywhere")
root.iconbitmap('weather icons/weather_app_icon.ico')
root.geometry("1050x900")
root.maxsize(height=1150,width=1050)
root.minsize(height=900,width=1050)

button_location = 1010
searchButtonx = 686
def resizeWindow(e):
    dif = e.width-button_location
    if dif<40:
        change_in_x = 686-((40-dif)/2)
        if not dif<-43:
            searchButton.place(x=change_in_x, y=132)
    elif dif>40:
        change_in_x = (dif-40)/2
        searchButton.place(x=searchButtonx+change_in_x,y=132)
    else:
        searchButton.place(x=686, y=132)

root.bind('<Configure>', resizeWindow)

def getPolygonPoints(x1, y1, x2, y2, r=25, **kwargs): # credit goes to users SneakyTurtle and tobias_k on https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
            points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
            return points

# function will take in current entered value from search box and return a list of suggested values
def searchSuggestions(e):
    suggestions = []
    return suggestions

#while button pressed and text != "", display search suggestions
def readBar(e):
    if e.keysym == 'Return': # do not run function if ENTER was pressed, call searchCity function instead
        print('Enter was pressed')
        searchCity(e)
        return
    # read what is typed
    currentSearch = searchBar.get()
    suggestions_box.delete(0,END)
    # if there is nothing typed, show no suggestions (hide the suggestions box)
    if currentSearch == '':
        print("Search bar is empty")
        suggestions_box.place_forget()
    else:
        print("Search bar: "+searchBar.get())
        suggestions_box.place(x=204,y=174)
        # Display what is being typed
        suggestions_box.insert(0, searchBar.get())
        # check if there are any suggestions
        #if :

def displayData(e, num_descr, _data):
    maincanvas.pack_forget()
    if num_descr == 1:
        description = _data[0]
        icon = _data[1]
        _city = _data[2]
        _location = _data[3]
        _temp = str(round(_data[4]))+"°"
        _temp_high = str(round(_data[5]))+"°"
        _temp_low = str(round(_data[6]))+"°"
        print("description = "+description)
        print("icon = "+icon)
        print("city = "+_city)
        print("location = "+_location)
        print("temp = "+str(_temp))
        print("temp high = "+str(_temp_high))
        print("temp low = "+str(_temp_low))
        #maincanvas.create_polygon(create_section(100, 45, 700, 500,r=100),fill="#E9ede9",smooth=True)
        maincanvas.create_polygon(getPolygonPoints(150, 45, 900, 650,r=100),fill="#E9ede9",smooth=True)
        maincanvas.create_text(525,100,text=_city, font=("Calibri", 28))
        weatherIcon = PhotoImage(file="weather icons/{}.png".format(icon))
        weatherIconLabel = Label(image=weatherIcon)
        weatherIconLabel.image = weatherIcon
        maincanvas.create_image(300,200,image=weatherIcon)
        maincanvas.create_text(450,170,text="Current", font=("Calibri", 20))
        maincanvas.create_text(450,230,text=_temp, font=("Calibri", 36))
        maincanvas.create_text(600,170,text="High", font=("Calibri", 20))
        maincanvas.create_text(600,230,text=_temp_high, font=("Calibri", 36))
        maincanvas.create_text(750,170,text="Low", font=("Calibri", 20))
        maincanvas.create_text(750,230,text=_temp_low, font=("Calibri", 36))
        maincanvas.pack()

def searchCity(e):
    city_entered = searchBar.get();
    if city_entered == '':
        return
    suggestions_box.place_forget()
    searchBar.delete(0,END)
    maincanvas.delete("all")
    print("Searching for "+city_entered+"...")
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=233fb10f061739fe6ced65c5f60ec5da".format(city_entered)
    try:
        weather_data = requests.get(url).json()
        country_code = weather_data["sys"]["country"]
    except KeyError as InvalidCity:
        print("Invalid city name")
        NoResults = maincanvas.create_text(525,105,justify='center',text="City not found.\nMake sure you only enter the city's name.\n(e.g. Abu Dhabi)", font=("Calibri", 18))
        return
    if country_code == "US" or country_code == "LR" or country_code == "MM":
        url+="&units=imperial"
    else:
        url+="&units=metric"
    weather_data = requests.get(url).json()
    # get all key weather info and create empty lists for storing weather descriptions and their respective weather icons (this is for cases where there may be more than one weather description)
    city = weather_data['name']+", "+countrycodes[country_code]
    location = "("+str(weather_data['coord']['lat'])+"°, "+str(weather_data['coord']['lon'])+"°)"
    temp = weather_data['main']['temp']
    temp_high = weather_data['main']['temp_max']
    temp_low = weather_data['main']['temp_min']
    weather = weather_data['weather']
    weather_descriptions = []
    weather_icons = []
    num_descriptions = 0
    for data in weather:
        weather_descriptions.append(data['description'])
        weather_icons.append(data['icon'])
        num_descriptions+=1
    print(weather_descriptions)
    print(weather_icons)
    pprint(weather_data)
    data_to_display = [weather_descriptions[0],weather_icons[0],city,location,temp,temp_high,temp_low]
    displayData(e, num_descriptions, data_to_display)

def listSelect(e):
    selectedlistEntry = suggestions_box.get(suggestions_box.curselection())
    print("Selected: "+selectedlistEntry)
    # fill in search bar with chosen suggestion and hide suggestions box
    searchBar.delete(0,END)
    searchBar.insert(0,selectedlistEntry)
    suggestions_box.delete(0,END)

_json = open("data/countrycodes.json","r") #countrycodes is a json I created utilizing the data from https://pkgstore.datahub.io/core/country-list/data_json/data/8c458f2d15d9f2119654b29ede6e45b8/data_json.json
countrycodes = json.loads(_json.read())
# Title canvas and frame around search bar
searchBorder = tk.Frame(root, bg="#F6f7f6",bd=-2)
searchBorder.place(relwidth = 1,relheight=0.5)
topcanvas = tk.Canvas(root, height = 110, width = 2555, bg = "#7bdaeb",bd=-2)
AppTitle = topcanvas.create_text(525,55,text="UbiWeather", font=("Calibri", 42))
AppIconImage = PhotoImage(file="weather icons/weather_app_icon.png")
AppIconImage = AppIconImage.subsample(2,2)
AppIcon = topcanvas.create_image(335,55,image=AppIconImage)
topcanvas.pack()
# Search bar and small margin above it
searchBarTopMargin = tk.Canvas(root, height = 20, width = 2555, bg = "#F6f7f6",bd=-2)
searchBarTopMargin.pack()
searchBar = Entry(root, width=40, justify=LEFT, relief="ridge",font= ('Calibri',24),bg="#E9ede9")
searchBar.pack(pady=0.5)
searchBar.bind("<KeyRelease>", readBar)
# Search Button
searchButton = tk.Button(root, height=1,width=15,relief="flat",font=('Calibri',15),text="Search", cursor="hand2", bg="#Bec0be")
searchButton.place(x=686,y=132)
searchButton.bind("<ButtonRelease>", searchCity)
# Main canvas
maincanvas = tk.Canvas(root, height = 1050, width = 2555, bg = "#F6f7f6",bd=-2)
maincanvas.create_polygon(getPolygonPoints(150, 45, 900, 650,r=100),fill="#E9ede9",smooth=True)
maincanvas.create_text(525,100,text="Sugar Land, United States", font=("Calibri", 28))
sugarland_weather = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Sugar+Land&appid=233fb10f061739fe6ced65c5f60ec5da&units=imperial").json()
sl_IconImage = PhotoImage(file="weather icons/{}.png".format(sugarland_weather['weather'][0]['icon']))
maincanvas.create_image(300,200,image=sl_IconImage)
maincanvas.create_text(450,170,text="Current", font=("Calibri", 20))
maincanvas.create_text(450,230,text=str(round(sugarland_weather['main']['temp']))+"°", font=("Calibri", 36))
maincanvas.create_text(600,170,text="High", font=("Calibri", 20))
maincanvas.create_text(600,230,text=str(round(sugarland_weather['main']['temp_max']))+"°", font=("Calibri", 36))
maincanvas.create_text(750,170,text="Low", font=("Calibri", 20))
maincanvas.create_text(750,230,text=str(round(sugarland_weather['main']['temp_min']))+"°", font=("Calibri", 36))
maincanvas.pack()
# Suggestions box
suggestions_box = Listbox(root, width=48,height=1,cursor="hand2", font=('Calibri',15), relief="raised", bg="#E9ede9",bd=0)
suggestions_box.bind("<<ListboxSelect>>",listSelect)

root.mainloop()