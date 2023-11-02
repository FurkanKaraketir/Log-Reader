import os
import json
import re
from gmplot import gmplot
import webbrowser  # Import the webbrowser module
import simplekml  # Import the simplekml library
import time
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw() 
# Define lists to store Lat, Long, and Alt values
timestamp = []
latitudes = []
longitudes = []
altitudes = []


def extract_lat_long_alt(line):
    # Split the line into tokens
    tokens = line.split(', ')

    # Check if the line starts with "GPS" and has enough tokens
    if len(tokens) >= 10 and tokens[0] == "GPS":
        # Extract the Lat, Long, and Alt values
        Time = float(tokens[1])
        Lat = float(tokens[8])
        Long = float(tokens[9])
        Alt = float(tokens[10])
        return Lat, Long, Alt, Time

    # Return None if the line doesn't contain GPS data
    return None



# Replace 'main.log' with your actual log file path
log_file_path = filedialog.askopenfilename(
    filetypes=[("Log files", "*.log")],
    title="Select a .log file"
)
with open(log_file_path, "r") as file:
    lines = file.readlines()
# Iterate through the lines and extract Lat, Long, and Alt
for line in lines:
    result = extract_lat_long_alt(line)
    if result is not None:
        Lat, Long, Alt, Time = result
        latitudes.append(Lat)
        longitudes.append(Long)
        altitudes.append(Alt)
        timestamp.append(Time)

latitude1 = latitudes[0]
longitude1 = longitudes[0]


gmap = gmplot.GoogleMapPlotter(latitude1, longitude1, 18)


# set mode to satellite
gmap.map_type = 'satellite'

# set api key
gmap.apikey = "AIzaSyCK9CucXXjSuf2dmN3RY-XCLdFdb735zco"

# Add markers for specific GPS points
for lat, lon in zip(latitudes, longitudes):
    gmap.marker(lat, lon, title='Marker')

# Save the Google Map to an HTML file
html_file_path = 'C:/Users/furka/Downloads/Log Reader/map_for_browser.html'
gmap.draw(html_file_path)

kmz_file_path = 'C:/Users/furka/Downloads/Log Reader/map_for_earth.kmz'
kml_file_path = 'C:/Users/furka/Downloads/Log Reader/map_for_earth.kml'

# Create a KML object
kml = simplekml.Kml()
folder = kml.newfolder(name='Markers')

# Add Placemarks for each marker
for lat, lon, alt in zip(latitudes, longitudes, altitudes):
    placemark = folder.newpoint()
    placemark.coords = [(lon, lat, alt)]  # Include altitude data
    placemark.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png'

    # Set altitude mode to clampToGround for 3D effect
    placemark.altitudemode = simplekml.AltitudeMode.relativetoground
    placemark.altitude = alt  # Adjust the altitude value as needed
# Save the KMZ file
kml.savekmz(kmz_file_path)

#draw graph for altitude
plt.plot(altitudes)
plt.ylabel('Altitude')
plt.xlabel('Time')
plt.title('Altitude Graph')

# Automatically open the HTML file in the default web browser
webbrowser.open('file://' + os.path.realpath(html_file_path))

os.startfile(kmz_file_path)


plt.show()
