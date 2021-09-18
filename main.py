from pprint import pprint
import requests
import datetime
import json
import tkinter as tk
from tkinter import *#filedialog, Text, messagebox, simpledialog, Entry
#import os

root = tk.Tk()
root.title("UbiWeather - Weather Anywhere and Everywhere")
root.iconbitmap('weather icons/weather_app_icon.ico')
root.geometry("750x642")
root.maxsize(height=642,width=750)
root.minsize(height=642,width=750)

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

def containsNumbers(string):
        for char in string:
            if char.isdigit():
                return TRUE
        return FALSE

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
        suggestions_box.place(x=54,y=174)
        # Display what is being typed
        suggestions_box.insert(0, searchBar.get())
        # check if there are any suggestions
        #if :

def switchDegreesUnit(e):
    global alternateUnit, temp, temp_high, temp_low, c_tempdisplay, h_tempdisplay, l_tempdisplay, forecast_temps, forecast_display
    print("altUnit value = "+alternateUnit)
    maincanvas.delete(c_tempdisplay)
    maincanvas.delete(h_tempdisplay)
    maincanvas.delete(l_tempdisplay)
    for each_label in forecast_display:
        maincanvas.delete(each_label)
    forecast_display = []
    temp_value = int(temp[0:len(temp)-2])
    htemp_value = int(temp_high[0:len(temp_high)-2])
    ltemp_value = int(temp_low[0:len(temp_low)-2])
    index = 0
    x1 = 60
    x2 = 160
    if alternateUnit == "F":
        FahrenLabel.pack_forget()
        CelsiusLabel.pack()
        temp = str(round((temp_value*1.8)+32))+"°"+alternateUnit
        temp_high = str(round((htemp_value*1.8)+32))+"°"+alternateUnit
        temp_low = str(round((ltemp_value*1.8)+32))+"°"+alternateUnit
        while index < 11:
            forecast_temps[index] = round((forecast_temps[index]*1.8)+32)
            forecast_temps[index+1] = round((forecast_temps[index+1]*1.8)+32)
            templabel = maincanvas.create_text((x1+x2)/2,391,text=str(forecast_temps[index])+"/"+str(forecast_temps[index+1])+"°F", font=("Calibri", 18))
            forecast_display.append(templabel)
            x1 = x1 + 106
            x2 = x2 + 106
            index = index + 2
        alternateUnit = "C"
    else:
        CelsiusLabel.pack_forget()
        FahrenLabel.pack()
        temp = str(round((temp_value-32)*.5556))+"°"+alternateUnit
        temp_high = str(round((htemp_value-32)*.5556))+"°"+alternateUnit
        temp_low = str(round((ltemp_value-32)*.5556))+"°"+alternateUnit
        while index < 11:
            forecast_temps[index] = round((forecast_temps[index]-32)*.5556)
            forecast_temps[index+1] = round((forecast_temps[index+1]-32)*.5556)
            templabel = maincanvas.create_text((x1+x2)/2,391,text=str(forecast_temps[index])+"/"+str(forecast_temps[index+1])+"°C", font=("Calibri", 18))
            forecast_display.append(templabel)
            x1 = x1 + 106
            x2 = x2 + 106
            index = index + 2
        alternateUnit = "F"
        #print(forecast_temps)
    c_tempdisplay = maincanvas.create_text(310,180,text=temp, font=("Calibri", 36))
    h_tempdisplay = maincanvas.create_text(460,180,text=temp_high, font=("Calibri", 36))
    l_tempdisplay = maincanvas.create_text(610,180,text=temp_low, font=("Calibri", 36))


