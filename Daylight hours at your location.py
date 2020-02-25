# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 23:13:35 2020

@author: juanv
"""
import json, requests, geocoder, sys
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter as ff

def get_loc(lat,lon): # Accepts two parameters: latitude, and longitude
    for i in range(1,13):
        params = {"lat":lat,"lng":lon, "date":"2019-"+str('%02d' % i)+"-01"}
        response = requests.get("https://api.sunrise-sunset.org/json", params=params)
        response_dic = json.loads(response.content)
        dl_str = response_dic["results"]["day_length"]
        dl_dt = datetime.strptime(dl_str,"%H:%M:%S").time() #Converting string to datetime object
        info[i] = dl_dt
    
def m2hm(x, i): #Formating the time 
    h = int(x/60)
    return '%(h)02d' % {'h':h}

print("\n\nThis program creates a graph of the daylight hours at your city throughout the year.\n\nAfter successful execution check the path where this script is located to find the .PDF file with the graph.")
input("\nPress Enter to continue...\n")

try:
    info = {} #dictionary containing returned values from function "get_loc"
    latlon = geocoder.ip('me').latlng #Using the geocoder module to get user´s location
    get_loc(lat=latlon[0],lon=latlon[1]) #Getting the lat and lon of the user´s location
    city = geocoder.ip('me').city #City name of the user
except Exception as ex:
    template = "\n\nAn exception of type {0} occurred. Arguments:\n\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)
    sys.exit(print ("\n\nConnection error: couldn't retrieve user's location.\n\n"))
    

#Converting the datetime object returned by function "get_loc" to minutes in int
info_dl_dt = list(info.values())
info_dl_min = [i.minute + (i.hour*60) for i in info_dl_dt]
   
month_list = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 
              'August', 'September', 'October', 'November', 'December']

#Creating the line chart    
fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(1,1,1)
#Formating the Y axis
ax.yaxis.set_major_formatter(ff(m2hm))
ax.yaxis.set_major_locator(plt.MultipleLocator(60))
#Typical plot stuff
plt.plot(month_list,info_dl_min, c="red", linewidth = 2)
plt.xlabel("Month", fontsize=18)
plt.ylabel("Hours", fontsize=18)
plt.xticks(rotation=90)
plt.title("Hours of day light in " + str(city), fontsize=24)
#From 4 hours to 18 hours
ax.set_ylim((4*60),(18*60))
#Turning off ticks and spines
ax.tick_params(left="off",bottom="off")
for key, spine in ax.spines.items():
    spine.set_visible(False)
#Filling the area under the plot 
plt.fill_between(month_list, info_dl_min, 0,
                 facecolor="yellow",
                 color="red",     
                 alpha=0.2) 

#Saving the plot at the same directory the script is located      
plt.savefig("Daylight " + str(city) +".pdf")
plt.show()

print("Please check the path where this script is located to find your .PDF file.")
