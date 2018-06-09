import SingingGadgets as sg
from .Instrument import Instrument

class Engine:
	def __init__(self, generator):
		self.generator= generator
	def tune(self, cmd):
		pass
	def generateWave(self, freq, fduration, sampleRate):
		return self.generator(freq, fduration, sampleRate)

class PureSin(Instrument):
	def __init__(self):
		Instrument.__init__(self)
		self.engine = Engine(sg.GeneratePureSin)

class Square(Instrument):
	def __init__(self):
		Instrument.__init__(self)
		self.engine = Engine(sg.GenerateSquare)

class Triangle(Instrument):
	def __init__(self):
		Instrument.__init__(self)
		self.engine = Engine(sg.GenerateTriangle)

class Sawtooth(Instrument):
	def __init__(self):
		Instrument.__init__(self)
		self.engine = Engine(sg.GenerateSawtooth)

class NaivePiano(Instrument):
	def __init__(self):
		Instrument.__init__(self)
		self.engine = Engine(sg.GenerateNaivePiano)

class BottleBlow(Instrument):
	def __init__(self):
		Instrument.__init__(self)
		self.engine = Engine(sg.GenerateBottleBlow)

