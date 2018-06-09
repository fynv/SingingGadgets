import math
import SingingGadgets as sg
from .Instrument import Instrument

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
	def __init__(self, preset, fontSamples):
		self.preset = preset
		self.fontSamples = fontSamples
		self.global_gain_db = 0.0
		self.vel = 1.0

	def tune(self, cmd):
		cmd_split= cmd.split(' ')
		cmd_len=len(cmd_split)
		if cmd_len>=1:
			if cmd_len>1 and cmd_split[0]=='velocity':
				self.vel = float(cmd_split[1])
				return True
		return False

	def generateWave(self, freq, fduration, sampleRate):
		key = math.log(freq / 261.626)/math.log(2)*12.0+60.0
		num_samples = fduration * sampleRate * 0.001
		(actual_num_samples, F32Samples) = sg.SynthNoteSF2(self.fontSamples, self.preset, key, self.vel, num_samples, sg.STEREO_INTERLEAVED, sampleRate, self.global_gain_db)
		return {
			'sample_rate': sampleRate,
			'num_channels': 2,
			'data': F32Samples,
			'align_pos': 0
		}		


class SF2Instrument(Instrument):
	def __init__(self, fn, preset_index):
		Instrument.__init__(self)
		sf2 = GetSF2(fn)
		self.engine= Engine(sf2[0][preset_index], sf2[1])

