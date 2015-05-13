# -*- coding: utf8 -*-
from datetime import datetime

datestr1 = '2015-01-27'
datestr2 = '2015-01-28'
timestr1 = '23:59:04'
timestr2 = '00:03:33'
date1 = datestr1.strip().split('-')
date2 = datestr2.strip().split('-')
time1 = timestr1.strip().split(':')
time2 = timestr2.strip().split(':')
datetime1 = datetime(year = int(date1[0]), month = int(date1[1]), day = int(date1[2]), hour = int(time1[0]), minute = int(time1[1]), second = int(time1[2]))
datetime2 = datetime(year = int(date2[0]), month = int(date2[1]), day = int(date2[2]), hour = int(time2[0]), minute = int(time2[1]), second = int(time2[2]))
delta = datetime1 - datetime2
print delta
print delta.seconds
print delta.total_seconds()
if abs(delta.total_seconds()) > 300:
	print 'False'
else:
	print 'True'
