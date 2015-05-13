#-*- coding: UTF-8 -*- 
import sys

dataset = []
bestdata = []

def tran_time(old_time):
	new_time = old_time[0] + old_time[1] + old_time[2] + old_time[3] + '-' + old_time[4] + old_time[5] + '-' + old_time[6] + old_time[7] + ' '
	new_time += old_time[8] + old_time[9] + ':' + old_time[10] + old_time[11] + ':' + old_time[12] + old_time[13]
	return new_time

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
		self.toprint = line[0]
		for i in range(1, 6):
			self.toprint += ' ' + line[i]
		self.toprint += ' '
		self.toprint += tran_time(line[6])
		for i in range(7, 13):
			self.toprint += ' ' + line[i]
		#self.pack_name = line[13]
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
			dataset.append(item)

def examine(imeinum):
	for item in bestdata:
		if item[0] == imeinum:
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
	temp = []
	temp.append(str(0))
	temp.append(int(0))
	bestdata.append(temp)
count = 1
dataset[0].reporttime = tran_time(dataset[i].reporttime)
for i in range(1, len(dataset)):
	#dataset[i].reporttime = tran_time(dataset[i].reporttime)
	if dataset[i].imei == dataset[i-1].imei:
		count = count + 1
	else:
		if count > bestdata[0][1]:
			bestdata[0][0] = dataset[i-1].imei
			bestdata[0][1] = count
			bestdata.sort(lambda a, b:int(a[1]) - int(b[1]))
		count = 1
for item in bestdata:
	print item[0] + ' ' + str(item[1]) + '\n'
prefix = 'everyday_sort/yyb_everyday_data_sorted'
order = 0
total = 0
fout = open(prefix + str(order), 'w')
for item in dataset:
	fout.write(item.toprint)
	fout.write('\n')
	total += 1
	if examine(item.imei):
		bestdataset.append(item)
	if total >= 11000000:
		total = 0
		order += 1
		fout.close()
		fout = open(prefix + str(order), 'w')
fout.close()
prefix = 'everyday_most/yyb_everyday_data_best'
order = 0
fout = open(prefix + str(order), 'w')
lastitem = dataset[0]
lastitem.imei = 0
for item in bestdataset:
	if lastitem.imei != item.imei:
		fout.close()
		order += 1
		fout = open(prefix + str(order), 'w')
		lastitem.imei = item.imei
	fout.write(item.toprint)
	fout.write('\n')
fout.close()


