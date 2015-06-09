#-*- coding: UTF-8 -*- 
import sys
import time
from datetime import datetime

datadic = {}
delta = 300

def gettime(old_time):
	newyear = int(old_time[0] + old_time[1] + old_time[2] + old_time[3])
	newmonth = int(old_time[4] + old_time[5])
	newday = int(old_time[6] + old_time[7])
	newhour = int(old_time[8] + old_time[9])
	newmin = int(old_time[10] + old_time[11])
	newsec = int(old_time[12] + old_time[13])
	dt = datetime(year = newyear, month = newmonth, day = newday, hour = newhour, minute = newmin, second = newsec)
	return int(time.mktime(dt.timetuple()))

class Everyday:
	def __init__(self, line):

		self.flag = 0
		self.time = gettime(line[6])
		self.imei = line[0]
		self.appid = line[3]
		self.act_id = line[5]
		self.cur_scene = line[1]
		self.src_id = line[2]
		self.network = line[7]
		self.resolution = line[8]
		self.mod_id = line[9]

		self.toprint = gettime(line[6]) + ' ' + line[0] + ' ' + line[3] + ' ' + line[5] + ' '
		self.toprint += line[1] + ' ' + line[2] + ' ' + line[7] + ' ' line[8] + ' ' + line[9]

		#self.tag_id = line[14]
	def __cmp__(self, other):
		if self.imei < other.imei:
			return -1
		elif self.imei == other.imei:
			if self.reporttime < other.reporttime:
				return -1
			elif self.reporttime == other.reporttime:
				return 0
		return 1

def readdata(filegroup):
	for datafile in filegroup:
		fin = open(datafile, 'r')
		raw_data = fin.readlines()
		for temp in raw_data:
			data = temp.strip().split('	')
			item = Everyday(data)
			if datadic.has_key(item.imei):
				datadic[item.imei].append(item)
			else:
				datadic[item.imei] = []
				datadic[item.imei].append(item)

def examine(j, dataset):
	for i in range(j, -1, -1):
		if dataset[j].time - dataset[i].time > delta:
			return False
		if dataset[j].appid == dataset[i].appid:
			return True
	return False

def modnum(modstr):
	tmp = 1
	modlist = modstr.strip().split('_')
	#print modlist
	if modlist[0] == '' and len(modlist) == 1:
		return -1000
	modsum = 0
	for i in range(len(modlist) - 1, -1, -1):
		if modlist[i] == '':
			continue
		if not modlist[i].isdigit():
			continue
		modsum += tmp * int(modlist[i])
		tmp *= 1000
	return modsum

def mycmp(x, y):
	d = x.time - y.time
	if d < 0:
		return -1
	if d == 0:
		if int(x.cur_scene) < int(y.cur_scene):
			return -1
		if int(x.cur_scene) == int(y.cur_scene):
			if int(x.act_id) < int(y.act_id):
				return -1
			if int(x.act_id) == int(y.act_id):
				modx = modnum(x.mod_id)
				mody = modnum(x.mod_id)
				if modx < mody:
					return -1
				if modx == mody:
					return 0
	return 1

files = []
bestdataset = []

prefix = 'yyb_everyday_data_all_result_'
suffix = '_output'
for i in range(20150127, 20150132):
	filename = prefix + str(i) + suffix
	files.append(filename)
for i in range(20150201, 20150203):
	filename = prefix + str(i) + suffix
	files.append(filename)
readdata(files)
print 'Reading Data Finished...'
for itemset in datadic:
	datadic[itemset].sort(cmp = mycmp)
	for j in range(len(datadic[itemset])):
		if datadic[itemset][j].act_id == '900' and examine(j, datadic[itemset]):
			sd = j
			end = j + 1
			st = j
			if end < len(datadic[itemset]):
				while datadic[itemset][end].time == datadic[itemset][sd].time:
					datadic[itemset][end].flag = 1
					end += 1
					if end >= len(datadic[itemset]):
						break
			while datadic[itemset][sd].time - datadic[itemset][st].time <= delta:
				datadic[itemset][st].flag = 1
				if datadic[itemset][st].act_id == '900' and examine(j, datadic[itemset]):
					sd = st
				st -= 1
				if st < 0:
					break
	datadic[itemset] = list(reversed(datadic[itemset]))
print 'Finding Target Finished...'
count = 0
fout = open('timeline_total', 'w')
while len(datadic) > 0:
	earliest = 9999999999
	fg = 0
	tgkey = ''
	for itemset in datadic:
		if datadic[itemset][-1].time < earliest:
			fg = datadic[itemset][-1].flag
			earliest = datadic[itemset][-1].time
			tgkey = itemset
	if fg == 0:
		while datadic[tgkey][-1].time == earliest:
			fout.write('0 ' + datadic[tgkey].pop().toprint + '\n')
			if len(datadic[tgkey]) == 0:
				datadic.pop(tgkey)
				break
	else:
		count += 1
		while datadic[tgkey][-1].flag == 1:
			fout.write(str(count) + ' ' + datadic[tgkey].pop().toprint + '\n')
			if len(datadic[tgkey]) == 0:
				datadic.pop(tgkey)
				break
		if count % 1000 == 0:
			print 'Getting No.' + str(count) + ' Event Finished!'
fout.close()


