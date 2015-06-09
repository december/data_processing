#-*- coding: UTF-8 -*- 
import sys

all_dic = {}
errorpair = []
erroruin = []

def readsource(filename):
	fin = open(filename, 'r')
	raw_data = fin.readlines()
	for temp in raw_data:
		data = temp.strip().split(' ')
		if all_dic.has_key(data[1]) and all_dic[data[1]] != data[0]:
			if erroruin.count(data[1]) == 0:
				erroruin.append(data[1])
				temppair = []
				temppair.append(data[1])
				temppair.append(all_dic[data[1]])
				errorpair.append(temppair)
			temppair = []
			temppair.append(data[1])
			temppair.append(data[0])
			errorpair.append(temppair)
		else:
			all_dic[data[1]] = data[0]
	fin.close()

def readsolution(filename):
	fin = open(filename, 'r')
	raw_data = fin.readlines()
	for temp in raw_data:
		data = temp.strip().split(' ')
		all_dic[data[0]] = data[1]
	fin.close()

readsource('yyb_sample_phone_info_output')
errorpair.sort(lambda a, b:int(a[0]) - int(b[0]))
fout = open('yyb_repeat_part', 'w')
for item in errorpair:
	fout.write(item[0] + ' ' + item[1] + '\n')
fout.close()
fout = open('yyb_multidevice_uin', 'w')
for item in erroruin:
	fout.write(item[0] + '\n')
fout.close()
