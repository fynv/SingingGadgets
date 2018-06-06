#!/usr/bin/python3

import SingingGadgets as sg
import ScoreDraft as sd
from ScoreDraft.Notes import *

#sd.ListPresetsSF2('florestan-subset.sf2')

def soS(octave=5, duration=48):
	return note(octave,Freqs[8],duration)

seq1 = [do(6,72), ti(5,24), la(5,24), so(5,72)]
seq2 = [la(3,192), BK(144), mi(4,48), so(4,48), do(5,48)]

seq1 = seq1 + [fa(5,96), BL(24), so(5,24), la(5,24), do(6,24)]
seq2 = seq2 + [re(3,192), BK(144), la(3,48), do(4,48),fa(4,48)]

seq1 = seq1 + [ti(5,72), la(5,24), so(5,24), fa(5,72)]
seq2 = seq2 + [so(3,192), BK(144), re(4,48), fa(4,48), ti(4,48)]

seq1 = seq1 + [mi(5,144), BL(48)]
seq2 = seq2 + [do(3,192), BK(144), so(3,48), do(4,48), mi(4,48)]

seq1 = seq1 + [la(5,72), so(5,24), fa(5,24), mi(5,72)]
seq2 = seq2 + [fa(3,192), BK(144), do(4,48), mi(4,48), la(4,48)]

seq1 = seq1 + [re(5,72), mi(5,24), fa(5,24), la(5,72)]
seq2 = seq2 + [re(3,192), BK(144), la(3,48), do(4,48), fa(4,48)]

seq1 = seq1 + [soS(5,72), fa(5,24), mi(5,24), re(5,72)]
seq2 = seq2 + [mi(3,192), BK(144), ti(3,48), re(4,48), soS(4,48)]

seq1 = seq1 + [do(5,144), BL(48)]
seq2 = seq2 + [la(3,192), BK(144), mi(4,48), so(4,48), do(5,48)]

seq1 = seq1 + [re(5,24), la(5,72), la(5,96)]
seq2 = seq2 + [re(3,192), BK(144), la(3,48), do(4,48), fa(4,48)]	

seq1 = seq1 + [BL(96), do(6,24), ti(5,72)]
seq2 = seq2 + [so(3,192), BK(144), re(4,48), fa(4,48), ti(4,48)]	

seq1 = seq1 + [so(5,144), BL(48)]
seq2 = seq2 + [mi(3,192), BK(144), ti(3,48), re(4,48), so(4,48)]

seq1 = seq1 + [la(4,24), fa(5,72), fa(5,96)]
seq2 = seq2 + [re(3,192), BK(144), la(3,48), do(4,48), fa(4,48)]

seq1 = seq1 + [BL(96), la(5,72), so(5,24)]
seq2 = seq2 + [so(3,192), BK(144), re(4,48), fa(4,48), ti(4,48)]	

seq1 = seq1 + [fa(5,24), mi(5,120), BL(48)]
seq2 = seq2 + [do(3,192), BK(144), so(3,48), do(4,48), mi(4,48)]

seq1 = seq1 +  [do(6,72), ti(5,24), la(5,24), so(5,72)]
seq2 = seq2 +  [la(3,192), BK(144), mi(4,48), so(4,48), do(5,48)]

seq1 = seq1 + [fa(5,96), BL(24), so(5,24), la(5,24), do(6,24)]
seq2 = seq2 + [re(3,192), BK(144), la(3,48), do(4,48),fa(4,48)]

seq1 = seq1 + [ti(5,72), la(5,24), so(5,24), fa(5,72)]
seq2 = seq2 + [so(3,192), BK(144), re(4,48), fa(4,48), ti(4,48)]

seq1 = seq1 + [mi(5,144), BL(48)]
seq2 = seq2 + [do(3,192), BK(144), so(3,48), do(4,48), mi(4,48)]

seq1 = seq1 + [la(5,72), so(5,24), fa(5,24), mi(5,72)]
seq2 = seq2 + [fa(3,192), BK(144), do(4,48), mi(4,48), la(4,48)]

seq1 = seq1 + [re(5,72), mi(5,24), fa(5,24), la(5,72)]
seq2 = seq2 + [re(3,192), BK(144), la(3,48), do(4,48), fa(4,48)]

seq1 = seq1 + [soS(5,72), la(5,24), ti(5,24), ti(5,72)]
seq2 = seq2 + [mi(3,192), BK(144), ti(3,48), re(4,48), soS(4,48)]

seq1 = seq1 + [do(6,24), ti(5,24), la(5,96), BL(48)]
seq2 = seq2 + [la(3,192), BK(144), mi(4,48), so(4,48), do(5,48)]

seq1 = seq1 + [la(5,24), so(5,72), la(5,24), so(5,24), fa(5,48)]
seq2 = seq2 + [re(3,192), BK(144), la(3,48), do(4,48), fa(4,48)]

seq1 = seq1 + [BL(96), do(6,24), ti(5,72)]
seq2 = seq2 + [so(3,192), BK(144), re(4,48), fa(4,48), ti(4,48)]	

seq1 = seq1 + [mi(6,144), BL(48)]
seq2 = seq2 + [fa(3,192), BK(144), do(4,48), mi(4,48), la(4,48)]

seq1 = seq1 + [mi(6,24), do(6,72), do(6,96)]
seq2 = seq2 + [re(3,192), BK(144), la(3,48), do(4,48), fa(4,48)]

seq1 = seq1 + [BL(96), ti(5,24), re(6,72)]
seq2 = seq2 + [so(3,192), BK(144), re(4,48), fa(4,48), ti(4,48)]	

seq1 = seq1 + [do(6,192)]
seq2 = seq2 + [do(3,192), BK(180), so(3,180), BK(168), do(4,168), BK(156), mi(4,156), BK(144), so(4,144), BK(132), do(5,132) ]	


track1 = sg.TrackBuffer()
track2 = sg.TrackBuffer()

piano = sd.SF2Instrument('florestan-subset.sf2', 0)

piano.play(track1, seq1, 120, 261.626 * (2**(1/3)))
piano.play(track2, seq2, 120, 261.626 * (2**(1/3)))

track_mix = sg.TrackBuffer()

sg.MixTrackBufferList(track_mix, [track1, track2])
sg.WriteTrackBufferToWav(track_mix,'test.wav')



