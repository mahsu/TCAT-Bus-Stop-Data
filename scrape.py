from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse, parse_qsl

class Stop:

	def __init__(self, name, stopid, area, zone, addl, lat, lon):
		self.name = name
		self.id = stopid
		self.area = area
		self.zone  = zone
		self.addl = addl
		self.lat = lat
		self.lon = lon

	def toCSV(self):
		self.name = '"' + self.name.replace('"','""') + '"' #wrap in quotes and escape '"''
		self.addl = '"' + self.addl.replace('"','""') + '"'
		return("{},{},{},{},{},{},{}\n".format(self.id,self.name,self.zone,self.lat,self.lon,self.area,self.addl))

#-------------------------------------------------
stops = [] #container for stop objects
BASE_URL = "http://tcat.nextinsight.com"
urlcontents = urlopen(BASE_URL+"/allstops.php")
allstops = BeautifulSoup(urlcontents)

links = allstops.find(id="page").find("p").find_all("a")

print("Found {} stops. Starting data collection.".format(len(links)))
for link in links:
	#extract useful info from the link
	stopurl = link.get("href")
	print("Collecting data in: " + stopurl)

	name = link.get_text()
	
	#visit the stop link
	urlcontents = urlopen(BASE_URL + stopurl)
	stop = BeautifulSoup(urlcontents)
	area = stop.find("h4",text="Area").find_next_sibling().get_text()
	zone = stop.find("h4", text="Fare Zone").find_next_sibling().get_text()
	zone = zone.replace("Zone ","") #strip Zone prefix
	addl = stop.find("h4", text="Additional Information").find_next_sibling().get_text()
	addl = addl.replace("\n","") #strip newlines
	mapurl = stop.find("a", text="View Stop On Map").get("href") #?lat=42.393639&lon=-76.362834&stopid=9368
	mapquery = parse_qsl(urlparse(mapurl).query)
	
	#[('lat', '42.458150'), ('lon', '-76.475667'), ('stopid', '3660')]
	lat = mapquery[0][1]
	lon = mapquery[1][1]
	stopid = mapquery[2][1]

	#create the stop object
	stops.append(Stop(name, stopid, area, zone, addl, lat, lon))

print("Data collection finished.\nCollected {} stops.\nBegin writing to file.".format(len(stops)))


f = open('TCATstops.csv', 'w')
f.write("id,name,zone,lat,lon,area,addl\n")

#iterate through stop objects
for stop in stops:
	f.write(stop.toCSV())

f.close()
print("Completed")




