aislib
======

A Python library for decoding and encoding AIS type 1 messages

TODO
------

* Still need to implement the communication state bits. These bits are divided into three sections:
  * bits 1-2 is the "sync state"
  * bits 3-5 is the "slot time-out"
  * bits 6-19 is the "sub message"