from .PyWavUtils import S16ToF32
from .PyWavUtils import F32ToS16
from .PyWavUtils import MaxValueF32

from .UTAUUtils import LoadFrq as LoadFrqUTAU
from .UTAUUtils import LoadOtoINIPath as LoadOtoINIPathUTAU
from .UTAUUtils import LoadPrefixMap as LoadPrefixMapUTAU
from .UTAUUtils import LookUpPrefixMap as LookUpPrefixMapUTAU
from .UTAUUtils import VoiceBank as VoiceBankUTAU

from .TrackBuffer import setDefaultNumberOfChannels
from .TrackBuffer import TrackBuffer
from .TrackBuffer import MixTrackBufferList
from .TrackBuffer import WriteTrackBufferToWav
from .TrackBuffer import ReadTrackBufferFromWav

# VoiceSampler
notVowel = 0
preVowel = 1
isVowel = 2

from .VoiceSampler import GenerateSentence
from .VoiceSampler import GenerateSentenceCUDA

from . import VoiceSampler

def DetectFrqVoice(wavF32, interval=256):
	return VoiceSampler.DetectFrq(wavF32,interval)


# Instrument Samplers

# Output Modes
# Two channels with single left/right samples one after another
STEREO_INTERLEAVED = 0
# Two channels with all samples for the left channel first then right
STEREO_UNWEAVED = 1
# A single channel (stereo instruments are mixed into center)
MONO = 2

from .SF2 import LoadSF2
from .SF2Presets import LoadPresets as LoadPresetsSF2
from .SF2Synth import SynthNote as SynthNoteSF2

from .SimpleInstruments import GeneratePureSin
from .SimpleInstruments import GenerateSquare
from .SimpleInstruments import GenerateTriangle
from .SimpleInstruments import GenerateSawtooth
from .SimpleInstruments import GenerateNaivePiano
from .SimpleInstruments import GenerateBottleBlow

from .BasicSamplers import DetectBaseFreq
from .BasicSamplers import InstrumentSingleSample
from .BasicSamplers import InstrumentMultiSample
from .BasicSamplers import PercussionSample
