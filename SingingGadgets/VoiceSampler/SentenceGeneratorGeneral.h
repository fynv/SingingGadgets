#ifndef __SentenceGeneratorGeneral_h
#define __SentenceGeneratorGeneral_h

#include "VoiceUtil.h"
using namespace VoiceUtil;

void RegulateSource(const float* srcData, unsigned len, Buffer& dstBuf);
void PreprocessFreqMap(const SentenceDescriptor* desc, unsigned outBufLen, float* freqMap, std::vector<unsigned>& bounds);

#endif