def displayForecast(e, _lat, _lon, unit_metric):
    global forecast_display, forecast_temps
    for each_label in forecast_display:
        maincanvas.delete(each_label)
    forecast_display = []
    week_days = ['Sun', 'Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat']
    current_day = datetime.datetime.now().strftime('%a')
    print("Current day = " + str(current_day))
    day_pos = -1 # variable used to store position of current day in week_days array
    for day in week_days:
        day_pos = day_pos + 1
        if day == current_day:
            break
    upcoming_days = []
    this_week_days = []
    next_week_days = []
    index = -1
    for day in week_days:
        index = index + 1
        if index < day_pos:
            next_week_days.insert(index,day)
        elif index > day_pos:
            this_week_days.insert(index,day)
    upcoming_days = this_week_days + next_week_days
    #print(upcoming_days)
    specified_unit = 'metric'
    unit_symbol = 'C'
    if(not unit_metric):
        specified_unit = 'imperial'
        unit_symbol = 'F'
    city_forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid=233fb10f061739fe6ced65c5f60ec5da&units={}".format(_lat,_lon,specified_unit)
    city_forecast = requests.get(city_forecast_url).json()
    pprint(city_forecast)
    index = 1
    x1 = 60
    x2 = 160
    maincanvas.create_polygon(getPolygonPoints(x1, 265, x2, 427,r=100),fill="#bebecf",smooth=True)
    templabel = maincanvas.create_text(110,391,text=str(round(city_forecast['daily'][index]['temp']['max']))+"/"+str(round(city_forecast['daily'][index]['temp']['min']))+"°"+unit_symbol, font=("Calibri", 18))
    forecast_temps = [round(city_forecast['daily'][index]['temp']['max']), round(city_forecast['daily'][index]['temp']['min'])]
    forecast_display.append(templabel)
    forecast_IconImage = PhotoImage(file="weather icons/{}.png".format(city_forecast['daily'][index]['weather'][0]['icon']))
    forecast_IconImage = forecast_IconImage.subsample(2,2)
    icon_label = Label(image=forecast_IconImage)
    icon_label.image = forecast_IconImage
    #print(sugarland_forecast['daily'][index]['weather'][0]['icon'])
    maincanvas.create_image(110,340,image=forecast_IconImage)
    maincanvas.create_text(110,286,text=upcoming_days[0], font=("Calibri", 18))
    for each_day in upcoming_days:
        if index == 1:
            index = index + 1
            continue
        index = index + 1
        x1 = x1 + 106
        x2 = x2 + 106
        maincanvas.create_polygon(getPolygonPoints(x1, 265, x2, 427,r=100),fill="#bebecf",smooth=True)
        templabel = maincanvas.create_text((x1+x2)/2,391,text=str(round(city_forecast['daily'][index]['temp']['max']))+"/"+str(round(city_forecast['daily'][index]['temp']['min']))+"°"+unit_symbol, font=("Calibri", 18))
        forecast_temps.append(round(city_forecast['daily'][index]['temp']['max']))
        forecast_temps.append(round(city_forecast['daily'][index]['temp']['min']))
        forecast_display.append(templabel)
        forecast_IconImage = PhotoImage(file="weather icons/{}.png".format(city_forecast['daily'][index]['weather'][0]['icon']))
        forecast_IconImage = forecast_IconImage.subsample(2,2)
        icon_label = Label(image=forecast_IconImage)
        icon_label.image = forecast_IconImage
        maincanvas.create_image((x1+x2)/2,340,image=icon_label.image)
        maincanvas.create_text((x1+x2)/2,286,text=each_day, font=("Calibri", 18))
    
def displayData(e, _data):
    maincanvas.pack_forget()
    global c_tempdisplay, h_tempdisplay, l_tempdisplay
    maincanvas.delete(c_tempdisplay)
    maincanvas.delete(h_tempdisplay)
    maincanvas.delete(l_tempdisplay)
    global temp, temp_high, temp_low
    _city = _data[2]
    _location = _data[3]
    if(_data[4]):
        temp += 'C'
        temp_high += "C"
        temp_low += "C"
        FahrenLabel.pack()
    else:
        temp += "F"
        temp_high += "F"
        temp_low += "F"
        CelsiusLabel.pack()
    DegreesButton.place(x=175,y=230)
    RefreshButton.place(x=125,y=230)
    RefreshLabel.pack()
    weatherIcon = PhotoImage(file="weather icons/{}.png".format(_data[1]))
    weatherIconLabel = Label(image=weatherIcon)
    weatherIconLabel.image = weatherIcon
    maincanvas.create_polygon(getPolygonPoints(50, 20, 700, 442,r=100),fill="#d0d1d9",smooth=True)
    maincanvas.create_text(365,60,text=_city, font=("Calibri", 28))
    maincanvas.create_image(165,150,image=weatherIcon)
    maincanvas.create_text(310,120,text="Current", font=("Calibri", 18))
    c_tempdisplay = maincanvas.create_text(310,180,text=temp, font=("Calibri", 36))
    maincanvas.create_text(460,120,text="High", font=("Calibri", 18))
    h_tempdisplay = maincanvas.create_text(460,180,text=temp_high, font=("Calibri", 36))
    maincanvas.create_text(610,120,text="Low", font=("Calibri", 18))
    l_tempdisplay = maincanvas.create_text(610,180,text=temp_low, font=("Calibri", 36))
    maincanvas.create_text(600,35,text=_location, font=("Calibri", 10))
    maincanvas.create_text(450,230,text=_data[0],font=("Calibri", 24), fill="white")
    maincanvas.pack()
    
