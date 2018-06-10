import wave
import SingingGadgets as sg
from .Percussion import Percussion
from .Catalog import Catalog

Catalog['Engines'] += ['PercussionSampler - Percussion']

class Engine:
	def __init__(self, sample):
		self.sample=sample		
	def tune(self, cmd):
		pass
	def generateWave(self, fduration, sampleRate):
		return sg.PercussionSample(self.sample, fduration, sampleRate)

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

	return {
		'nframes' : nFrames,
		'nchannels' : nChn,
		'frames': sg.S16ToF32(wavS16),
		'framerate': framerate
		}

Samples = {}

def GetSample(fn):
	if not (fn in Samples):
		Samples[fn] = loadWav(fn)
	return Samples[fn]

class PercussionSampler(Percussion):
	def __init__(self, wavPath):
		Percussion.__init__(self)
		sample = GetSample(wavPath)
		self.engine = Engine(sample)

