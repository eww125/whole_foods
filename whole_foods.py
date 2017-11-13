dublin_whole_foods = [37.70577, -121.88984]
from urllib2 import urlopen
from json import load, dumps
from time import time
t = time()

# api_key import
import os
home_dir =  os.path.expanduser('~')
directory_path = home_dir + "/api_keys/"
f = open(directory_path + 'google_places', 'r')
API_KEY = f.read().rstrip()
f.close()
print "API_KEY=" + API_KEY

#build the url
url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
url += '37.70577,-121.88984'
url += '&rankby=distance&types=grocery_or_supermarket&name=%27Whole%20Foods%20Market%27&key='
url += API_KEY
print "url="
print url


response = urlopen(url)
json_obj = load(response)

# uncomment 3 lines below to see JSON output to file
f = open('output.json', 'w')
f.write(dumps(json_obj, indent=4))
f.close()

store_list = []
for x in range (len(json_obj['results'])):
    # extract name
    store_name = json_obj['results'][x]['name']
    # extract address
    store_address = json_obj['results'][x]['vicinity']
    # extract lat
    store_lat = json_obj['results'][x]['geometry']['location']['lat']
    # extract lon
    store_lon = json_obj['results'][x]['geometry']['location']['lng']
    store_list.append([store_name, store_address, store_lat, store_lon])

print store_list

"""
# convert to point
import polyline
polyline_list = polyline.decode(polyline_str)

# write to csv
import pandas as pd
df = pd.DataFrame(polyline_list)
df.columns = ['lat', 'lon']
print df
df.to_csv('data.csv', index=False)

import csv

# Read in raw data from csv
rawData = csv.reader(open('data.csv', 'rb'), dialect='excel')

coordinate_list=[]
# loop through the csv by row skipping the first
iter = 0
for row in rawData:
    iter += 1
    if iter >= 2:
        lat = row[0]
        lon = row[1]
        coordinate_list.append("[" + lon + ", " + lat + "]")

final_string = '{"type":"LineString","coordinates":['
final_string += ",".join(str(x) for x in coordinate_list)
final_string += "]}"
print final_string

# opens an geoJSON file to write the output to
outFileHandle = open(origin_name + "_" + destination_name + ".geojson", "w")
outFileHandle.write(final_string)
outFileHandle.close()
"""

print "complete!"
print "Time elapsed: " + str(time() - t) + " s."
