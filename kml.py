from pykml import parser
from os import path
import urllib.request
#url = 'http://code.google.com/apis/kml/documentation/KML_Samples.kml'
#request = urllib.request.Request(url)
#fileobject = response = urllib.request.urlopen(request)
#root = parser.parse(fileobject).getroot()
mySearch = "GPS on vehicle"

kml_file = path.join('kmltest.xml')
with open(kml_file) as f:
    doc = parser.parse(f).getroot()

print(doc.Document.Placemark.name)
print(doc.Document.Style.IconStyle.heading)

for pm in doc.Document.Placemark:
    if(pm.name == mySearch):
        print("Found me")
        print(pm.Point.coordinates)
        posarray = pm.Point.coordinates
        print(posarray)
        print(type(posarray))
        posarray2 = posarray.text
        print(type(posarray2))
        posarray3 = posarray2.split(',')
        print(posarray3)
        poslong = posarray3[0]
        poslongfilter = poslong.replace('\n','')
        poslat = posarray3[1]
        poslatfilter = poslat.replace('\n','')
        longfloat = float(poslongfilter)
        latfloat = float(poslatfilter)
        print(longfloat)
        print(latfloat)
        print(type(longfloat))
        print(type(latfloat))
        int_lat_1 = int(latfloat)
        int_lat_1 = int_lat_1 * 60 * 100000
        int_lat_2 = latfloat - float((int(latfloat)))
        int_lat_2 = int_lat_2 * 60 * 10000
        #int_lat_2 = msg.latitude_minutes * 10000
        int_lat_3 = int_lat_2 + int_lat_1
        int_lat_4 = int(int_lat_3)
        print (latfloat)
        print (round(latfloat))
        print (int_lat_1)
        print (int_lat_2)
        print (int_lat_3)
        print (int_lat_4)

    #print(pm.name)

#import urllib.request
#url = "http://www.google.com/"
#request = urllib.request.Request(url)
#response = urllib.request.urlopen(request)
#print (response.read().decode('utf-8'))