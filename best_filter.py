#-*- coding: UTF-8 -*- 
import sys
from datetime import datetime

#2015-01-27 
#	01:01:01 DOWNLOAD XXX (version) in XXX from XXX under 3G (mod = )

maxdelta = 300

dataset = []
actset = []
act_dic = {'100':'EXPOSE', '200':'TICK', '900':'DOWNLOAD', '905':'UPDATEIT', '305':'SETUP', '500':'OPEN'}
scene_dic = {'2008':'详情页', '200807':'标签详情页', '200802':'详情页评论', '2023':'开发者其他应用详情', \
			'201001':'更新管理', '2039':'猜你喜欢', '204101':'飙升榜', '204102':'经典榜', \
			'204103':'个性榜', '204104':'好友榜', '200501':'软件首页', '20050304':'分类页子标签页', \
			'200503':'分类首页', '200502':'软件排行', '200601':'游戏首页', '200603':'游戏分类页', \
			'20060301':'游戏分类详情', '200602':'游戏排行', '201002':'下载管理', '202912':'身边的人在玩', \
			'202907':'好友圈流行', '202913':'用户属性维度', '202914':'应用标签', '2001':'发现首页', \
			'2002':'首页－必备', '2003':'首页－最热', '200504':'软件－专题', '200505':'软件－小红花', '200506':'软件－腾讯'}

class Everyday:
	def __init__(self, line):
		self.imei = line[0]
		self.cur_scene = line[1]
		self.src_scene = line[2]
		self.appid = line[3]
		self.app_version = line[4]
		self.act_id = line[5]
		self.date = line[6]
		self.time = line[7]
		self.network = line[8]
		self.resolution = line[9]
		self.mod_id = line[10]
		self.track_id = line[11]
		self.type = line[12]
		self.mf = line[13]
		self.toprint = '    ' + line[7] + ' '
		temp = line[5]
		if act_dic.has_key(line[5]):
			temp = act_dic[line[5]]
		self.toprint += temp + ' ' + line[3]
		if self.app_version != '':
			self.toprint += '(' + line[4] + ')'
		scene1 = line[1]
		scene2 = line[2]
		if scene_dic.has_key(line[1]):
			scene1 = scene_dic[line[1]]
		if scene_dic.has_key(line[2]):
			scene2 = scene_dic[line[2]]
		self.toprint += ' in ' + scene1 + ' from ' + scene2 + ' under ' + line[8]
		if line[10] != '-1':
			self.toprint += ' (mod=' + line[10] + ')'
		if int(line[12]) == 1:
			self.toprint += ' BY AUTO'
		if int(line[12]) == 2:
			self.toprint += ' BY PLUGIN'

def readdata(filename):
	fin = open(filename, 'r')
	raw_data = fin.readlines()
	for temp in raw_data:
		data = temp.strip().split(' ')
		item = Everyday(data)
		dataset.append(item)

def examine(datestr1, datestr2, timestr1, timestr2):
	date1 = datestr1.strip().split('-')
	date2 = datestr2.strip().split('-')
	time1 = timestr1.strip().split(':')
	time2 = timestr2.strip().split(':')
	datetime1 = datetime(year = int(date1[0]), month = int(date1[1]), day = int(date1[2]), hour = int(time1[0]), minute = int(time1[1]), second = int(time1[2]))
	datetime2 = datetime(year = int(date2[0]), month = int(date2[1]), day = int(date2[2]), hour = int(time2[0]), minute = int(time2[1]), second = int(time2[2]))
	delta = datetime1 - datetime2
	if abs(delta.total_seconds()) > maxdelta:
		return False
	else:
		return True

prefix = 'yyb_everyday_data_best'
for i in range(1, 11):
	dataset = []
	actset = []
	count = 0
	readdata(prefix + str(i))
	rp = dataset[0]
	fout = open('act_best' + str(i), 'w')
	fout.write(rp.imei + ' ' + rp.mf + ' ' + rp.resolution + '\n')
	for j in range(len(dataset)):
		if j == 0 or dataset[j].date != dataset[j-1].date:
			fout.write('\n' + dataset[j].date + '\n')
		if dataset[j].act_id == '900':
			#actset.append(dataset[j].toprint)
			for k in range(j, -1, -1):
				if examine(dataset[j].date, dataset[k].date, dataset[j].time, dataset[k].time):
					actset.append(dataset[k].toprint)
				else:
					break
			count += 1
			fout.write('	#' + str(count) + '\n')
			while len(actset):
				fout.write(actset.pop() + '\n')
	fout.close()
