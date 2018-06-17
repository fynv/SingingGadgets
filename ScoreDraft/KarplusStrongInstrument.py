import SingingGadgets as sg
from .Instrument import Instrument
from .Catalog import Catalog
Catalog['Engines'] += ['KarplusStrongInstrument - Instrument']

class Engine:
	def __init__(self):
		self.cut_freq=10000.0
		self.loop_gain=0.99
		self.sustain_gain=0.8
	def tune(self, cmd):
		pass
	def generateWave(self, freq, fduration, sampleRate):
		return sg.KarplusStrongGenerate(freq,fduration,sampleRate,self.cut_freq, self.loop_gain, self.sustain_gain)

class KarplusStrongInstrument(Instrument):
	def __init__(self):
		Instrument.__init__(self)
		self.engine = Engine()
	def setCutFrequency(self, cut_freq):
		# This is the cut-frequency of the feedback filter for pitch 261.626Hz
		self.engine.cut_freq = cut_freq
	def setLoopGain(self, loop_gain):
		self.engine.loop_gain = loop_gain
	def setSustainGain(self, sustain_gain):
		self.engine.sustain_gain = sustain_gain

