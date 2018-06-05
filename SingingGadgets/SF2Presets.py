import struct

def EnvelopeClear(env):
	env['delay'] = -12000.0
	env['attack'] = -12000.0
	env['hold'] = -12000.0
	env['decay'] = -12000.0
	env['sustain'] = 0.0
	env['release'] = -12000.0
	env['keynumToHold'] = 0.0
	env['keynumToDecay'] = 0.0

def RegionClear(region):
	region['loop_mode'] = 0
	region['sample_rate'] = 0
	region['lokey'] = 0
	region['hikey'] = 127
	region['lovel'] = 0
	region['hivel'] = 127
	region['group'] = 0
	region['offset'] = 0
	region['end'] = 0
	region['loop_start'] = 0
	region['loop_end'] = 0
	region['transpose'] = 0
	region['tune'] = 0
	region['pitch_keycenter'] = -1
	region['pitch_keytrack'] = 100
	region['attenuation'] = 0.0
	region['pan'] = 0.0
	region['ampenv'] = {}
	EnvelopeClear(region['ampenv'])
	region['modenv'] = {}
	EnvelopeClear(region['modenv'])
	region['initialFilterQ'] = 0
	region['initialFilterFc'] = 13500
	region['modEnvToPitch'] = 0
	region['modEnvToFilterFc'] = 0
	region['modLfoToFilterFc'] = 0
	region['modLfoToVolume'] = 0
	region['delayModLFO'] = -12000.0
	region['freqModLFO'] = 0
	region['modLfoToPitch'] = 0
	region['delayVibLFO'] = -12000.0
	region['freqVibLFO'] = 0
	region['vibLfoToPitch'] = 0

def EnvelopeClearForRelative(env):
	env['delay'] = 0.0
	env['attack'] = 0.0
	env['hold'] = 0.0
	env['decay'] = 0.0
	env['sustain'] = 0.0
	env['release'] = 0.0
	env['keynumToHold'] = 0.0
	env['keynumToDecay'] = 0.0

def RegionClearForRelative(region):
	region['loop_mode'] = 0
	region['sample_rate'] = 0
	region['lokey'] = 0
	region['hikey'] = 127
	region['lovel'] = 0
	region['hivel'] = 127
	region['group'] = 0
	region['offset'] = 0
	region['end'] = 0
	region['loop_start'] = 0
	region['loop_end'] = 0
	region['transpose'] = 0
	region['tune'] = 0
	region['pitch_keycenter'] = 60
	region['pitch_keytrack'] = 0
	region['attenuation'] = 0.0
	region['pan'] = 0.0
	region['ampenv'] = {}
	EnvelopeClearForRelative(region['ampenv'])
	region['modenv'] = {}
	EnvelopeClearForRelative(region['modenv'])
	region['initialFilterQ'] = 0
	region['initialFilterFc'] = 0
	region['modEnvToPitch'] = 0
	region['modEnvToFilterFc'] = 0
	region['modLfoToFilterFc'] = 0
	region['modLfoToVolume'] = 0
	region['delayModLFO'] = 0.0
	region['freqModLFO'] = 0
	region['modLfoToPitch'] = 0
	region['delayVibLFO'] = 0.0
	region['freqVibLFO'] = 0
	region['vibLfoToPitch'] = 0

def RegionCopy(region):
	ret = region.copy()
	ret['ampenv']=region['ampenv'].copy()
	ret['modenv']=region['modenv'].copy()
	return ret

def TimeCents2Sec(timecents):
	return 2.0**(timecents/1200.0)

def DecibelsToGain(db):
	if db> -100.0:
		return 10.0**(db*0.05)
	else:
		return 0.0

