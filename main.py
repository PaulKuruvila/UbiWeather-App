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

def resizeWindow(e):
    global searchButtonx, button_location
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

def switchDegreesUnit(e):
    global alternateUnit, temp, temp_high, temp_low, c_tempdisplay, h_tempdisplay, l_tempdisplay
    print("altUnit value = "+alternateUnit)
    maincanvas.delete(c_tempdisplay)
    maincanvas.delete(h_tempdisplay)
    maincanvas.delete(l_tempdisplay)
    temp_value = int(temp[0:len(temp)-2])
    htemp_value = int(temp_high[0:len(temp_high)-2])
    ltemp_value = int(temp_low[0:len(temp_low)-2])
    if alternateUnit == "F":
        FahrenLabel.pack_forget()
        CelsiusLabel.pack()
        temp = str(round((temp_value*1.8)+32))+"°"+alternateUnit
        temp_high = str(round((htemp_value*1.8)+32))+"°"+alternateUnit
        temp_low = str(round((ltemp_value*1.8)+32))+"°"+alternateUnit
        alternateUnit = "C"
    else:
        CelsiusLabel.pack_forget()
        FahrenLabel.pack()
        temp = str(round((temp_value-32)*.5556))+"°"+alternateUnit
        temp_high = str(round((htemp_value-32)*.5556))+"°"+alternateUnit
        temp_low = str(round((ltemp_value-32)*.5556))+"°"+alternateUnit
        alternateUnit = "F"
    c_tempdisplay = maincanvas.create_text(450,230,text=temp, font=("Calibri", 36))
    h_tempdisplay = maincanvas.create_text(750,230,text=temp_high, font=("Calibri", 36))
    l_tempdisplay = maincanvas.create_text(600,230,text=temp_low, font=("Calibri", 36))

def displayData(e, num_descr, _data):
    maincanvas.pack_forget()
    description = _data[0][0]
    icon = _data[1][0]
    global temp, temp_high, temp_low
    _city = _data[2]
    _location = _data[3]
    if(_data[4]):
        temp += 'C'
        temp_high += "C"
        temp_low += "C"
    else:
        temp += "F"
        temp_high += "F"
        temp_low += "F"
    weatherIcon = PhotoImage(file="weather icons/{}.png".format(icon))
    weatherIconLabel = Label(image=weatherIcon)
    weatherIconLabel.image = weatherIcon
    if num_descr == 1:
        maincanvas.create_polygon(getPolygonPoints(150, 45, 900, 650,r=100),fill="#E9ede9",smooth=True)
        maincanvas.create_text(525,100,text=_city, font=("Calibri", 28))
        maincanvas.create_image(300,200,image=weatherIcon)
        maincanvas.create_text(450,170,text="Current", font=("Calibri", 20))
        maincanvas.create_text(450,230,text=temp, font=("Calibri", 36))
        maincanvas.create_text(750,170,text="High", font=("Calibri", 20))
        maincanvas.create_text(750,230,text=temp_high, font=("Calibri", 36))
        maincanvas.create_text(600,170,text="Low", font=("Calibri", 20))
        maincanvas.create_text(600,230,text=temp_low, font=("Calibri", 36))
        maincanvas.create_text(800,75,text=_location, font=("Calibri", 10))
        maincanvas.pack()
    elif num_descr == 2:
        description2 = _data[0][1]
        icon2 = _data[1][1]
        maincanvas.create_polygon(getPolygonPoints(50, 50, 500, 650,r=100),fill="#E9ede9",smooth=True)
        maincanvas.create_polygon(getPolygonPoints(550, 50, 1000, 650,r=100),fill="#E9ede9",smooth=True)
        maincanvas.pack()
    else:
        print("Unexpected error; Invalid values received")
        return
    
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
    is_metric = TRUE
    if country_code == "US" or country_code == "LR" or country_code == "MM":
        url+="&units=imperial"
        is_metric = FALSE
    else:
        url+="&units=metric"
    weather_data = requests.get(url).json()
    # get all key weather info and create empty lists for storing weather descriptions and their respective weather icons (this is for cases where there may be more than one weather description)
    city = weather_data['name']+", "+countrycodes[country_code]
    location = "("+str(weather_data['coord']['lat'])+"°, "+str(weather_data['coord']['lon'])+"°)"
    global temp, temp_high, temp_low
    temp = str(round(weather_data['main']['temp']))+"°"
    temp_high = str(round(weather_data['main']['temp_max']))+"°"
    temp_low = str(round(weather_data['main']['temp_min']))+"°"
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
    data_to_display = [weather_descriptions,weather_icons,city,location,is_metric]
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
button_location = 1010
searchButtonx = 686
searchButton.bind("<ButtonRelease>", searchCity)
# Main canvas
maincanvas = tk.Canvas(root, height = 1050, width = 2555, bg = "#F6f7f6",bd=-2)
maincanvas.create_polygon(getPolygonPoints(150, 45, 900, 650,r=100),fill="#E9ede9",smooth=True)
maincanvas.create_text(525,100,text="Sugar Land, United States", font=("Calibri", 28))
sugarland_weather = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Sugar+Land&appid=233fb10f061739fe6ced65c5f60ec5da&units=imperial").json()
sl_IconImage = PhotoImage(file="weather icons/{}.png".format(sugarland_weather['weather'][0]['icon']))
temp = str(round(sugarland_weather['main']['temp']))+"°F"
temp_high = str(round(sugarland_weather['main']['temp_max']))+"°F"
temp_low = str(round(sugarland_weather['main']['temp_min']))+"°F"
maincanvas.create_image(300,200,image=sl_IconImage)
c_templabel = maincanvas.create_text(450,170,text="Current", font=("Calibri", 20))
c_tempdisplay = maincanvas.create_text(450,230,text=temp, font=("Calibri", 36))
h_templabel = maincanvas.create_text(750,170,text="High", font=("Calibri", 20))
h_tempdisplay = maincanvas.create_text(750,230,text=temp_high, font=("Calibri", 36))
l_templabel = maincanvas.create_text(600,170,text="Low", font=("Calibri", 20))
l_tempdisplay = maincanvas.create_text(600,230,text=temp_low, font=("Calibri", 36))
maincanvas.create_text(800,75,text="("+str(sugarland_weather['coord']['lat'])+"°, "+str(sugarland_weather['coord']['lon'])+"°)", font=("Calibri", 10))
maincanvas.pack()
# Metric/Imperial Unit Button
alternateUnit = "C"
CButton = tk.LabelFrame(maincanvas,cursor="hand2",bg="#E9ede9",relief="flat")
CButton.place(x=225,y=75)
FahrenLabel = tk.Label(CButton,height=1,width=5,text="°F",font=('Calibri',12),bg="#E9ede9")
CelsiusLabel = tk.Label(CButton,height=1,width=5,text="°C",font=('Calibri',12),bg="#E9ede9")
CelsiusLabel.pack()
CelsiusLabel.bind("<ButtonRelease>",switchDegreesUnit)
FahrenLabel.bind("<ButtonRelease>",switchDegreesUnit)
# Suggestions box
suggestions_box = Listbox(root, width=48,height=1,cursor="hand2", font=('Calibri',15), relief="raised", bg="#E9ede9",bd=0)
suggestions_box.bind("<<ListboxSelect>>",listSelect)

root.mainloop()