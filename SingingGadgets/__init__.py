from .UTAUUtils import LoadFrq as LoadFrqUTAU
from .UTAUUtils import LoadOtoINIPath as LoadOtoINIPathUTAU
from .UTAUUtils import LoadPrefixMap as LoadPrefixMapUTAU
from .UTAUUtils import LookUpPrefixMap as LookUpPrefixMapUTAU
from .UTAUUtils import VoiceBank as VoiceBankUTAU

from .VoiceSampler import S16ToF32 as S16ToF32Voice
from .VoiceSampler import F32ToS16 as F32ToS16Voice
from .VoiceSampler import MaxValueF32 as MaxValueF32Voice
from .VoiceSampler import GenerateSentence
from .VoiceSampler import GenerateSentenceCUDA

from . import VoiceSampler

def DetectFrqVoice(wavF32, interval=256):
	return VoiceSampler.DetectFrq(wavF32,interval)

notVowel = 0
preVowel = 1
isVowel = 2

from .TrackBuffer import TrackBuffer
from .TrackBuffer import MixTrackBufferList
from .TrackBuffer import WriteTrackBufferToWav
from .TrackBuffer import ReadTrackBufferFromWav