def RegionEnvtosecs(env, sustainIsGain):
	# EG times need to be converted from timecents to seconds.
	# Pin very short EG segments.  Timecents don't get to zero, and our EG is
	# happier with zero values.
	if env['delay']< -11950.0:
		env['delay']=0.0
	else:
		env['delay']=TimeCents2Sec(env['delay'])
	if env['attack']< -11950.0:
		env['attack']=0.0
	else:
		env['attack']=TimeCents2Sec(env['attack'])
	if env['release']< -11950.0:
		env['release']=0.0
	else:
		env['release']=TimeCents2Sec(env['release'])

	# If we have dynamic hold or decay times depending on key number we need
	# to keep the values in timecents so we can calculate it during startNote
	if env['keynumToHold']==0.0:
		if env['hold']< -11950.0:
			env['hold']=0.0
		else:
			env['hold']=TimeCents2Sec(env['hold'])
	if env['keynumToDecay']==0.0:
		if env['decay']< -11950.0:
			env['decay']=0.0
		else:
			env['decay']=TimeCents2Sec(env['decay'])

	if env['sustain'] <0.0:
		env['sustain'] =0.0
	elif sustainIsGain:
		env['sustain'] = DecibelsToGain(-env['sustain']/10.0)
	else:
		env['sustain'] = 1.0 - (env['sustain']/1000.0)

TSF_LOOPMODE_NONE=0
TSF_LOOPMODE_CONTINUOUS=1
TSF_LOOPMODE_SUSTAIN = 2
# region operators
def ROP_Unused(region, amount):
	pass
def ROP_Reserved(region, amount):
	pass
def ROP_StartAddrsOffset(region, amount):
	region['offset'] += struct.unpack('h',amount)[0]
def ROP_EndAddrsOffset(region, amount):
	region['end'] += struct.unpack('h',amount)[0]
def ROP_StartloopAddrsOffset(region, amount):
	region['loop_start'] += struct.unpack('h',amount)[0]
def ROP_EndloopAddrsOffset(region, amount):
	region['loop_end'] += struct.unpack('h',amount)[0]
def ROP_StartAddrsCoarseOffset(region, amount):
	region['offset'] += struct.unpack('h',amount)[0] * 32768
def ROP_ModLfoToPitch(region, amount):
	region['modLfoToPitch'] = struct.unpack('h',amount)[0]
def ROP_VibLfoToPitch(region, amount):
	region['vibLfoToPitch'] = struct.unpack('h',amount)[0]
def ROP_ModEnvToPitch(region, amount):
	region['modEnvToPitch'] = struct.unpack('h',amount)[0]
def ROP_InitialFilterFc(region, amount):
	region['initialFilterFc'] = struct.unpack('h',amount)[0]
def ROP_InitialFilterQ(region, amount):
	region['initialFilterQ'] = struct.unpack('h',amount)[0]
def ROP_ModLfoToFilterFc(region, amount):
	region['modLfoToFilterFc'] = struct.unpack('h',amount)[0]
def ROP_ModEnvToFilterFc(region, amount):
	region['modEnvToFilterFc'] = struct.unpack('h',amount)[0]
def ROP_EndAddrsCoarseOffset(region, amount):
	region['end'] += struct.unpack('h',amount)[0]* 32768
def ROP_ModLfoToVolume(region, amount):
	region['modLfoToVolume'] = struct.unpack('h',amount)[0]
def ROP_ChorusEffectsSend(region, amount):
	pass
def ROP_ReverbEffectsSend(region, amount):
	pass
def ROP_Pan(region, amount):
	region['pan'] = struct.unpack('h',amount)[0]/1000.0
def ROP_DelayModLFO(region, amount):
	region['delayModLFO'] = struct.unpack('h',amount)[0]
def ROP_FreqModLFO(region, amount):
	region['freqModLFO'] = struct.unpack('h',amount)[0]
def ROP_DelayVibLFO(region, amount):
	region['delayVibLFO'] = struct.unpack('h',amount)[0]
def ROP_FreqVibLFO(region, amount):
	region['freqVibLFO'] = struct.unpack('h',amount)[0]
def ROP_DelayModEnv(region, amount):
	region['modenv']['delay'] = struct.unpack('h',amount)[0]
def ROP_AttackModEnv(region, amount):
	region['modenv']['attack'] = struct.unpack('h',amount)[0]
def ROP_HoldModEnv(region, amount):
	region['modenv']['hold'] = struct.unpack('h',amount)[0]
