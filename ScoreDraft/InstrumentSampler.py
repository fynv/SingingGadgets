import os
import wave
import SingingGadgets as sg
from .Instrument import Instrument
from .Catalog import Catalog
Catalog['Engines'] += ['InstrumentSampler_Single - Instrument']
Catalog['Engines'] += ['InstrumentSampler_Multi - Instrument']

class Engine_Single:
	def __init__(self, sample):
		self.sample=sample		
	def tune(self, cmd):
		pass
	def generateWave(self, freq, fduration, sampleRate):
		return sg.InstrumentSingleSample(self.sample, freq, fduration, sampleRate)

class Engine_Multi:
	def __init__(self, samples):
		self.samples=samples	
	def tune(self, cmd):
		pass
	def generateWave(self, freq, fduration, sampleRate):
		return sg.InstrumentMultiSample(self.samples, freq, fduration, sampleRate)

def loadWav(file):
	wavS16=bytes()
	nChn = 1
	nFrames = 0
	framerate = 44100
	with wave.open(file, mode='rb') as wavFile:
		nFrames =wavFile.getnframes() 
		nChn = wavFile.getnchannels()
		wavS16=wavFile.readframes(nFrames)
		framerate = wavFile.getframerate()

	sample= {
		'nframes' : nFrames,
		'nchannels' : nChn,
		'frames': sg.S16ToF32(wavS16),
		'framerate': framerate
		}

	basefreq = 0
	freq_fn = file[0:len(file)-4]+".freq"
	if os.path.isfile(freq_fn):
		with open(freq_fn, "r") as f:
			basefreq= float(f.readline())
			sample['basefreq']=basefreq

	if basefreq == 0:
		sg.DetectBaseFreq(sample)
		basefreq = sample['basefreq']
		with open(file[0:len(file)-4]+".freq", "w") as f:
			f.write(str(basefreq))
		
	return sample

Samples_Single = {}

def GetSample_Single(fn):
	if not (fn in Samples_Single):
		Samples_Single[fn] = loadWav(fn)
	return Samples_Single[fn]

Samples_Multi = {}

def GetSamples_Multi(path):
	if not (path in Samples_Multi):
		samples = []
		if os.path.isdir(path):
			for item in os.listdir(path):
				fn = path+'/'+item
				if os.path.isfile(fn) and item.endswith(".wav"):
					samples+=[loadWav(fn)]
		Samples_Multi[path] = samples
	return Samples_Multi[path]

class InstrumentSampler_Single(Instrument):
	def __init__(self, wavPath):
		Instrument.__init__(self)
		sample = GetSample_Single(wavPath)
		self.engine = Engine_Single(sample)

class InstrumentSampler_Multi(Instrument):
	def __init__(self, folderPath):
		Instrument.__init__(self)
		samples = GetSamples_Multi(folderPath)
		self.engine = Engine_Multi(samples)
