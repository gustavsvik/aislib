# Echo server program
import socket
import time
import sys
import os
import pynmea2
import aislib
import signal

#filepath = sys.argv[1]
timestamp = 0

aismsg = aislib.AISPositionReportMessage(
    mmsi = 237772000,
    status = 8,
    sog = 75,
    pa = 1,
    lon = (25*60+00)*10000,
    lat = (35*60+30)*10000,
    cog = 2800,
    ts = 40,
    raim = 1,
    comm_state = 82419   
)

#if not os.path.isfile(filepath):
#  print("File path {} does not exist. Exiting...".format(filepath))
#  sys.exit()

#def signal_handler(sig, frame):
#    print('You pressed Ctrl+C!')
#    sys.exit()

#signal.signal(signal.SIGINT, signal_handler)
#s.socket(socket.AF_INET, socket.SOCK_STREAM)
#p.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = ''                 # Symbolic name meaning the local host
PORT = 50008             # Arbitrary non-privileged port

HOST_RECV = '127.0.0.1'
PORT_RECV = 2000

while 1:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print 'Connected by', addr
        while 1:
            print 'Connect to source'
            try:
                p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                p.connect((HOST_RECV, PORT_RECV))
            except:
                print "Error in connect to source"
                sys.exit()
                #continue

            print 'Connected to source'
            while 1:
                data = p.recv(2048)
                data = data.splitlines(True)
                for i in data:
                    try:
                        msg = pynmea2.parse(i)
                    except:
                        print "Error in decoding!"
                        print i
                        continue  
                    if type(msg) is pynmea2.types.talker.GLL:
                        print("Found GLL")
                        int_lat_1 = int(round(msg.latitude))
                        int_lat_1 = int_lat_1 * 60 *10000
                        int_lat_2 = msg.latitude_minutes * 10000
                        int_lat_3 = int_lat_2 + int_lat_1
                        print int(int_lat_3)
                        int_lon_1 = int(round(msg.longitude))
                        int_lon_1 = int_lon_1 * 60 *10000
                        int_lon_2 = msg.longitude_minutes * 10000
                        int_lon_3 = int_lon_2 + int_lon_1
                        print int(int_lon_3)
                        timestamp = timestamp + 1
                        if timestamp > 59:
                            timestamp = 0
                        aismsg.ts = timestamp
                        aismsg.lat = int(int_lat_3)
                        aismsg.lon = int(int_lon_3)
                        ais = aislib.AIS(aismsg)
                        payload = ais.build_payload(False)
                        conn.send(payload)
                        conn.send('\n\r')
                    if type(msg) is pynmea2.types.talker.GGA:
                        print("Found GGA")
                        int_lat_1 = int(round(msg.latitude))
                        int_lat_1 = int_lat_1 * 60 *10000
                        int_lat_2 = msg.latitude_minutes * 10000
                        int_lat_3 = int_lat_2 + int_lat_1
                        print int(int_lat_3)
                        int_lon_1 = int(round(msg.longitude))
                        int_lon_1 = int_lon_1 * 60 *10000
                        int_lon_2 = msg.longitude_minutes * 10000
                        int_lon_3 = int_lon_2 + int_lon_1
                        print int(int_lon_3)
                        timestamp = timestamp + 1
                        if timestamp > 59:
                            timestamp = 0
                        aismsg.ts = timestamp
                        aismsg.lat = int(int_lat_3)
                        aismsg.lon = int(int_lon_3)
                        ais = aislib.AIS(aismsg)
                        payload = ais.build_payload(False)
                        conn.send(payload)
                        conn.send('\n\r')
                    if type(msg) is pynmea2.types.talker.HDT:
                        print("Found HDT")
                        print msg.heading
                        #aismsg.cog = int(msg.heading*10)
                    if type(msg) is pynmea2.types.talker.VTG:
                        print("Found VTG")
                        print msg.spd_over_grnd_kts
                        print msg.true_track
                        aismsg.sog = int(msg.spd_over_grnd_kts*10)
                        aismsg.cog = int(msg.true_track*10)
                    time.sleep(0.05)
    except KeyboardInterrupt:
        print("Got ctrl+c, exit... bye!")
        conn.close()
        p.close()
        s.close()
        sys.exit()
    except:
        print("Session closed, restart server")
        conn.close()
        p.close()
        s.close()
        continue
        #sys.exit()
    conn.close()