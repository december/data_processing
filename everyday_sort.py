#-*- coding: UTF-8 -*- 
import sys

dataset = []
bestdata = []

class Everyday:
	def __init__(self, line):
		self.imei = line[0]
		self.cur_scene = line[1]
		self.src_id = line[2]
		self.appid = line[3]
		self.app_version = line[4]
		self.act_id = line[5]
		self.reporttime = line[6]  # to be transferred
		self.network = line[7]
		self.resolution = line[8]
		self.mod_id = line[9]
		self.track_id = line[10]
		self.type = line[11]
		self.mf = line[12]
		self.pack_name = line[13]
		self.tag_id = line[14]
	def __cmp__(self, other):
		if self.imei < other.imei:
			return -1
		elif self.imei == other.imei:
			if self.reporttime < other.reporttime:
				return -1
			elif self.reporttime == other.reporttime:
				return 0
		return 1

def tran_time(old_time):
	new_time = old_time[0] + old_time[1] + '-' + old_time[2] + old_time[3] + '-' old_time[4] + old_time[5] + ' '
	new_time += old_time[6] + old_time[7] + ':' + old_time[8] + old_time[9] + ':' old_time[10] + old_time[11]
	return new_time

def readdata(filegroup):
	for datafile in filegroup:
		fin = open(datafile, 'r')
		raw_data = fin.readlines()
		for temp in raw_data:
			data = temp.strip().split('\t')
			item = Everyday(data)
			dataset.append(item)

def examine(imeinum):
	for item in bestdata:
		if item.imei == imeinum:
			return True
	return False

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
dataset.sort()
for i in range(0, 10):
	temp.append(str(0))
	temp.append(int(0))
	bestdata.append(temp)
count = 1
dataset[0].reporttime = tran_time(dataset[i].reporttime)
for i in range(1, len(dataset)):
	dataset[i].reporttime = tran_time(dataset[i].reporttime)
	if dataset[i].imei == dataset[i-1].imei:
		count = count + 1
	else:
		if count > bestdata[0][1]:
			bestdata[0][0] = dataset[i-1].imei
			bestdata[0][1] = count
			bestdata.sort(lambda a, b:int(a[1]) - int(b[1]))
		count = 1
for item in bestdata:
	print item[0] + ' ' + item[1] + '\n'
fout = open('yyb_everyday_data_sorted', 'w')
for item in dataset:
	fout.write(item)
	fout.write('\n')
	if examine(item.imei):
		bestdataset.append(item)
fout.close()
fout = open('yyb_everyday_data_best', 'w')
for item in bestdataset:
	fout.write(item)
	fout.write('\n')
fout.close()