def ROP_DecayModEnv(region, amount):
	region['modenv']['decay'] = struct.unpack('h',amount)[0]
def ROP_SustainModEnv(region, amount):
	region['modenv']['sustain'] = struct.unpack('h',amount)[0]
def ROP_ReleaseModEnv(region, amount):
	region['modenv']['release'] = struct.unpack('h',amount)[0]
def ROP_KeynumToModEnvHold(region, amount):
	region['modenv']['keynumToHold'] = struct.unpack('h',amount)[0]
def ROP_KeynumToModEnvDecay(region, amount):
	region['modenv']['keynumToDecay'] = struct.unpack('h',amount)[0]
def ROP_DelayVolEnv(region, amount):
	region['ampenv']['delay'] = struct.unpack('h',amount)[0]
def ROP_AttackVolEnv(region, amount):
	region['ampenv']['attack'] = struct.unpack('h',amount)[0]
def ROP_HoldVolEnv(region, amount):
	region['ampenv']['hold'] = struct.unpack('h',amount)[0]
def ROP_DecayVolEnv(region, amount):
	region['ampenv']['decay'] = struct.unpack('h',amount)[0]
def ROP_SustainVolEnv(region, amount):
	region['ampenv']['sustain'] = struct.unpack('h',amount)[0]
def ROP_ReleaseVolEnv(region, amount):
	region['ampenv']['release'] = struct.unpack('h',amount)[0]
def ROP_KeynumToVolEnvHold(region, amount):
	region['ampenv']['keynumToHold'] = struct.unpack('h',amount)[0]
def ROP_KeynumToVolEnvDecay(region, amount):
	region['ampenv']['keynumToDecay'] = struct.unpack('h',amount)[0]
def ROP_Instrument(region, amount):
	pass
def ROP_KeyRange(region, amount):
	(region['lokey'], region['hikey'])= struct.unpack('BB',amount)
def ROP_VelRange(region, amount):
	(region['lovel'], region['hivel'])= struct.unpack('BB',amount)
def ROP_StartloopAddrsCoarseOffset(region, amount):
	region['loop_start'] += struct.unpack('h',amount)[0] * 32768
def ROP_Keynum(region, amount):
	pass
def ROP_Velocity(region, amount):
	pass
def ROP_InitialAttenuation(region, amount):
	region['attenuation'] += struct.unpack('h',amount)[0] * 0.1
def ROP_EndloopAddrsCoarseOffset(region, amount):
	region['loop_end'] += struct.unpack('h',amount)[0] * 32768
def ROP_CoarseTune(region, amount):
	region['transpose'] += struct.unpack('h',amount)[0]
def ROP_FineTune(region, amount):
	region['tune'] += struct.unpack('h',amount)[0]
def ROP_SampleID(region, amount):
	pass
def ROP_SampleModes(region, amount):
	word=  struct.unpack('H',amount)[0]
	if word % 4 ==3:
		region['loop_mode'] = TSF_LOOPMODE_SUSTAIN
	elif word % 4 == 1:
		region['loop_mode'] = TSF_LOOPMODE_CONTINUOUS
	else:
		region['loop_mode'] = TSF_LOOPMODE_NONE
def ROP_ScaleTuning(region, amount):
	region['pitch_keytrack'] = struct.unpack('h',amount)[0] 
def ROP_ExclusiveClass(region, amount):
	region['group'] = struct.unpack('H',amount)[0] 
def ROP_OverridingRootKey(region, amount):
	region['pitch_keycenter'] = struct.unpack('h',amount)[0] 

