#!/usr/bin/env python

# README #
# Add icon to /usr/share/icons/hicolor
# sudo gtk-update-icon-cache -f /usr/share/icons/hicolor/
# Obtain StopName from http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=umd&r=<BusNumber>
# Modify bus_config.ini as applicable

# IMPORTS #
import urllib
import xml.etree.ElementTree as ET
import os
import ConfigParser

# CONFIG PARSER #
Config = ConfigParser.ConfigParser()
Config.read("bus_config.ini")
busNumber = Config.get("Travel","BusNumber")
stopName = Config.get("Travel","StopName")

# GET PREDICTION DATA #
link = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=umd&r=" + busNumber + "&s=" + stopName
print link
f = urllib.urlopen(link)
predTxt = f.read()

# PARSE XML #
root = ET.fromstring(predTxt)

details = root.findall("./predictions")
for i in details:
	route = i.attrib["routeTitle"]
	stop = i.attrib["stopTitle"]

dir_details = root.findall("./predictions/direction")
for i in dir_details:
	direction = i.attrib["title"]

time_details = root.findall("./predictions/direction/prediction")
if len(time_details) == 2:
	time1 = time_details[0].attrib["minutes"]
	time2 = time_details[1].attrib["minutes"]
else:
	time = time_details[0].attrib["minutes"]


# LIBNOTIFY #
if len(time_details) == 2:
	msg = 'notify-send -u critical -i resize_bus -t 1000 "Bus Schedule" "' + route + '\n From: ' + stop + '\n Towards: ' + direction + '\n Arriving in: ' + time1 + ' AND ' + time2 + ' min"'
else:
	msg = 'notify-send -u critical -i resize_bus -t 1000 "Bus Schedule" "' + route + '\n From: ' + stop + '\n Towards: ' + direction + '\n Arriving in: ' + time + ' min"'
os.system(msg)