def searchCity(e):
    global city_entered, refreshed
    print("refreshed == "+str(refreshed))
    if not refreshed:
        city_entered = searchBar.get();
    else:
        refreshed = FALSE
    if city_entered == '':
        return
    if refreshed:
        print("Page refreshed.")
    suggestions_box.place_forget()
    searchBar.delete(0,END)
    maincanvas.delete("all")
    global alternateUnit
    if alternateUnit == "C":
        CelsiusLabel.pack_forget()
    else:
        FahrenLabel.pack_forget()
    DegreesButton.place_forget()
    RefreshLabel.pack_forget()
    RefreshButton.place_forget()

    print("Attempting to search for "+city_entered+"...")
    if containsNumbers(city_entered): # Makes sure that the entered city name does not have any numbers in it
        print("Invalid city name")
        NoResults = maincanvas.create_text(375,105,justify='center',text="City not found.\nMake sure you only enter the city's name.\n(e.g. Abu Dhabi)", font=("Calibri", 18))
        return

    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=233fb10f061739fe6ced65c5f60ec5da".format(city_entered)
    weekly_forecast_url = "http://api.openweathermap.org/data/2.5/forecast/daily?q={}&cnt=7&appid=".format(city_entered)
    try:
        weather_data = requests.get(url).json()
        country_code = weather_data["sys"]["country"]
    except KeyError as InvalidCity:
        print("Invalid city name")
        NoResults = maincanvas.create_text(375,105,justify='center',text="City not found.\nMake sure you only enter the city's name.\n(e.g. Abu Dhabi)", font=("Calibri", 18))
        return
    is_metric = TRUE
    if country_code == "US" or country_code == "LR" or country_code == "MM":
        url+="&units=imperial"
        weekly_forecast_url+="&units=imperial"
        is_metric = FALSE
        alternateUnit = "C"
    else:
        url+="&units=metric"
        weekly_forecast_url+="&units=metric"
        alternateUnit = "F"
    weather_data = requests.get(url).json()
    weekly_forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid=233fb10f061739fe6ced65c5f60ec5da".format(weather_data['coord']['lat'], weather_data['coord']['lon'])
    if is_metric:
        weekly_forecast_url+="&units=metric"
    else:
        weekly_forecast_url+="&units=imperial"
    forecast_data = requests.get(weekly_forecast_url).json()
    #pprint(forecast_data)
    # get all key weather info and create empty lists for storing weather descriptions and their respective weather icons (this is for cases where there may be more than one weather description)
    city = weather_data['name']+", "+countrycodes[country_code]
    location = "("+str(weather_data['coord']['lat'])+"°, "+str(weather_data['coord']['lon'])+"°)"
    global temp, temp_high, temp_low
    temp = str(round(weather_data['main']['temp']))+"°"
    temp_high = str(round(weather_data['main']['temp_max']))+"°"
    temp_low = str(round(weather_data['main']['temp_min']))+"°"
    weather = weather_data['weather']
    weather_description = weather_data['weather'][0]['description']
    weather_icon = weather_data['weather'][0]['icon']
    pprint(weather_data)
    data_to_display = [weather_description,weather_icon,city,location,is_metric]
    displayData(e, data_to_display)
    displayForecast(e, weather_data['coord']['lat'], weather_data['coord']['lon'], is_metric)

refreshed = False # global variable that checks if user refreshed page
def refresh(e):
    global refreshed
    refreshed = TRUE
    print("Refreshing page...")
    searchCity(e)

def listSelect(e):
    selectedlistEntry = suggestions_box.get(suggestions_box.curselection())
    print("Selected: "+selectedlistEntry)
    # fill in search bar with chosen suggestion and hide suggestions box
    searchBar.delete(0,END)
    searchBar.insert(0,selectedlistEntry)
    suggestions_box.delete(0,END)
    suggestions_box.place_forget()

