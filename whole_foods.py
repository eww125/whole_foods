dublin_whole_foods = [37.70577, -121.88984]
van_ness_socal = [33.974876, -118.318013]

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
url += '33.974876,-118.318013'
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

print len(json_obj['results'])
store_list = []
for x in range (len(json_obj['results'])):
    # extract name
    name = json_obj['results'][x]['name']
    # extract address
    address = json_obj['results'][x]['vicinity']
    # extract lat
    lat = json_obj['results'][x]['geometry']['location']['lat']
    # extract lon
    lon = json_obj['results'][x]['geometry']['location']['lng']
    store_list.append([name, address, lat, lon])

print store_list

# write to csv
import pandas as pd
df = pd.DataFrame(store_list)
df.columns = ['name', 'address', 'lat', 'lon']
print df
df.to_csv('whole_foods.csv', index=False)
"""
import csv

# Read in raw data from csv
rawData = csv.reader(open('whole_foods.csv', 'rb'), dialect='excel')

coordinate_list=[]
# loop through the csv by row skipping the first
iter = 0
for row in rawData:
    iter += 1
    if iter >= 2:
        lat = row[0]
        lon = row[1]
        coordinate_list.append("[" + lon + ", " + lat + "]")

final_string = '{"type":"Point","coordinates":['
final_string += ",".join(str(x) for x in coordinate_list)
final_string += "]}"
print final_string

# opens an geoJSON file to write the output to
outFileHandle = open('whole_foods' + '.geojson', 'w')
outFileHandle.write(final_string)
outFileHandle.close()
"""
print "complete!"
print "Time elapsed: " + str(time() - t) + " s."
