from .UtauDraft import GetVoiceBank as GetVoiceBankUTAU
from .UtauDraft import UtauDraft
from .CVVCChineseConverter import CVVCChineseConverter
from .XiaYYConverter import XiaYYConverter
from .JPVCVConverter import JPVCVConverter
from .TsuroVCVConverter import TsuroVCVConverter
from .TTEnglishConverter import TTEnglishConverter
from .VCCVEnglishConverter import VCCVEnglishConverter

from .SF2Instrument import ListPresets as ListPresetsSF2
from .SF2Instrument import SF2Instrument

import os
import numbers

UTAU_VB_ROOT='UTAUVoice'
UTAU_VB_SUFFIX='_UTAU'
if os.path.isdir(UTAU_VB_ROOT):
	for item in os.listdir(UTAU_VB_ROOT):
		if os.path.isdir(UTAU_VB_ROOT+'/'+item):
			definition="""
def """+item+UTAU_VB_SUFFIX+"""(useCuda=True):
	return UtauDraft('"""+UTAU_VB_ROOT+"""/"""+item+"""',useCuda)
"""
			exec(definition)

def isNumber(x):
	return isinstance(x, numbers.Number)

def TellDuration(seq):
	duration = 0
	for item in seq:
		if type(item)== tuple:
			_item = item[0]	
			if type(_item) == str: # singing
				tupleSize=len(item)
				j=0
				while j<tupleSize:
					j+=1  # by-pass lyric
					_item=item[j]
					if type(_item) == tuple: # singing note
						while j<tupleSize:
							_item = item[j]
							if type(_item) != tuple:
								break
							numCtrlPnt= len(_item)//2
							for k in range(numCtrlPnt):
								duration+=_item[k*2+1]
							j+=1
					elif isNumber(_item): # singing rap
						duration += item[j]
						j+=3
			elif isNumber(_item): # note
				duration += item[1]
	return duration

