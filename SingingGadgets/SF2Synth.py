import math
from .PyWavUtils import MixF32
from .PySF2Synth import Synth

TSF_LOOPMODE_NONE=0
TSF_LOOPMODE_CONTINUOUS=1
TSF_LOOPMODE_SUSTAIN = 2

# Output Modes
# Two channels with single left/right samples one after another
STEREO_INTERLEAVED = 0
# Two channels with all samples for the left channel first then right
STEREO_UNWEAVED = 1
# A single channel (stereo instruments are mixed into center)
MONO = 2

def GainToDecibels(gain):
	if gain <= .00001:
		return -100.0
	else:
		return 20.0 * math.log10(gain)

def TimeCents2Sec(timecents):
	return 2.0**(timecents/1200.0)

def DecibelsToGain(db):
	if db> -100.0:
		return 10.0**(db*0.05)
	else:
		return 0.0

def Cents2Hertz(cents):
	return 8.176 * (2.0 **(cents / 1200.0))

(TSF_SEGMENT_NONE, TSF_SEGMENT_DELAY, TSF_SEGMENT_ATTACK, TSF_SEGMENT_HOLD, TSF_SEGMENT_DECAY, TSF_SEGMENT_SUSTAIN, TSF_SEGMENT_RELEASE, TSF_SEGMENT_DONE) = tuple(range(8))
TSF_FASTRELEASETIME = 0.01

def VoiceEnvelopeNextsegment_Release(e, outSampleRate):
	e['segment'] = TSF_SEGMENT_DONE
	e['segmentIsExponential'] = False
	e['level'] = 0.0
	e['slope'] = 0.0
	e['samplesUntilNextSegment']=0x7FFFFFF

def VoiceEnvelopeNextsegment_Sustain(e, outSampleRate):
	e['segment'] = TSF_SEGMENT_RELEASE
	rel_time = TSF_FASTRELEASETIME
	if e['parameters']['release'] > 0:
		rel_time= e['parameters']['release']
	e['samplesUntilNextSegment']=rel_time*outSampleRate
	if e['isAmpEnv']:
		# I don't truly understand this; just following what LinuxSampler does.
		mysterySlope = -9.226 / e['samplesUntilNextSegment']
		e['slope'] = math.exp(mysterySlope)
		e['segmentIsExponential'] = True
	else:
		e['slope'] = -e['level'] / e['samplesUntilNextSegment']
		e['segmentIsExponential'] = False

def VoiceEnvelopeNextsegment_Decay(e, outSampleRate):
	e['segment'] = TSF_SEGMENT_SUSTAIN
	e['level'] = e['parameters']['sustain']
	e['slope'] = 0.0
	e['samplesUntilNextSegment'] = 0x7FFFFFFF
	e['segmentIsExponential'] = False

def VoiceEnvelopeNextsegment_Hold(e, outSampleRate):
	e['samplesUntilNextSegment']= int(e['parameters']['decay']*outSampleRate)
	if e['samplesUntilNextSegment'] > 0:
		e['segment'] = TSF_SEGMENT_DECAY
		e['level'] = 1.0
		if e['isAmpEnv']:
			# I don't truly understand this; just following what LinuxSampler does.
			mysterySlope = -9.226 / e['samplesUntilNextSegment']
			e['slope'] = math.exp(mysterySlope)
			e['segmentIsExponential'] = True
			if e['parameters']['sustain'] > 0.0:
				# Again, this is following LinuxSampler's example, which is similar to
				# SF2-style decay, where "decay" specifies the time it would take to
				# get to zero, not to the sustain level.  The SFZ spec is not that
				# specific about what "decay" means, so perhaps it's really supposed
				# to specify the time to reach the sustain level.
				e['samplesUntilNextSegment'] = int(math.log(e['parameters']['sustain'])/mysterySlope)
		else:
			e['slope'] = -1.0 / e['samplesUntilNextSegment']
			e['samplesUntilNextSegment'] = int(e['parameters']['decay']*(1.0-e['parameters']['sustain'])* outSampleRate)
			e['segmentIsExponential'] = False
	else:
		VoiceEnvelopeNextsegment_Decay(e,outSampleRate)

def VoiceEnvelopeNextsegment_Attack(e, outSampleRate):
	e['samplesUntilNextSegment']= int(e['parameters']['hold']*outSampleRate)
	if e['samplesUntilNextSegment'] > 0:
		e['segment'] = TSF_SEGMENT_HOLD
		e['segmentIsExponential'] = False
		e['level'] = 1.0
		e['slope'] = 0.0
	else:
		VoiceEnvelopeNextsegment_Hold(e,outSampleRate)

