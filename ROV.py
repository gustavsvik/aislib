import socket
import time
import aislib
import pynmea2
import sys
import os
import signal

#
# Tests for Message Type 1
#
#aismsg = aislib.AISPositionReportMessage(
#    mmsi = 237772000,
#    status = 8,
#    sog = 75,
#    pa = 1,
#    lon = (25*60+00)*10000,
#    lat = (35*60+30)*10000,
#    cog = 2800,
#    ts = 40,
#    raim = 1,
#    comm_state = 82419   
#)
#ais = aislib.AIS(aismsg)
#payload = ais.build_payload(False)
#print (payload)
#print ("nav status 1: %d" % aismsg.get_attr("status"))

filepath = sys.argv[1]

if not os.path.isfile(filepath):
  print("File path {} does not exist. Exiting...".format(filepath))
  sys.exit()

HOST = ''                 # Symbolic name meaning the local host
PORT = 50005             # Arbitrary non-privileged port

while 1:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print 'Connected by', addr
        with open(filepath) as fp:
            for line in fp:
                conn.send(line)
                #conn.send('\n')
                msg = pynmea2.parse(line)
                #print(type(msg))
                if type(msg) is pynmea2.types.talker.HDT:
                    print("Found HDT")
                if type(msg) is pynmea2.types.talker.VTG:
                    print("Found VTG")
                if type(msg) is pynmea2.types.talker.GLL:
                    print("Found GLL")
                    time.sleep(1)           #If we got GLL wait for 1 second before send again
                if type(msg) is pynmea2.types.talker.GSA:
                    print("Found GSA")
    except KeyboardInterrupt:
        print("Got ctrl+c, exit... bye!")
        conn.close()
        sys.exit()
    except:
        print("Session closed, restart server")
        conn.close()
        continue
    conn.close()

#aismsg2 = ais.decode(payload)
#ais2 = aislib.AIS(aismsg2)
#payload2 = ais2.build_payload(False)
#assert payload ==  payload2
#print ("nav status 2: %d" % aismsg2.get_attr("status"))