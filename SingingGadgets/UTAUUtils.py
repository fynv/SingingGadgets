# from .PyUTAUUtils import *

import struct

def LoadFrq(filename):
	with open(filename, 'rb') as f:
		f.seek(8,0)
		interval= struct.unpack('i',f.read(4))[0]
		f.seek(12,0)
		key = struct.unpack('d', f.read(8))[0]
		f.seek(36,0)
		count = struct.unpack('i', f.read(4))[0]
		f.seek(40,0)
		data=[]
		for i in range(count):
			(freq, dyn) = struct.unpack('dd', f.read(16))
			data+=[(freq,dyn)]
		return {
			"interval": interval,
			"key": key,
			"data": data
		}

class OtoMap:
	def __init__(self):
		self.oto_map={}

	def AddOtoINIPath(self,path):
		otoIniPath=path+'/oto.ini'
		with open(otoIniPath,'r', encoding='mbcs') as f:
			while True:
				line = f.readline()
				if not line:
					break
				p = line.find('=')
				if p==-1:
					continue
				fn=line[0:p]

				p+=1

				# lyric
				lyric=''
				p2 = line.find(',',p)
				if p2==-1:
					continue
				if p2>p:
					lyric=line[p:p2]
				p=p2+1

				if len(lyric)==0:
					lyric = fn[0:len(fn)-4]

				# offset
				offset=0
				p2 = line.find(',',p)
				if p2==-1:
					continue
				if p2>p:
					offset=float(line[p:p2])
				p=p2+1

				# consonant
				consonant = 0
				p2 = line.find(',',p)
				if p2==-1:
					continue
				if p2>p:
					consonant=float(line[p:p2])
				p=p2+1

				# cutoff
				cutoff = 0
				p2 = line.find(',',p)
				if p2==-1:
					continue
				if p2>p:
					cutoff=float(line[p:p2])
				p=p2+1

				# preutter
				preutterance = 0
				p2 = line.find(',',p)
				if p2==-1:
					continue
				if p2>p:
					preutterance=float(line[p:p2])
				p=p2+1

				# overlap
				overlap = float(line[p:])

				properties={
					'filename': path+'/'+fn,
					'offset': offset,
					'consonant': consonant,
					'cutoff': cutoff,
					'preutterance': preutterance,
					'overlap': overlap
				}

				self.oto_map[lyric]=properties