region_operators = [ROP_StartAddrsOffset, ROP_EndAddrsOffset, ROP_StartloopAddrsOffset, ROP_EndloopAddrsOffset, ROP_StartAddrsCoarseOffset, 
		ROP_ModLfoToPitch, ROP_VibLfoToPitch, ROP_ModEnvToPitch, ROP_InitialFilterFc, ROP_InitialFilterQ, ROP_ModLfoToFilterFc, 
		ROP_ModEnvToFilterFc, ROP_EndAddrsCoarseOffset, ROP_ModLfoToVolume, ROP_Unused, ROP_ChorusEffectsSend, ROP_ReverbEffectsSend, 
		ROP_Pan, ROP_Unused, ROP_Unused, ROP_Unused, ROP_DelayModLFO, ROP_FreqModLFO, ROP_DelayVibLFO, ROP_FreqVibLFO, ROP_DelayModEnv, 
		ROP_AttackModEnv, ROP_HoldModEnv, ROP_DecayModEnv, ROP_SustainModEnv, ROP_ReleaseModEnv, ROP_KeynumToModEnvHold, 
		ROP_KeynumToModEnvDecay, ROP_DelayVolEnv, ROP_AttackVolEnv, ROP_HoldVolEnv, ROP_DecayVolEnv, ROP_SustainVolEnv, 
		ROP_ReleaseVolEnv, ROP_KeynumToVolEnvHold, ROP_KeynumToVolEnvDecay, ROP_Instrument, ROP_Reserved, ROP_KeyRange, ROP_VelRange, 
		ROP_StartloopAddrsCoarseOffset, ROP_Keynum, ROP_Velocity, ROP_InitialAttenuation, ROP_Reserved, ROP_EndloopAddrsCoarseOffset, 
		ROP_CoarseTune, ROP_FineTune, ROP_SampleID, ROP_SampleModes, ROP_Reserved, ROP_ScaleTuning,
		ROP_ExclusiveClass, ROP_OverridingRootKey]

