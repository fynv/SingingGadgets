#ifndef _SF2Synth_h
#define _SF2Synth_h

#define TSF_TRUE 1
#define TSF_FALSE 0
#define TSF_BOOL char
#define TSF_PI 3.14159265358979323846264338327950288
#define TSF_NULL 0

enum { TSF_LOOPMODE_NONE, TSF_LOOPMODE_CONTINUOUS, TSF_LOOPMODE_SUSTAIN };

struct tsf_envelope { float delay, attack, hold, decay, sustain, release, keynumToHold, keynumToDecay; };

struct tsf_region
{
	int loop_mode;
	unsigned int sample_rate;
	unsigned int offset, end, loop_start, loop_end;
	int transpose, tune, pitch_keycenter, pitch_keytrack;
	float attenuation, pan;
	tsf_envelope ampenv, modenv;
	int initialFilterQ, initialFilterFc;
	int modEnvToPitch, modEnvToFilterFc, modLfoToFilterFc, modLfoToVolume;
	float delayModLFO;
	int freqModLFO, modLfoToPitch;
	float delayVibLFO;
	int freqVibLFO, vibLfoToPitch;
};

#include "Synth.h"
#include <Python.h>

PyObject* SynthRegion(const float* input, const tsf_region& region, float key, float vel,
	unsigned numSamples, OutputMode outputmode, float samplerate, float global_gain_db);

#endif

