# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 21:04:18 2020

@author: juanv
"""

import json
import requests
import geocoder
from datetime import datetime, timedelta



#The following function uses an API to return some relevant info
#updates the "info" dictionary
def get_time(lat,lon): # Accepts two parameters: latitude, and longitude
    params = {"lat":lat,"lng":lon}
    response = requests.get("https://api.sunrise-sunset.org/json", params=params)
    response_dic = json.loads(response.content)
    info.update(response_dic["results"])
    
    


print("\n\nA simple program that tells you some information about the sunset and the sunrise at your location")
input("\nPress Enter to continue...\n")


info = {} #dictionary containing the information that the API sends
latlon = geocoder.ip('me').latlng #Using the geocoder module to get user´s location
get_time(lat=latlon[0],lon=latlon[1])

#Converting to the correct time zone by creating datetime objects
sunrise_str = info["sunrise"]
sunrise_dt = datetime.strptime(sunrise_str,"%I:%M:%S %p")
sunset_str = info["sunset"]
sunset_dt = datetime.strptime(sunset_str,"%I:%M:%S %p")
dl_str = info["day_length"]
dl_dt = datetime.strptime(dl_str,"%I:%M:%S")
sunrise = (sunrise_dt + timedelta(hours=1)).time()
sunset = (sunset_dt + timedelta(hours=1)).time()
daylight = dl_dt.time()

print("\n\nThe sunset in " + str(geocoder.ip('me').city) + " is at " + str(sunset))

print("\nThe sunrise in " + str(geocoder.ip('me').city) + " is at " +str(sunrise))

print("\n" + str(geocoder.ip('me').city) + " has " +str(daylight.hour)+" hours and "+str(daylight.minute)+" minutes of day light at this moment of the year.")