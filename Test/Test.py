#!/usr/bin/python3

import wave
import SingingGadgets as sg

def loadWav(file):
	wavS16=bytes()
	with wave.open(file, mode='rb') as wavFile:
		wavS16=wavFile.readframes(wavFile.getnframes())
	return sg.S16ToF32(wavS16)

def saveWav(wavF32, file, amp=1.0):
	wavS16=sg.F32ToS16(wavF32, amp)
	with wave.open(file, mode='wb') as wavFile:
		wavFile.setnchannels(1)
		wavFile.setsampwidth(2)
		wavFile.setframerate(44100)
		wavFile.setnframes(len(wavS16)//2)
		wavFile.writeframes(wavS16)

wav = loadWav('fa.wav')
frq = sg.LoadFrqUTAU('fa_wav.frq')
#frq =  sg.DetectFrqVoice(wav)

src={
	'wav': wav,
	'frq': frq
}

sentence= {
	'pieces': [ 
		{
			'src': src,
			'map': [(24.04, -73.457, sg.notVowel), (97.497, 0.0, sg.preVowel), (177.999, 153.959, sg.isVowel), (362.911, 454.59)]
		},
		{
			'src': src,
			'map': [(24.04, 426.543, sg.notVowel), (97.497, 500.0, sg.preVowel), (177.999, 653.959, sg.isVowel), (362.911, 954.59)]
		},
		{
			'src': src,
			'map': [(24.04, 926.543, sg.notVowel), (97.497, 1000.0, sg.preVowel), (177.999, 1153.959, sg.isVowel), (362.911, 1500.0)]
		}
	],
	'piece_map': [(0, 0), (0, 426.543), (1,454.59), (1,926.543), (2,954.59), (2,1500)],
	'freq_map': [(264.0, 0), (264.0, 500), (264.0*1.125, 500), (264.0*1.125, 1000), (264.0*1.25,1000), (264.0*1.25,1500)],
	'volume_map': [(1.0, 0), (1.0, 1450), (0.0, 1500)]
}

#res=sg.GenerateSentence(sentence)
res=sg.GenerateSentenceCUDA(sentence)

#outData=res['data']
#maxValue=sg.MaxValueF32(outData)
#saveWav(res['data'],'out.wav', 1.0/maxValue)

track = sg.TrackBuffer(1)
track.writeBlend(res)
track.moveCursor(2000)
track.writeBlend(res)
sg.WriteTrackBufferToWav(track,'out.wav')

