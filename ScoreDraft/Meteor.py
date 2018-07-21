from SingingGadgets.TrackBuffer import TrackBuffer
from SingingGadgets.TrackBuffer import MixTrackBufferList
from SingingGadgets.TrackBuffer import WriteTrackBufferToWav

from .Instrument import Instrument
from .Percussion import Percussion
from .Singer import Singer

from .PyMeteorGenerator import GenerateMeteor

import json
import math

EventType_Inst=0
EventType_Perc=1
EventType_Sing=2


class DummyTrackBuffer(TrackBuffer):
	def __init__ (self, eventList, chn=-1):
		TrackBuffer.__init__(self, chn)
		self.eventList=eventList

	def writeBlend(self, wavBuf):
		TrackBuffer.writeBlend(self,wavBuf)
		if 'event' in wavBuf:
			event = wavBuf['event']
			event['offset'] = self.getCursor()
			self.eventList += [event]

class DummyInstrumentEngine:
	def __init__(self, id, engine, isGMDrum):
		self.id=id
		self.engine = engine
		self.isGMDrum = isGMDrum

	def tune(self, cmd):
		return self.engine.tune(cmd)

	def generateWave(self, freq, fduration, sampleRate):
		wavBuf=self.engine.generateWave(freq, fduration, sampleRate)
		if not self.isGMDrum:
			event = {
				'type': EventType_Inst,
				'id': self.id,
				'freq': freq,
				'fduration': fduration
			}
		else:
			midiPitch = int(math.log(freq/261.626)*12.0 / math.log(2.0) + 0.5)  + 60;
			if midiPitch<0:
				midiPitch = 0
			elif midiPitch>127:
				midiPitch = 127
			event = {
				'type': EventType_Perc,
				'id': midiPitch,
				'fduration': fduration
			}

		wavBuf['event'] = event
		return wavBuf


class DummyInstrument(Instrument):
	def __init__(self, id, inst):
		Instrument.__init__(self)
		self.engine= DummyInstrumentEngine(id, inst.engine, inst.isGMDrum())


class DummyInstrumentCreator:
	def __init__(self):
		self.count=0
		self.map={}

	def Create(self, inst):
		if not inst in self.map:
			self.map[inst] = DummyInstrument(self.count, inst)
			self.count+=1
		return self.map[inst]

class DummyPercussionEngine:
	def __init__(self, id, engine):
		self.id=id
		self.engine=engine

	def tune(self, cmd):
		return self.engine.tune(cmd)

	def generateWave(self, fduration, sampleRate):
		wavBuf=self.engine.generateWave(fduration, sampleRate)
		event = {
			'type': EventType_Perc,
			'id': self.id + 128,
			'fduration': fduration
		}
		wavBuf['event'] = event
		return wavBuf

class DummyPercussion(Percussion):
	def __init__(self, id, perc):
		Percussion.__init__(self)
		self.engine= DummyPercussionEngine(id, perc.engine)	


class DummyPercussionCreator:
	def __init__(self):
		self.count=0
		self.map={}

	def Create(self, perc):
		if not perc in self.map:
			self.map[perc] = DummyPercussion(self.count, perc)
			self.count+=1
		return self.map[perc]

class DummySingerEngine:
	def __init__(self, id, engine):
		self.id=id
		self.engine=engine

	def tune(self, cmd):
		return self.engine.tune(cmd)

	def generateWave(self, syllableList, sampleRate):
		wavBuf=self.engine.generateWave(syllableList, sampleRate)
		event = {
			'type': EventType_Sing,
			'id': self.id,
			'syllableList': syllableList
		}
		wavBuf['event'] = event
		return wavBuf

class DummySinger(Singer):
	def __init__(self, id, singer):
		Singer.__init__(self)
		self.engine= DummySingerEngine(id, singer.engine)	


class DummySingerCreator:
	def __init__(self):
		self.count=0
		self.map={}

	def Create(self, singer):
		if not singer in self.map:
			self.map[singer] = DummySinger(self.count, singer)
			self.count+=1
		return self.map[singer]

class Document:
	def __init__ (self):
		self.bufferList=[]
		self.tempo=80
		self.refFreq=261.626
		self.eventList=[]
		self.instCreator=DummyInstrumentCreator()
		self.percCreator=DummyPercussionCreator()
		self.singerCreator=DummySingerCreator()

	def getBuffer(self, bufferIndex):
		return self.bufferList[bufferIndex]

	def getTempo(self):
		return self.tempo

	def setTempo(self,tempo):
		self.tempo=tempo

	def getReferenceFrequency(self):
		return self.refFreq

	def setReferenceFrequency(self,refFreq):
		self.refFreq=refFreq

	def newBuf(self, chn=-1):
		buf=DummyTrackBuffer(self.eventList,chn)
		self.bufferList.append(buf)
		return len(self.bufferList)-1

	def setTrackVolume(self, bufferIndex, volume):
		self.bufferList[bufferIndex].setVolume(volume)

	def setTrackPan(self, bufferIndex, pan):
		self.bufferList[bufferIndex].setPan(pan)

	def playNoteSeq(self, seq, instrument, bufferIndex=-1):
		dummyInst = self.instCreator.Create(instrument)
		if bufferIndex==-1:
			bufferIndex= self.newBuf()		
		buf=self.bufferList[bufferIndex]
		dummyInst.play(buf, seq, self.tempo, self.refFreq)
		return bufferIndex	

	def playBeatSeq(self, seq, percList, bufferIndex=-1):
		dummyPercList =[self.percCreator.Create(perc) for perc in percList]
		if bufferIndex==-1:
			bufferIndex= self.newBuf()		
		buf=self.bufferList[bufferIndex]			
		Percussion.play(dummyPercList, buf, seq, self.tempo)
		return bufferIndex

	def sing(self, seq, singer, bufferIndex=-1):
		dummySinger = self.singerCreator.Create(singer)
		if bufferIndex==-1:
			bufferIndex= self.newBuf()		
		buf=self.bufferList[bufferIndex]
		dummySinger.sing( buf, seq, self.tempo, self.refFreq)
		return bufferIndex

	def trackToWav(self, bufferIndex, filename):
		WriteTrackBufferToWav(self.bufferList[bufferIndex], filename)

	def mix(self, targetBuf):
		MixTrackBufferList(targetBuf,self.bufferList)

	def mixDown(self,filename,chn=-1):
		targetBuf=TrackBuffer(chn)
		self.mix(targetBuf)
		WriteTrackBufferToWav(targetBuf, filename)

	def saveToFile(self,filename):
		GenerateMeteor(self.eventList, filename)

	def saveToFile_json(self, filename):
		with open(filename,'w') as f:
			json.dump(self.eventList, f)