def LoadPresets(sf2):
	hydra= sf2[0]
	fontSamples = sf2[1]
	fontSampleCount = len(fontSamples)//4
	presets=[]
	if ('phdrs' in hydra) and ('pbags' in hydra) and ('pmods' in hydra) and ('pgens' in hydra) and ('insts' in hydra) and ('ibags' in hydra) and ('imods' in hydra) and ('igens' in hydra) and ('shdrs' in hydra):
		presetNum= len(hydra['phdrs']) -1 # Exclude EOP
		presets = [None] * presetNum

		GenInstrument = 41
		GenKeyRange = 43
		GenVelRange = 44
		GenSampleID = 53
		
		for i in range(presetNum):
			sortedIndex = 0
			region_index = 0
			phdr = hydra['phdrs'][i]
			for j in range(presetNum):
				otherphdr = hydra['phdrs'][j]
				if i==j or otherphdr['bank']>phdr['bank']:
					continue
				elif otherphdr['bank']<phdr['bank']:
					sortedIndex+=1
				elif otherphdr['preset']>phdr['preset']:
					continue
				elif otherphdr['preset']<phdr['preset']:
					sortedIndex+=1
				elif j<i:
					sortedIndex+=1

			presets[sortedIndex]={
				'presetName' : phdr['presetName'],
				'bank': phdr['bank'],
				'preset': phdr['preset'],
				'regionNum': 0
			}

			preset = presets[sortedIndex]

			# count regions covered by this preset
			for j in range(phdr['presetBagNdx'],  hydra['phdrs'][i+1]['presetBagNdx']):
				pbag= hydra['pbags'][j]
				plokey = 0
				phikey = 127
				plovel = 0
				phivel = 127
				for k in range(pbag['genNdx'], hydra['pbags'][j+1]['genNdx']):
					pgen = hydra['pgens'][k]
					if pgen['genOper'] == GenKeyRange:
						(plokey,phikey) = struct.unpack('BB',pgen['genAmount'])
						continue
					if pgen['genOper'] == GenVelRange:
						(plovel,phivel) = struct.unpack('BB',pgen['genAmount'])
						continue
					if pgen['genOper'] != GenInstrument:
						continue
					whichInst = struct.unpack('H',pgen['genAmount'])[0]
					if whichInst >= len(hydra['insts']):
						continue
					inst = hydra['insts'][whichInst]
					for l in range(inst['instBagNdx'], hydra['insts'][whichInst+1]['instBagNdx']):
						ibag = hydra['ibags'][l]
						ilokey = 0
						ihikey = 127
						ilovel = 0
						ihivel = 127
						for m in range(ibag['instGenNdx'], hydra['ibags'][l+1]['instGenNdx']):
							igen = hydra['igens'][m]
							if igen['genOper'] == GenKeyRange:
								(ilokey, ihikey)= struct.unpack('BB',igen['genAmount'])
								continue
							if igen['genOper'] == GenVelRange:
								(ilovel, ihivel)= struct.unpack('BB',igen['genAmount'])
							if igen['genOper'] == GenSampleID and ihikey>=plokey and ilokey <= phikey and ihivel >= plovel and ilovel <= phivel:
								preset['regionNum']+=1

			preset['regions']= [None]*preset['regionNum']
			globalRegion={}
			RegionClearForRelative(globalRegion)

			# Zones
			for j in range(phdr['presetBagNdx'],  hydra['phdrs'][i+1]['presetBagNdx']):
				pbag= hydra['pbags'][j]
				presetRegion = RegionCopy(globalRegion)
				hadGenInstrument =0

				# Generators
				for k in range(pbag['genNdx'], hydra['pbags'][j+1]['genNdx']):
					pgen = hydra['pgens'][k]

					# Instrument.
					if pgen['genOper'] == GenInstrument:
						whichInst = struct.unpack('H',pgen['genAmount'])[0]
						if whichInst >= len(hydra['insts']):
							continue

						instRegion = {}
						RegionClear(instRegion)
						inst= hydra['insts'][whichInst]
						for l in range(inst['instBagNdx'], hydra['insts'][whichInst+1]['instBagNdx']):
							ibag = hydra['ibags'][l]
							zoneRegion = RegionCopy(instRegion)
							hadSampleID=0
							for m in range(ibag['instGenNdx'], hydra['ibags'][l+1]['instGenNdx']):
								igen = hydra['igens'][m]
								if igen['genOper'] == GenSampleID:
									# preset region key and vel ranges are a filter for the zone regions
									if zoneRegion['hikey'] < presetRegion['lokey'] or zoneRegion['lokey'] > presetRegion['hikey']:
										continue
									if zoneRegion['hivel'] < presetRegion['lovel'] or zoneRegion['lovel'] > presetRegion['hivel']:
										continue
									if presetRegion['lokey'] > zoneRegion['lokey']:
										zoneRegion['lokey'] =  presetRegion['lokey']
									if presetRegion['hikey'] < zoneRegion['hikey']:
										zoneRegion['hikey'] = presetRegion['hikey']
									if presetRegion['lovel'] > zoneRegion['lovel']:
										zoneRegion['lovel'] = presetRegion['lovel']
									if presetRegion['hivel'] < zoneRegion['hivel']:
										zoneRegion['hivel'] = presetRegion['hivel']

									# sum regions
									zoneRegion['offset'] += presetRegion['offset']
									zoneRegion['end'] += presetRegion['end']
									zoneRegion['loop_start'] += presetRegion['loop_start']
									zoneRegion['loop_end'] += presetRegion['loop_end']
									zoneRegion['transpose'] += presetRegion['transpose']
									zoneRegion['tune'] += presetRegion['tune']
									zoneRegion['pitch_keytrack'] += presetRegion['pitch_keytrack']
									zoneRegion['attenuation'] += presetRegion['attenuation']
									zoneRegion['pan'] += presetRegion['pan']
									zoneRegion['ampenv']['delay'] += presetRegion['ampenv']['delay']
									zoneRegion['ampenv']['attack'] += presetRegion['ampenv']['attack']
									zoneRegion['ampenv']['hold'] += presetRegion['ampenv']['hold']
									zoneRegion['ampenv']['decay'] += presetRegion['ampenv']['decay']
									zoneRegion['ampenv']['sustain'] += presetRegion['ampenv']['sustain']
									zoneRegion['ampenv']['release'] += presetRegion['ampenv']['release']
									zoneRegion['modenv']['delay'] += presetRegion['modenv']['delay']
									zoneRegion['modenv']['attack'] += presetRegion['modenv']['attack']
									zoneRegion['modenv']['hold'] += presetRegion['modenv']['hold']
									zoneRegion['modenv']['decay'] += presetRegion['modenv']['decay']
									zoneRegion['modenv']['sustain'] += presetRegion['modenv']['sustain']
									zoneRegion['modenv']['release'] += presetRegion['modenv']['release']
									zoneRegion['initialFilterQ'] += presetRegion['initialFilterQ']
									zoneRegion['initialFilterFc'] += presetRegion['initialFilterFc']
									zoneRegion['modEnvToPitch'] += presetRegion['modEnvToPitch']
									zoneRegion['modEnvToFilterFc'] += presetRegion['modEnvToFilterFc']
									zoneRegion['delayModLFO'] += presetRegion['delayModLFO']
									zoneRegion['freqModLFO'] += presetRegion['freqModLFO']
									zoneRegion['modLfoToPitch'] += presetRegion['modLfoToPitch']
									zoneRegion['modLfoToFilterFc'] += presetRegion['modLfoToFilterFc']
									zoneRegion['modLfoToVolume'] += presetRegion['modLfoToVolume']
									zoneRegion['delayVibLFO'] += presetRegion['delayVibLFO']
									zoneRegion['freqVibLFO'] += presetRegion['freqVibLFO']
									zoneRegion['vibLfoToPitch'] += presetRegion['vibLfoToPitch']

									# EG times need to be converted from timecents to seconds.
									RegionEnvtosecs(zoneRegion['ampenv'], True)
									RegionEnvtosecs(zoneRegion['modenv'], False)

									# LFO times need to be converted from timecents to seconds.
									if zoneRegion['delayModLFO']< -11950.0:
										zoneRegion['delayModLFO'] = 0
									else:
										zoneRegion['delayModLFO'] = TimeCents2Sec(zoneRegion['delayModLFO'])

									if zoneRegion['delayVibLFO']< -11950.0:
										zoneRegion['delayVibLFO'] = 0
									else:
										zoneRegion['delayVibLFO'] = TimeCents2Sec(zoneRegion['delayVibLFO'])

									# Pin values to their ranges.
									if zoneRegion['pan']<-0.5:
										zoneRegion['pan'] = -0.5
									elif zoneRegion['pan']>0.5:
										zoneRegion['pan'] = 0.5

									if zoneRegion['initialFilterQ'] < 1500 or zoneRegion['initialFilterQ'] > 13500:
										 zoneRegion['initialFilterQ'] = 0

									shdr= hydra['shdrs'][struct.unpack('H',igen['genAmount'])[0]]
									zoneRegion['offset']+=shdr['start']
									zoneRegion['end']+=shdr['end']
									zoneRegion['loop_start']+=shdr['startLoop']
									zoneRegion['loop_end']+=shdr['endLoop']

									if shdr['endLoop'] > 0:
										zoneRegion['loop_end'] -= 1

									if zoneRegion['pitch_keycenter'] ==-1:
										zoneRegion['pitch_keycenter'] = shdr['originalPitch']

									zoneRegion['tune'] += shdr['pitchCorrection']
									zoneRegion['sample_rate'] = shdr['sampleRate']
									if zoneRegion['end']!=0 and zoneRegion['end']< fontSampleCount:
										zoneRegion['end']+=1
									else:
										zoneRegion['end']=fontSampleCount

									preset['regions'][region_index] = RegionCopy(zoneRegion)
									region_index+=1
									hadSampleID = 1
								else:
									genOper=igen['genOper']
									if genOper<len(region_operators):
										region_operators[genOper](zoneRegion, igen['genAmount'])

							# Handle instrument's global zone.
							if l==inst['instBagNdx'] and hadSampleID == 0:
								instRegion =RegionCopy(zoneRegion)

						hadGenInstrument = 1;
					else:
						genOper=pgen['genOper']
						if genOper<len(region_operators):
							region_operators[genOper](presetRegion, pgen['genAmount'])
				# Handle preset's global zone.
				if j == phdr['presetBagNdx'] and hadGenInstrument==0:
					globalRegion = RegionCopy(presetRegion)
	return presets