_json = open("data/countrycodes.json","r") #countrycodes is a json I created utilizing the data from https://pkgstore.datahub.io/core/country-list/data_json/data/8c458f2d15d9f2119654b29ede6e45b8/data_json.json
countrycodes = json.loads(_json.read())
# Title canvas and frame around search bar
searchBorder = tk.Frame(root, bg="#F6f7f6",bd=-2)
searchBorder.place(relwidth = 1,relheight=0.5)
topcanvas = tk.Canvas(root, height = 110, width = 2555, bg = "#F6f7f6",bd=-2)
topcanvas.create_polygon(getPolygonPoints(50, 10, 700, 110,r=120),fill="#c3dfe0",smooth=True)
AppTitle = topcanvas.create_text(400,60,text="UbiWeather", font=("Calibri", 42))
AppIconImage = PhotoImage(file="weather icons/weather_app_icon.png")
AppIconImage = AppIconImage.subsample(2,2)
AppIcon = topcanvas.create_image(200,60,image=AppIconImage)
topcanvas.pack()
# Search bar and small margin above it
searchBarTopMargin = tk.Canvas(root, height = 20, width = 2555, bg = "#F6f7f6",bd=-2)
searchBarTopMargin.pack()
searchBar = Entry(root, width=40, justify=LEFT, relief="ridge",font= ('Calibri',24),bg="#E9ede9")
searchBar.pack(pady=0.5)
searchBar.bind("<KeyRelease>", readBar)
# Search Button
city_entered = ""
searchButton = tk.Button(root, height=1,width=15,relief="flat",font=('Calibri',15),text="Search", cursor="hand2", bg="#Bec0be")
searchButton.place(x=536,y=132)
button_location = 1010
searchButtonx = 536
searchButton.bind("<ButtonRelease>", searchCity)
# Main canvas
maincanvas = tk.Canvas(root, height = 1050, width = 2555, bg = "#F6f7f6",bd=-2)
maincanvas.create_polygon(getPolygonPoints(50, 20, 700, 442,r=100),fill="#d0d1d9",smooth=True)
city_entered = "Sugar Land, United States"
maincanvas.create_text(365,60,text=city_entered, font=("Calibri", 28))
sugarland_weather = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Sugar+Land&appid=233fb10f061739fe6ced65c5f60ec5da&units=imperial").json()
sl_IconImage = PhotoImage(file="weather icons/{}.png".format(sugarland_weather['weather'][0]['icon']))
#sl_IconImage = sl_IconImage.subsample(2,2)
temp = str(round(sugarland_weather['main']['temp']))+"°F"
temp_high = str(round(sugarland_weather['main']['temp_max']))+"°F"
temp_low = str(round(sugarland_weather['main']['temp_min']))+"°F"
maincanvas.create_image(165,150,image=sl_IconImage)
c_templabel = maincanvas.create_text(310,120,text="Current", font=("Calibri", 18))
c_tempdisplay = maincanvas.create_text(310,180,text=temp, font=("Calibri", 36))
h_templabel = maincanvas.create_text(460,120,text="High", font=("Calibri", 18))
h_tempdisplay = maincanvas.create_text(460,180,text=temp_high, font=("Calibri", 36))
l_templabel = maincanvas.create_text(610,120,text="Low", font=("Calibri", 18))
l_tempdisplay = maincanvas.create_text(610,180,text=temp_low, font=("Calibri", 36))
maincanvas.create_text(600,35,text="("+str(sugarland_weather['coord']['lat'])+"°, "+str(sugarland_weather['coord']['lon'])+"°)", font=("Calibri", 10))
maincanvas.create_text(450,230,text=sugarland_weather['weather'][0]['description'],font=("Calibri", 24), fill="white")
maincanvas.pack()
# Upcoming Forecast
week_days = ['Sun', 'Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat']
current_day = datetime.datetime.now().strftime('%a')
print("Current day = " + str(current_day))
day_pos = -1 # variable used to store position of current day in week_days array
for day in week_days:
    day_pos = day_pos + 1
    if day == current_day:
        break
upcoming_days = []
this_week_days = []
next_week_days = []
index = -1
for day in week_days:
    index = index + 1
    if index < day_pos:
        next_week_days.insert(index,day)
    elif index > day_pos:
        this_week_days.insert(index,day)
