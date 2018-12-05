Title: DVBT2MPG : No DVB-T drive
Date: 2009-09-21 14:02
Author: Dominique
Tags: Logiciels de Papa, DVBT2MPG
Slug: dvbt2mpgf-pas-de-disque-dvb-t-trouve
Lang: en

I got many emails concerning detection problems on SAGEM PVR disks with
DVBT2MPG. Following a PC disk crash, I lost all my emails. So I can’t
answer to everybody. Sorry for that.  

By analyzing the .log files I received, I discovered that SAGEM changed
from a “Big Endian” processor to a “Little Endian” one in its PVR. The
new version of DVBT2MPG (V1R2.3) automatically detects byte order.
However I have no hardware to test it! So if somebody with this problem
can test it for me and give me the result, it will be fine.  

Remark concerning Vista: In order to allow access to disk sectors, you
must change the properties of the DVBT2MPG.EXE file. It must execute as
“Administrator” (it is the same under Windows 7).


