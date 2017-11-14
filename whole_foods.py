import pandas as pd
import csv
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

#possible hub locations
#hub_location = ['santa_monica', 34.021944, -118.481389]
#hub_location = ['dublin', 37.70577, -121.88984]
#hub_location = ['long_beach', 33.768333, -118.195556]
hub_location = ['pasadena', 34.156111, -118.131944]

# write hub centroid to csv
with open(hub_location[0] + '_hub.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['hub_id', 'lat', 'lon'])
    wr.writerow(hub_location)


#build the url
url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
url += str(hub_location[1]) + ',' + str(hub_location[2])
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
    store_list.append([hub_location[0], name, address, lat, lon])

print store_list

# write spokes to csv
df = pd.DataFrame(store_list)
df.columns = ['hub_id', 'name', 'address', 'lat', 'lon']
print df
df.to_csv(hub_location[0] + '_spokes.csv', index=False)

print "complete!"
print "Time elapsed: " + str(time() - t) + " s."