upcoming_days = this_week_days + next_week_days
print(upcoming_days)
sugarland_forecast = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=29.6197&lon=-95.6349&exclude=current,minutely,hourly,alerts&appid=233fb10f061739fe6ced65c5f60ec5da&units=imperial").json()
#pprint(sugarland_forecast)
index = 1
x1 = 60
x2 = 160
forecast_temps = [round(sugarland_forecast['daily'][index]['temp']['max']), round(sugarland_forecast['daily'][index]['temp']['min'])] # array that stores max/min temps for the 6 day forecast, so that the temps can be altered by the switchDegrees function
forecast_display = []
maincanvas.create_polygon(getPolygonPoints(x1, 265, x2, 427,r=100),fill="#bebecf",smooth=True)
templabel = maincanvas.create_text(110,391,text=str(round(sugarland_forecast['daily'][index]['temp']['max']))+"/"+str(round(sugarland_forecast['daily'][index]['temp']['min']))+"°F", font=("Calibri", 18))
forecast_display.append(templabel)
forecast_IconImage = PhotoImage(file="weather icons/{}.png".format(sugarland_forecast['daily'][index]['weather'][0]['icon']))
forecast_IconImage = forecast_IconImage.subsample(2,2)
icon_label = Label(image=forecast_IconImage)
icon_label.image = forecast_IconImage
#print(sugarland_forecast['daily'][index]['weather'][0]['icon'])
maincanvas.create_image(110,340,image=forecast_IconImage)
maincanvas.create_text(110,286,text=upcoming_days[0], font=("Calibri", 18))
for each_day in upcoming_days:
    if index == 1:
        index = index + 1
        continue
    index = index + 1
    x1 = x1 + 106
    x2 = x2 + 106
    maincanvas.create_polygon(getPolygonPoints(x1, 265, x2, 427,r=100),fill="#bebecf",smooth=True)
    templabel = maincanvas.create_text((x1+x2)/2,391,text=str(round(sugarland_forecast['daily'][index]['temp']['max']))+"/"+str(round(sugarland_forecast['daily'][index]['temp']['min']))+"°F", font=("Calibri", 18))
    forecast_display.append(templabel)
    forecast_temps.append(round(sugarland_forecast['daily'][index]['temp']['max']))
    forecast_temps.append(round(sugarland_forecast['daily'][index]['temp']['min']))
    forecast_IconImage = PhotoImage(file="weather icons/{}.png".format(sugarland_forecast['daily'][index]['weather'][0]['icon']))
    forecast_IconImage = forecast_IconImage.subsample(2,2)
    icon_label = Label(image=forecast_IconImage)
    icon_label.image = forecast_IconImage
    #print(sugarland_forecast['daily'][index]['weather'][0]['icon'])
    maincanvas.create_image((x1+x2)/2,340,image=icon_label.image)
    maincanvas.create_text((x1+x2)/2,286,text=each_day, font=("Calibri", 18))
#print(forecast_temps)
# Refresh Button
RefreshButton = tk.LabelFrame(maincanvas,cursor="hand2",bg="#d0d1d9",relief="flat")
RefreshButton.place(x=125,y=230)
RefreshLabel = tk.Label(RefreshButton,height=1,width=5,text="Reload",font=('Calibri',11),bg="#d0d1d9")
RefreshLabel.pack()
RefreshLabel.bind("<ButtonRelease>",refresh)
# Metric/Imperial Unit Button
alternateUnit = "C"
DegreesButton = tk.LabelFrame(maincanvas,cursor="hand2",bg="#d0d1d9",relief="flat")
DegreesButton.place(x=175,y=230)
FahrenLabel = tk.Label(DegreesButton,height=1,width=5,text="°F",font=('Calibri',11),bg="#d0d1d9")
CelsiusLabel = tk.Label(DegreesButton,height=1,width=5,text="°C",font=('Calibri',11),bg="#d0d1d9")
CelsiusLabel.pack()
CelsiusLabel.bind("<ButtonRelease>",switchDegreesUnit)
FahrenLabel.bind("<ButtonRelease>",switchDegreesUnit)
# Suggestions box
suggestions_box = Listbox(root, width=48,height=1,cursor="hand2", font=('Calibri',15), relief="raised", bg="#E9ede9",bd=0)
suggestions_box.bind("<<ListboxSelect>>",listSelect)

root.mainloop()