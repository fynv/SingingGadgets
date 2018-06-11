import math
from .PyWavUtils import MixF32
from .PySF2Synth import SynthRegion

# Output Modes
# Two channels with single left/right samples one after another
STEREO_INTERLEAVED = 0
# Two channels with all samples for the left channel first then right
STEREO_UNWEAVED = 1
# A single channel (stereo instruments are mixed into center)
MONO = 2


def SynthNote(inputSamples, preset, key, vel, numSamples, outputmode = STEREO_INTERLEAVED, samplerate = 44100.0, global_gain_db = 0.0):
	ikey=int(key+0.5)
	midiVelocity = int(vel*127)
	bufs = []

	chn = 2
	if outputmode == MONO:
		chn =1

	max_numSamples = 0
	for region in preset['regions']:
		if ikey < region['lokey'] or ikey > region['hikey'] or midiVelocity < region['lovel'] or midiVelocity > region['hivel']:
			continue

		res=SynthRegion(inputSamples, region, key, vel, numSamples, outputmode, samplerate, global_gain_db)
		bufs+=[res]
		region_numSamples = len(res)/4/chn
		if region_numSamples>max_numSamples:
			max_numSamples = region_numSamples	

	if len(bufs)<1:
		return (0, None)

	elif  len(bufs)<2:
		return (max_numSamples, bufs[0])

	else:
		return (max_numSamples, MixF32(bufs))

