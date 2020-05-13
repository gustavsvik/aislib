import socket
import time
import sys
import os
import aislib
import signal
from pykml import parser
from os import path
import urllib2

url = 'http://localhost/rov.kml'

timestamp = 0

aismsg = aislib.AISPositionReportMessage(
    mmsi = 237772000,
    status = 8,
    sog = 1,
    pa = 1,
    lon = (25*60+00)*10000,
    lat = (35*60+30)*10000,
    cog = 0,
    ts = 40,
    raim = 1,
    comm_state = 82419   
)

mySearch = "GPS on vehicle"

HOST = ''                 # Symbolic name meaning the local host
PORT = 50012            # Arbitrary non-privileged port

while 1:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print ('Connected by', addr)
        while 1:
            #Read from file
            fileobject = urllib2.urlopen(url)
            doc = parser.parse(fileobject).getroot()
            #kml_file = path.join('kmltest.xml')
            #with open(kml_file) as f:
                #doc = parser.parse(f).getroot()
                #fileobject = urllib2.urlopen(url)
                #doc = parser.parse(fileobject).getroot()
            for pm in doc.Document.Placemark:
                if(pm.name == mySearch):
                    posarray = pm.Point.coordinates.text
                    posarray2 = posarray.split(',')
                    poslong = posarray2[0]
                    poslongfilter = poslong.replace('\n','')
                    poslat = posarray2[1]
                    poslatfilter = poslat.replace('\n','')
                    longfloat = float(poslongfilter)
                    latfloat = float(poslatfilter)
                    timestamp = timestamp + 1
                    if timestamp > 59:
                        timestamp = 0
                    aismsg.ts = timestamp
                    int_lat_1 = int(latfloat)
                    int_lat_1 = int_lat_1 * 60 * 10000
                    int_lat_2 = latfloat - float((int(latfloat)))
                    int_lat_2 = int_lat_2 * 60 * 10000
                    int_lat_3 = int_lat_2 + int_lat_1
                    aismsg.lat = int(int_lat_3)
                    int_long_1 = int(longfloat)
                    int_long_1 = int_long_1 * 60 * 10000
                    int_long_2 = longfloat - float((int(longfloat)))
                    int_long_2 = int_long_2 * 60 * 10000
                    int_long_3 = int_long_2 + int_long_1
                    aismsg.lon = int(int_long_3)
                    heading = float(doc.Document.Style.IconStyle.heading.text)
                    heading = heading * 10
                    aismsg.cog = int(heading)
                    ais = aislib.AIS(aismsg)
                    payload = ais.build_payload(False)
                    conn.send(payload)
                    conn.send('\n\r')
            time.sleep(1)
    except KeyboardInterrupt:
        print("Got ctrl+c, exit... bye!")
        #conn.close()
        #p.close()
        s.close()
        sys.exit()
    except:
        print("Session closed, restart server")
        #conn.close()
        #p.close()
        s.close()
        continue
     #   sys.exit()