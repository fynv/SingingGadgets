import math
import SingingGadgets as sg
from .InstrumentBase import InstrumentBase

SF2s={}

def GetSF2(fn):
	if not (fn in SF2s):
		sf2_file = sg.LoadSF2(fn)
		sf2_presets =  sg.LoadPresetsSF2(sf2_file)
		SF2s[fn] = (sf2_presets, sf2_file[1])
	return SF2s[fn]

def ListPresets(fn):
	sf2 = GetSF2(fn)
	sf2_presets = sf2[0]
	for i in range(len(sf2_presets)):
		preset = sf2_presets[i]
		print ('%d : %s bank=%d number=%d' % (i, preset['presetName'], preset['bank'], preset['preset']))

class Engine:
	def __init__(self, preset, fontSamples, sampleRate, global_gain_db):
		self.preset = preset
		self.fontSamples = fontSamples
		self.sampleRate = sampleRate
		self.global_gain_db = global_gain_db
		self.vel = 1.0

	def tune(self, cmd):
		cmd_split= cmd.split(' ')
		cmd_len=len(cmd_split)
		if cmd_len>=1:
			if cmd_len>1 and cmd_split[0]=='velocity':
				self.vel = float(cmd_split[1])
				return True
		return False

	def generateWave(self, freq, fduration):
		key = math.log(freq / 261.626)/math.log(2)*12.0+60.0
		num_samples = fduration * self.sampleRate * 0.001
		(actual_num_samples, F32Samples) = sg.SynthNoteSF2(self.fontSamples, self.preset, key, self.vel, num_samples, outputmode = sg.STEREO_INTERLEAVED, samplerate = self.sampleRate, global_gain_db = self.global_gain_db)
		return {
			'sample_rate': self.sampleRate,
			'num_channels': 2,
			'data': F32Samples,
			'align_pos': 0
		}		


class SF2Instrument(InstrumentBase):
	def __init__(self, fn, preset_index, sampleRate=44100, global_gain_db=0.0):
		InstrumentBase.__init__(self)
		sf2 = GetSF2(fn)
		self.engine= Engine(sf2[0][preset_index], sf2[1], sampleRate, global_gain_db)