def VoiceEnvelopeNextsegment_Delay(e, outSampleRate):
	e['samplesUntilNextSegment']= int(e['parameters']['attack']*outSampleRate)
	if e['samplesUntilNextSegment'] > 0:
		if not e['isAmpEnv']:
			e['samplesUntilNextSegment'] = int(e['parameters']['attack']* ((145 - e['midiVelocity']) / 144.0) * outSampleRate)
		e['segment'] = TSF_SEGMENT_ATTACK
		e['segmentIsExponential'] = False
		e['level'] = 0.0
		e['slope'] = 1.0 / e['samplesUntilNextSegment']
	else:
		VoiceEnvelopeNextsegment_Attack(e,outSampleRate)

def VoiceEnvelopeNextsegment_None(e, outSampleRate):
	e['samplesUntilNextSegment'] = int(e['parameters']['delay']*outSampleRate)
	if e['samplesUntilNextSegment'] > 0:
		e['segment']=TSF_SEGMENT_DELAY
		e['segmentIsExponential']= False
		e['level'] = 0.0
		e['slope'] = 0.0
	else:
		VoiceEnvelopeNextsegment_Delay(e,outSampleRate)


VoiceEnvelopeNextsegment = (VoiceEnvelopeNextsegment_None, VoiceEnvelopeNextsegment_Delay, VoiceEnvelopeNextsegment_Attack, VoiceEnvelopeNextsegment_Hold, VoiceEnvelopeNextsegment_Decay, VoiceEnvelopeNextsegment_Sustain, VoiceEnvelopeNextsegment_Release)

def VoiceEnvelopeSetup(e, new_parameters, midiNoteNumber, midiVelocity, isAmpEnv, outSampleRate):
	e['parameters']=new_parameters.copy()
	if e['parameters']['keynumToHold']!=0.0:
		e['parameters']['hold']+=e['parameters']['keynumToHold']*(60.0 - midiNoteNumber)
		if e['parameters']['hold'] < -10000.0:
			e['parameters']['hold'] = 0.0
		else:
			e['parameters']['hold'] = TimeCents2Sec(e['parameters']['hold'])
	if e['parameters']['keynumToDecay']!=0.0:
		e['parameters']['decay']+=e['parameters']['keynumToDecay']*(60.0 - midiNoteNumber)
		if e['parameters']['decay'] < -10000.0:
			e['parameters']['decay'] = 0.0
		else:
			e['parameters']['decay'] = TimeCents2Sec(e['parameters']['decay'])
	e['midiVelocity'] = midiVelocity
	e['isAmpEnv'] = isAmpEnv
	VoiceEnvelopeNextsegment_None(e, outSampleRate)

def VoiceLowpassSetup(e, Fc):
	# Lowpass filter from http://www.earlevel.com/main/2012/11/26/biquad-c-source-code/
	K = math.tan(math.pi*Fc)
	KK = K * K
	norm = 1.0 / (1.0 + K * e['QInv'] + KK)
	e['a0'] = KK * norm
	e['a1'] = 2.0 * e['a0']
	e['b1'] = 2.0 * (KK -1.0) *norm
	e['b2'] = (1.0 - K *  e['QInv'] + KK) *norm

def VoiceLfoSetup(e, delay, freqCents, outSampleRate):
	e['samplesUntil'] = int(delay*outSampleRate)
	e['delta'] = 4.0 * Cents2Hertz(freqCents)/outSampleRate
	e['level'] = 0 

def VoiceEnvelopeProcess(e, numSamples, outSampleRate):
	if e['slope']!=0.0:
		if e['segmentIsExponential']:
			e['level'] *= e['slope'] ** numSamples
		else:
			e['level'] += e['slope'] * numSamples

	e['samplesUntilNextSegment'] -=numSamples
	if e['samplesUntilNextSegment'] <=0:
		if e['segment'] > TSF_SEGMENT_RELEASE:
			e['segment'] = TSF_SEGMENT_RELEASE
		VoiceEnvelopeNextsegment[e['segment']](e, outSampleRate)

def VoiceLfoProcess(e, blockSamples):
	if e['samplesUntil']>blockSamples:
		e['samplesUntil'] -= blockSamples
		return
	e['level']+=e['delta']*blockSamples
	if e['level'] > 1.0:
		e['delta'] = -e['delta'] 
		e['level'] = 2.0 - e['level']
	elif e['level'] < -1.0:
		e['delta'] = -e['delta'] 
		e['level'] = -2.0 - e['level']

TSF_RENDER_EFFECTSAMPLEBLOCK = 64

