#!/usr/bin/python3
import struct
from .PyWavUtils import S16ToF32

def decode_string(with_zero):
	no_zero=bytes()
	for i in range(len(with_zero)):
		b= with_zero[i]
		if b!=0 and b<128:
			no_zero+=with_zero[i:i+1]
		else:
			break
	return no_zero.decode('ascii')

def ReadRiffChunk(f):
	fourcc = f.read(4).decode('ascii')
	size = struct.unpack('i',f.read(4))[0]
	if fourcc=='RIFF' or fourcc=='LIST':
		fourcc =  f.read(4).decode('ascii')
		size-=4
	return (fourcc,size)

def HydraRead_phdr(f):
	phdr={}
	phdr['presetName'] = decode_string(f.read(20))
	phdr['preset'] = struct.unpack('H',f.read(2))[0]
	phdr['bank'] = struct.unpack('H',f.read(2))[0]
	phdr['presetBagNdx'] = struct.unpack('H',f.read(2))[0]
	phdr['library'] = struct.unpack('I',f.read(4))[0]
	phdr['genre'] = struct.unpack('I',f.read(4))[0]
	phdr['morphology'] = struct.unpack('I',f.read(4))[0]
	return phdr

def HydraRead_pbag(f):
	pbag={}
	pbag['genNdx'] = struct.unpack('H',f.read(2))[0]
	pbag['modNdx'] = struct.unpack('H',f.read(2))[0]
	return pbag

def HydraRead_pmod(f):
	pmod={}
	pmod['modSrcOper'] = struct.unpack('H',f.read(2))[0]
	pmod['modDestOper'] = struct.unpack('H',f.read(2))[0]
	pmod['modAmount'] = struct.unpack('h',f.read(2))[0]
	pmod['modAmtSrcOper'] = struct.unpack('H',f.read(2))[0]
	pmod['modTransOper'] = struct.unpack('H',f.read(2))[0]
	return pmod

def HydraRead_pgen(f):
	pgen={}
	pgen['genOper'] = struct.unpack('H',f.read(2))[0]
	pgen['genAmount'] = f.read(2) # delay the unpacking
	return pgen

def HydraRead_inst(f):
	inst={}
	inst['instName'] = decode_string(f.read(20))
	inst['instBagNdx'] = struct.unpack('H',f.read(2))[0]
	return inst

def HydraRead_ibag(f):
	ibag={}
	ibag['instGenNdx'] = struct.unpack('H',f.read(2))[0]
	ibag['instModNdx'] = struct.unpack('H',f.read(2))[0]
	return ibag

def HydraRead_imod(f):
	imod={}
	imod['modSrcOper'] = struct.unpack('H',f.read(2))[0]
	imod['modDestOper'] = struct.unpack('H',f.read(2))[0]
	imod['modAmount'] = struct.unpack('h',f.read(2))[0]
	imod['modAmtSrcOper'] = struct.unpack('H',f.read(2))[0]
	imod['modTransOper'] = struct.unpack('H',f.read(2))[0]
	return imod

def HydraRead_igen(f):
	igen={}
	igen['genOper'] = struct.unpack('H',f.read(2))[0]
	igen['genAmount'] = f.read(2) # delay the unpacking
	return igen

def HydraRead_shdr(f):
	shdr={}
	shdr['sampleName'] =  decode_string(f.read(20))
	shdr['start'] = struct.unpack('I',f.read(4))[0]
	shdr['end'] = struct.unpack('I',f.read(4))[0]
	shdr['startLoop'] = struct.unpack('I',f.read(4))[0]
	shdr['endLoop'] = struct.unpack('I',f.read(4))[0]
	shdr['sampleRate'] = struct.unpack('I',f.read(4))[0]
	shdr['originalPitch'] = struct.unpack('B',f.read(1))[0]
	shdr['pitchCorrection'] = struct.unpack('b',f.read(1))[0]
	shdr['sampleLink'] = struct.unpack('H',f.read(2))[0]
	shdr['sampleType'] = struct.unpack('H',f.read(2))[0]
	return shdr

hydra_trunk_types={
	'phdr': (HydraRead_phdr, 38),
	'pbag': (HydraRead_pbag, 4),
	'pmod': (HydraRead_pmod, 10),
	'pgen': (HydraRead_pgen, 4),
	'inst': (HydraRead_inst, 22),
	'ibag': (HydraRead_ibag, 4),
	'imod': (HydraRead_imod, 10),
	'igen': (HydraRead_igen, 4),
	'shdr': (HydraRead_shdr, 46),
}


def HandleChunk(f, hydra, chunk):
	if not chunk[0] in hydra_trunk_types:
		return False
	trunkType= hydra_trunk_types[chunk[0]]	
	num = chunk[1]//trunkType[1]
	hydra[chunk[0]+'s'] = [trunkType[0](f) for i in range(num)]
	return True

def LoadSF2(fn):
	hydra={}
	fontSamples=bytes()
	with open(fn, 'rb') as f:
		f.seek(0,2)
		fsize=f.tell()
		f.seek(0,0)
		chunkHead = ReadRiffChunk(f)
		if chunkHead[0]!='sfbk':
			return (hydra, fontSamples)

		while f.tell()<fsize:
			chunkList = ReadRiffChunk(f)
			start_list = f.tell()
			end_list = start_list + chunkList[1]
			if chunkList[0]=='pdta':
				while f.tell()<end_list:
					chunk = ReadRiffChunk(f)
					if not HandleChunk(f, hydra, chunk):
						f.seek(chunk[1],1)

			elif chunkList[0]=='sdta':
				while f.tell()<end_list:
					chunk = ReadRiffChunk(f)
					if chunk[0]=='smpl':
						s16samples=f.read(chunk[1]) 
						fontSamples=S16ToF32(s16samples)
					else:
						f.seek(chunk[1],1)
			else:
				f.seek(chunkList[1], 1)

	return (hydra, fontSamples) 



#sf2= LoadSF2('florestan-subset.sf2')	
