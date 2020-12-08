aislib
======

A Python library for decoding and encoding: 
 * AIS type 1 messages
 * AIS type 5 messages
 * AIS type 21 messages
 * AIS type 24 part A and Part B messages (main craft case )
 
As there exist reliable and comprehensive python decoders, the emphasis is on encoding.

It is easy but boring to add further messages types, I will do it only if the need arises.
To do it you need to read carefully the documentation, the best source I have found is http://catb.org/gpsd/AIVDM.html

The bitstring Python library is a required dependency. You can get it here: https://pypi.python.org/pypi/bitstring

TODO
------

* Still need to implement the communication state bits. These bits are divided into three sections:
  * bits 1-2 is the "sync state"
  * bits 3-5 is the "slot time-out"
  * bits 6-19 is the "sub message"

# nmea-server.py
Will need pynmea2 and bitstring to be able to work.

The problem is that this aislib needs python2 to be able to run.
So we need to install pynmea2 and bitstring by manual in ubuntu to make it work.

pip will direct to python3 as default.