def SynthVoice(inputSamples, numSamples, voice, outputmode, samplerate):
	region = voice['region']
	updateModEnv = region['modEnvToPitch'] or region['modEnvToFilterFc']
	updateModLFO = voice['modlfo']['delta']!=0.0 and (region['modLfoToPitch']!=0 or region['modLfoToFilterFc']!=0 or region['modLfoToVolume']!=0)
	updateVibLFO = voice['viblfo']['delta']!= 0.0 and (region['vibLfoToPitch']!= 0)
	isLooping = voice['loopStart'] < voice['loopEnd']

	tmpLoopStart = voice['loopStart']
	tmpLoopEnd  = voice['loopEnd']

	tmpSampleEnd = region['end']
	tmpSourceSamplePosition = voice['ns']['sourceSamplePosition']

	tmpLowPass = voice['lowpass'].copy()
	dynamicLowpass = region['modLfoToFilterFc']!=0 or region['modEnvToFilterFc']!=0
	dynamicPitchRatio = region['modLfoToPitch']!=0 or region['modEnvToPitch']!=0 or region['vibLfoToPitch']!=0
	dynamicGain = region['modLfoToVolume']!=0

	tmpSampleRate=0
	tmpInitialFilterFc = 0
	tmpModLfoToFilterFc = 0
	tmpModEnvToFilterFc = 0
	if dynamicLowpass:
		tmpSampleRate = samplerate
		tmpInitialFilterFc = region['initialFilterFc']
		tmpModLfoToFilterFc = region['modLfoToFilterFc']
		tmpModEnvToFilterFc = region['modEnvToFilterFc']

	pitchRatio = TimeCents2Sec(voice['pitchInputTimecents'])*voice['pitchOutputFactor']
	tmpModLfoToPitch = 0
	tmpVibLfoToPitch = 0
	tmpModEnvToPitch = 0
	if dynamicPitchRatio:
		pitchRatio = 0
		tmpModLfoToPitch = region['modLfoToPitch']
		tmpVibLfoToPitch = region['vibLfoToPitch']
		tmpModEnvToPitch = region['modEnvToPitch']

	noteGain = DecibelsToGain(voice['noteGainDB'])
	tmpModLfoToVolume = 0
	if dynamicGain:
		noteGain = 0
		tmpModLfoToVolume = region['modLfoToVolume']*0.1

	control={
		'outputmode': outputmode,
		'loopStart': tmpLoopStart,
		'loopEnd': tmpLoopEnd,
		'end': tmpSampleEnd,
		'panFactorLeft': voice['panFactorLeft'],
		'panFactorRight': voice['panFactorRight'],
		'effect_sample_block': TSF_RENDER_EFFECTSAMPLEBLOCK,
		'controlPnts': []
	}
	
	countSamples = 0 

	while True:
		blockSamples = TSF_RENDER_EFFECTSAMPLEBLOCK
		countSamples += blockSamples

		if countSamples >= numSamples and voice['ampenv']['segment']<TSF_SEGMENT_RELEASE:
			VoiceEnvelopeNextsegment_Sustain(voice['ampenv'], samplerate)
			VoiceEnvelopeNextsegment_Sustain(voice['modenv'], samplerate)
			if voice['region']['loop_mode'] == TSF_LOOPMODE_SUSTAIN:
				# Continue playing, but stop looping.
				isLooping = False

		if dynamicLowpass:
			fres = tmpInitialFilterFc + voice['modlfo']['level'] * tmpModLfoToFilterFc + voice['modenv']['level'] * tmpModEnvToFilterFc
			tmpLowpass['active'] = fres <= 13500.0
			if tmpLowpass['active']:
				VoiceLowpassSetup(tmpLowpass, Cents2Hertz(fres)/tmpSampleRate)

		if dynamicPitchRatio:
			pitchRatio = TimeCents2Sec(voice['pitchInputTimecents'] + (voice['modlfo']['level']*tmpModLfoToPitch +voice['viblfo']['level']*tmpVibLfoToPitch + voice['modenv']['level']*tmpModEnvToPitch))*  voice['pitchOutputFactor']

		if dynamicGain:
			noteGain = DecibelsToGain(voice['noteGainDB']+ (voice['modlfo']['level']*tmpModLfoToVolume))

		gainMono = noteGain * voice['ampenv']['level']

		# Update EG.
		VoiceEnvelopeProcess(voice['ampenv'], blockSamples, samplerate)
		if updateModEnv:
			VoiceEnvelopeProcess(voice['modenv'], blockSamples, samplerate)

		# Update LFOs.
		if updateModLFO:
			VoiceLfoProcess(voice['modlfo'], blockSamples)
		if updateVibLFO:
			VoiceLfoProcess(voice['viblfo'], blockSamples)

		ctrlPnt = {
			'looping': isLooping,
			'gainMono': gainMono,
			'pitchRatio': pitchRatio,
			'lowPass': {
				'active': tmpLowPass['active'],
				'a0': tmpLowPass['a0'],
				'a1': tmpLowPass['a1'],
				'b1': tmpLowPass['b1'],
				'b2': tmpLowPass['b2'],
			}
		}

		control['controlPnts']+=[ctrlPnt]

		tmpSourceSamplePosition +=  pitchRatio*blockSamples

		while tmpSourceSamplePosition > tmpLoopEnd and isLooping: 
			tmpSourceSamplePosition -= (tmpLoopEnd - tmpLoopStart + 1.0)

		if tmpSourceSamplePosition > tmpSampleEnd or voice['ampenv']['segment'] == TSF_SEGMENT_DONE:
			break

	chn = 2
	if outputmode == MONO:
		chn =1

	outBuf = b'\0' * (countSamples*chn*4)

	Synth(inputSamples, outBuf, countSamples, voice['ns'], control)

	return (countSamples,outBuf)

