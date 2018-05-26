#ifndef _TrackBuffer_h
#define _TrackBuffer_h

#include "stdio.h"
#include "Deferred.h"
#include <vector>

inline void CalcPan(float pan, float& l, float& r)
{
	if (pan == 0.0f) return;
	else if (pan < 0.0f)
	{
		pan = -pan;
		float ll = l;
		float rl = r*pan;
		float rr = r*(1.0f - pan);
		l = ll + rl;
		r = rr;
	}
	else
	{
		float ll = l*(1.0f - pan);
		float lr = l*pan;
		float rr = r;
		l = ll;
		r = lr + rr;
	}
}

class WavBuffer
{
	std::vector<float> _data;
public:
	WavBuffer()
	{
		m_sampleRate = 44100.0f;
		m_channelNum = 1;
		m_sampleNum = 0;
		m_data = nullptr;

		m_alignPos = 0;
		m_volume = 1.0f;
		m_pan = 0.0f;
	}
	void Allocate(unsigned channelNum, size_t sampleNum)
	{
		m_channelNum = channelNum;
		m_sampleNum = sampleNum;
		_data.resize(sampleNum * channelNum);
		m_data = &_data[0];
	}

	float m_sampleRate;
	unsigned m_channelNum;
	size_t m_sampleNum;
	float* m_data;
	unsigned m_alignPos;
	float m_volume;
	float m_pan;
};


class TrackBuffer;
class TrackBuffer_deferred : public Deferred<TrackBuffer>
{
public:
	TrackBuffer_deferred();
	TrackBuffer_deferred(const TrackBuffer_deferred & in);
	TrackBuffer_deferred(unsigned rate, unsigned chn = 1);
};


class TrackBuffer
{
public:
	TrackBuffer(unsigned rate = 44100, unsigned chn = 1);
	~TrackBuffer();

	unsigned Rate() const { return m_rate; }
	void SetRate(unsigned rate) { m_rate = rate; }

	unsigned NumberOfChannels() const { return m_chn; }

	unsigned NumberOfSamples()
	{
		return m_length;
	}
	unsigned AlignPos()
	{
		return m_alignPos;
	}

	float Volume() const  { return m_volume; }
	float AbsoluteVolume()
	{
		float maxValue = MaxValue();
		return maxValue>0.0f ? m_volume / maxValue : 1.0f;
	}
	void SetVolume(float vol) { m_volume = vol; }

	float Pan() const { return m_pan; }
	void SetPan(float pan) { m_pan = pan; }

	float GetCursor();
	void SetCursor(float fpos);
	void MoveCursor(float delta);

	void SeekToCursor();
	void WriteBlend(const WavBuffer& wavBuf);

	void Sample(unsigned index, float* sample);
	float MaxValue();

	void GetSamples(unsigned startIndex, unsigned length, float* buffer);

	bool CombineTracks(unsigned num, TrackBuffer_deferred* tracks);

	unsigned GetLocalBufferSize();

private:
	FILE *m_fp;

	unsigned m_rate;
	unsigned m_chn;

	float m_volume;
	float m_pan;

	float *m_localBuffer;
	unsigned m_localBufferPos;

	unsigned m_length;
	unsigned m_alignPos;

	float m_cursor;

	inline float _ms2sample(float ms)
	{
		return ms*0.001f*m_rate;
	}

	void _writeSamples(unsigned count, const float* samples, unsigned alignPos);
	void _seek(unsigned upos);
};

#endif
