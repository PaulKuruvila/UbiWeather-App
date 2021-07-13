from pprint import pprint
import requests
import json
import tkinter as tk
from tkinter import *#filedialog, Text, messagebox, simpledialog, Entry
#import os

root = tk.Tk()
root.title("UbiWeather")
#root.iconphoto('weather icons\01d.png')
root.geometry("1050x900")
root.maxsize(height=1150,width=1050)
root.minsize(height=550,width=968)

button_location = 1010
searchButtonx = 847
def resizeWindow(e):
    dif = e.width-button_location
    if dif<40:
        change_in_x = 847-((40-dif)/2)
        if not dif<-43:
            searchButton.place(x=change_in_x, y=100)
    elif dif>40:
        change_in_x = (dif-40)/2
        searchButton.place(x=searchButtonx+change_in_x,y=100)
    else:
        searchButton.place(x=847, y=100)

root.bind('<Configure>', resizeWindow)

#while button pressed and text != "", display search suggestions
justSelected = False
justEmpty = True
def searchSuggestions(e):
    global justSelected
    global justEmpty
    # read what is typed
    currentSearch = searchBar.get()
    suggestions_box.delete(0,END)
    print("justSelected = "+str(justSelected))
    print("justEmpty = "+str(justEmpty))

    # if there is nothing typed, show no suggestions (hide the suggestions box)
    if currentSearch == '':
        print("Search bar is empty")
        suggestions_box.place_forget()
        justSelected = False
        justEmpty = True
    else:
        print("Search bar: "+searchBar.get())
        # check if there are any suggestions
        #if :
        # don't suggest anything if a suggestion was just chosen
        if not justSelected:
            suggestions_box.place(x=204,y=143)
            # Display what is being typed
            suggestions_box.insert(0, searchBar.get())
            if justEmpty:
                print("trying to fix buggy error")
                e.xview_scroll(1, tk.UNITS)
        else:
            suggestions_box.place_forget()
        justEmpty = False

def searchCity(e):
    print("Search")
    suggestions_box.place_forget()
    cityname = []#simpledialog.askstring("Input", "What is your first name?", parent=root)

def listSelect(e):
    global justSelected
    selectedlistEntry = suggestions_box.get(suggestions_box.curselection())

    print("Selected: "+selectedlistEntry)
    justSelected = True
    # fill in search bar with chosen suggestion and hide suggestions box
    searchBar.delete(0,END)
    searchBar.insert(0,selectedlistEntry)
    suggestions_box.delete(0,END)
    suggestions_box.place_forget()

# Title canvas and frame around search bar
searchBorder = tk.Frame(root, bg="#7bdaeb",bd=-2)
searchBorder.place(relwidth = 1,relheight=0.5)
topcanvas = tk.Canvas(root, height = 85, width = 2555, bg = "#72d23e",bd=-2)
AppTitle = topcanvas.create_text(525,45,text="UbiWeather", font=("Calibri", 36))
topcanvas.pack()
# Search bar and small margin above it
searchBarTopMargin = tk.Canvas(root, height = 15, width = 2555, bg = "#7bdaeb",bd=-2)
searchBarTopMargin.pack()
searchBar = Entry(root, width=40, justify=LEFT, relief="groove",font= ('Calibri',24),bg="#E9ede9")
searchBar.pack()
searchBar.bind("<KeyRelease>", searchSuggestions)
# Search Button
searchButton = tk.Button(root, height=1,width=15,font=('Calibri',15),text="Search", cursor="hand2", bg="#Bec0be")
searchButton.place(x=847,y=100)
#searchButton.bind("<KeyRelease>", searchCity)
# Main canvas
canvas = tk.Canvas(root, height = 1050, width = 2555, bg = "#7bdaeb",bd=-2)
canvas.pack()
# Suggestions box
suggestions_box = Listbox(root, width=64,cursor="hand2", font=('Calibri',15), relief="raised", bg="#E9ede9")
suggestions_box.pack(expand="YES")
suggestions_box.place(x=204,y=143)
suggestions_box.place_forget()
suggestions_box.bind("<<ListboxSelect>>",listSelect)

root.mainloop()