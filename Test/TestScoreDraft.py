#!/usr/bin/python3
import os
import SingingGadgets as sg
import ScoreDraft as sd
from ScoreDraft.Notes import *

track = sg.TrackBuffer(1)	

'''
singer=sd.GePing_UTAU()
seq= [ ("ni", la(4,24), do(5,48), la(4,24), "tiao", re(5,24), mi(5,48), "zhuo", re(5,24), "dan", re(5,16), mi(5,16), re(5,16), do(5,144) ) ]
seq=seq+ [ ("wo", ti(4,24), la(4,48), ti(4,24), "qian", re(5,72), "zhe", mi(5,24), "ma", do(5,48), la(4, 144))]
singer.sing(track,seq, 90, 207.65)
'''

'''
singer=sd.Ayaka_UTAU()
singer.setLyricConverter(sd.CVVCChineseConverter)
#singer.setCZMode()

line= ("zheng", re(5,24), "yue", do(5,48), "li", re(5,24), "cai", mi(5,36), so(5,12), "hua", mi(5,24), la(4,24))
line+=("wu", re(5,24), "you", do(5,48), "hua", re(5,24), "cai", mi(5,24), do(5,12), re(5,12), mi(5,24), BL(24))
seq = [line]

singer.sing(track,seq, 80, 440.0)
'''

'''
seq= [ ('あ', mi(5,48), 'り', so(5,48), 'が', ti(5,48), 'とぅ', do(6,144), ti(5,144), so(5,144))]


singer=sd.Ayaka2_UTAU()
singer.setLyricConverter(sd.JPVCVConverter)

singer.sing(track,seq, 120)
'''

seq = [ ("ma", mi(5,24), "ma", re(5,24), mi(5,48)), BL(24)]
seq +=[ ("do",mi(5,24),"yO", so(5,24), "ri", la(5,24), "mem", mi(5,12),re(5,12), "b3", re(5,72)), BL(24)]
seq +=[ ("dhx",do(5,12), re(5,12), "Od", mi(5,24), "str0l", so(5,24), "h@t", so(5,72)), BL(24)]
seq +=[ ("yO", mi(5,12),ti(5,36)),BL(12),("gAv", la(5,24), "t6",so(5,12), "mE", mi(5,96))]

if os.name=='nt':
	singer = sd.UtauDraft('F:\\workspace\\ScoreDraft_local\\python_test\\UTAUVoice\\CZloid')
else:
	singer = sd.UtauDraft('/home/fei/ScoreDraft/python_test/UTAUVoice/CZloid')
	
singer.setLyricConverter(sd.VCCVEnglishConverter)
singer.setCZMode()
singer.sing(track,seq, 100)

sg.WriteTrackBufferToWav(track,'test.wav')