def SynthNote(inputSamples, preset, key, vel, numSamples, outputmode = STEREO_INTERLEAVED, samplerate = 44100.0, global_gain_db = 0.0):
	ikey=int(key+0.5)
	midiVelocity = int(vel*127)
	voices=[]
	for region in preset['regions']:
		if ikey < region['lokey'] or ikey > region['hikey'] or midiVelocity < region['lovel'] or midiVelocity > region['hivel']:
			continue

		voice = {
			'region': region,
			'noteGainDB': global_gain_db - region['attenuation'] - GainToDecibels(1.0/vel),
			'ns': {},
			'ampenv': {},
			'modenv': {},
			'lowpass': {},
			'modlfo':{},
			'viblfo':{}
		}

		note = key + region['transpose'] +region['tune'] / 100.0
		adjustedPitch = region['pitch_keycenter'] + (note - region['pitch_keycenter'])*(region['pitch_keytrack']/100.0)
		voice['pitchInputTimecents'] = adjustedPitch * 100.0
		voice['pitchOutputFactor'] = region['sample_rate']/(TimeCents2Sec(region['pitch_keycenter']*100.0) * samplerate)

		# The SFZ spec is silent about the pan curve, but a 3dB pan law seems common. This sqrt() curve matches what Dimension LE does; Alchemy Free seems closer to sin(adjustedPan * pi/2).
		voice['panFactorLeft'] = math.sqrt(0.5 - region['pan'])
		voice['panFactorRight'] = math.sqrt(0.5 + region['pan'])

		# Offset/end.
		voice['ns']['sourceSamplePosition'] = region['offset']

		# Loop.
		doLoop = region['loop_mode'] != TSF_LOOPMODE_NONE and region['loop_start'] < region['loop_end']
		voice['loopStart'] = 0
		voice['loopEnd'] = 0
		if doLoop:
			voice['loopStart'] = region['loop_start']
			voice['loopEnd'] = region['loop_end']

		# Setup envelopes.
		VoiceEnvelopeSetup(voice['ampenv'], region['ampenv'], key, midiVelocity, True, samplerate);
		VoiceEnvelopeSetup(voice['modenv'], region['modenv'], key, midiVelocity, False, samplerate);

		# Setup lowpass filter.
		filterQDB = region['initialFilterQ'] / 10.0
		voice['lowpass']['QInv'] = 1.0 / (10.0 ** (filterQDB / 20.0))
		voice['ns']['lowPass']={
			'z1': 0,
			'z2': 0,
		}
		voice['lowpass']['active'] =  region['initialFilterFc'] <= 13500
		if voice['lowpass']['active']:
			VoiceLowpassSetup(voice['lowpass'],Cents2Hertz(region['initialFilterFc']) / samplerate)

		# Setup LFO filters.
		VoiceLfoSetup(voice['modlfo'], region['delayModLFO'], region['freqModLFO'], samplerate)
		VoiceLfoSetup(voice['viblfo'], region['delayVibLFO'], region['freqVibLFO'], samplerate);

		voices+=[voice]

	if len(voices)<1:
		return (0, None)

	elif  len(voices)<2:
		return SynthVoice(inputSamples, numSamples, voices[0], outputmode, samplerate)

	else:
		bufs=[]
		maxNumSamples = 0
		for voice in voices:
			res = SynthVoice(inputSamples, numSamples, voice, outputmode, samplerate)
			if res[0]>maxNumSamples:
				maxNumSamples = res[0]
			bufs+=[res[1]]

		return (maxNumSamples, MixF32(bufs))

		
		







