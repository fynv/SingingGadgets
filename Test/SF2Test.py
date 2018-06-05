#!/usr/bin/python3

import wave
import SingingGadgets as sg

sf2= sg.LoadSF2('florestan-subset.sf2')
presets = sg.LoadPresetsSF2(sf2)

res=sg.SynthNoteSF2(sf2[1], presets[0], 60, 1.0, 44100*2)
wavS16=sg.F32ToS16(res[1], 1.0)

with wave.open('out.wav', mode='wb') as wavFile:
	wavFile.setnchannels(2)
	wavFile.setsampwidth(2)
	wavFile.setframerate(44100)
	wavFile.setnframes(len(wavS16)//4)
	wavFile.writeframes(wavS16)


