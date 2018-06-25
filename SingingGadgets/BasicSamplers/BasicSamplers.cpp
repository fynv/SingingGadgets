#include <Python.h>
#include <WavBuf.h>
#include <Sample.h>
#include <vector>
#include <stdio.h>
#include <cstdlib>
#include "FrequencyDetection.h"
#include "InstrumentSingleSampler.h"
#include "InstrumentMultiSampler.h"
#include "PercussionSampler.h"

static void CreateSample(PyObject *input, Sample& sample)
{
	sample.m_wav_length = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(input, "nframes"));
	sample.m_chn = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(input, "nchannels"));

	PyObject* o_frames = PyDict_GetItemString(input, "frames");
	char* p;  ssize_t len;
	PyBytes_AsStringAndSize(o_frames, &p, &len);
	sample.m_wav_samples = (float*)p;
	sample.m_origin_sample_rate = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(input, "framerate"));

	PyObject* o_maxv = PyDict_GetItemString(input, "maxv");
	if (!o_maxv)
	{
		float maxV = 0.0f;
		for (ssize_t i = 0; i < len; i++)
		{
			float v = fabsf(p[i]);
			if (v > maxV) maxV = v;
		}
		sample.m_max_v = maxV;

		PyDict_SetItemString(input, "maxv", PyFloat_FromDouble((double)maxV));
	}
	else
	{
		sample.m_max_v = (float)PyFloat_AsDouble(o_maxv);
	}
}

static float s_DetectBaseFreq(const Sample& sample)
{
	float* localMono = nullptr;
	float* pSamples = nullptr;

	if (sample.m_chn == 1)
	{
		pSamples = sample.m_wav_samples;
	}
	else if (sample.m_chn == 2)
	{
		localMono = new float[sample.m_wav_length];
		pSamples = localMono;
		for (unsigned i = 0; i < sample.m_wav_length; i++)
		{
			localMono[i] = 0.5f*(sample.m_wav_samples[i * 2] + sample.m_wav_samples[i * 2 + 1]);
		}
	}
	Buffer buf;
	buf.m_size = sample.m_wav_length;
	buf.m_data = pSamples;
	float baseFreq = fetchFrequency(buf, sample.m_origin_sample_rate);
	delete[] localMono;

	return baseFreq;
}

static void CreateInstrumentSample(PyObject *input, InstrumentSample& sample)
{
	CreateSample(input, sample);
	PyObject* o_baseFreq = PyDict_GetItemString(input, "basefreq");
	if (!o_baseFreq)
	{
		sample.m_origin_freq = s_DetectBaseFreq(sample);
		PyDict_SetItemString(input, "basefreq", PyFloat_FromDouble((double)sample.m_origin_freq));
	}
	else
	{
		sample.m_origin_freq = (float)PyFloat_AsDouble(PyDict_GetItemString(input, "basefreq"));
	}
}


static PyObject* DetectBaseFreq(PyObject *self, PyObject *args)
{
	PyObject* o_sample = PyTuple_GetItem(args, 0);

	Sample sample;
	CreateSample(o_sample, sample);

	float baseFreq = s_DetectBaseFreq(sample);
	PyDict_SetItemString(o_sample, "basefreq", PyFloat_FromDouble((double)baseFreq));

	return PyLong_FromLong(0);
}

static PyObject* InstrumentSingleSample(PyObject *self, PyObject *args)
{
	PyObject* o_sample = PyTuple_GetItem(args, 0);
	InstrumentSample sample;
	CreateInstrumentSample(o_sample, sample);

	float freq = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	float fduration = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));
	float sampleRate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 3));

	float fNumOfSamples = fduration*sampleRate*0.001f;
	ssize_t len = (ssize_t)ceilf(fNumOfSamples);
	float sampleFreq = freq / sampleRate;

	PyWavBuf res;
	res.SetSampleRate(sampleRate);
	res.SetNumChannels(sample.m_chn);
	res.Allocate(len*sample.m_chn);

	float* ptr;
	res.GetDataPtrAndLen(ptr, len);
	len /= sample.m_chn;

	InstrumentSingleSample(sample, ptr, (unsigned)len, sampleFreq);

	return res.pyWavBuf;
}

static int compareSampleWav(const void* a, const void* b)
{
	InstrumentSample& wavA = *((InstrumentSample*)a);
	InstrumentSample& wavB = *((InstrumentSample*)b);

	float origin_SampleFreqA = wavA.m_origin_freq / (float)wavA.m_origin_sample_rate;
	float origin_SampleFreqB = wavB.m_origin_freq / (float)wavB.m_origin_sample_rate;

	return origin_SampleFreqA > origin_SampleFreqB ? 1 : -1;
}

static PyObject* InstrumentMultiSample(PyObject *self, PyObject *args)
{
	PyObject* sampleList = PyTuple_GetItem(args, 0);
	unsigned num_samples = (unsigned)PyList_Size(sampleList);

	unsigned chn = 0;

	std::vector<InstrumentSample> samples;
	for (unsigned i = 0; i < num_samples; i++)
	{
		PyObject* o_sample = PyList_GetItem(sampleList, i);
		InstrumentSample sample;
		CreateInstrumentSample(o_sample, sample);

		if (i == 0)
			chn = sample.m_chn;
		else
			if (chn != sample.m_chn)
			{
				printf("All samples does not have the same number of channels\n");
				return nullptr;
			}

		samples.push_back(sample);
	}
	std::qsort(samples.data(), samples.size(), sizeof(InstrumentSample), compareSampleWav);

	float freq = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	float fduration = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));
	float sampleRate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 3));

	float fNumOfSamples = fduration*sampleRate*0.001f;
	ssize_t len = (ssize_t)ceilf(fNumOfSamples);
	float sampleFreq = freq / sampleRate;

	PyWavBuf res;
	res.SetSampleRate(sampleRate);
	res.SetNumChannels(chn);
	res.Allocate(len*chn);

	float* ptr;
	res.GetDataPtrAndLen(ptr, len);
	len /= chn;
	
	InstrumentMultiSample(samples, ptr, (unsigned)len, sampleFreq);

	return res.pyWavBuf;
}

static PyObject* PercussionSample(PyObject *self, PyObject *args)
{
	PyObject* o_sample = PyTuple_GetItem(args, 0);
	Sample sample;
	CreateSample(o_sample, sample);
	float fduration = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	float sampleRate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));

	float fNumOfSamples = fduration*sampleRate*0.001f;
	ssize_t len = (ssize_t)ceilf(fNumOfSamples);

	PyWavBuf res;
	res.SetSampleRate(sampleRate);
	res.SetNumChannels(sample.m_chn);
	res.Allocate(len*sample.m_chn);

	float* ptr;
	res.GetDataPtrAndLen(ptr, len);
	len /= sample.m_chn;

	PercussionSample(sample, ptr, (unsigned)len, sampleRate / (float)sample.m_origin_sample_rate);

	return res.pyWavBuf;
}


static PyMethodDef s_Methods[] = {
	{
		"DetectBaseFreq",
		DetectBaseFreq,
		METH_VARARGS,
		""
	},
	{
		"InstrumentSingleSample",
		InstrumentSingleSample,
		METH_VARARGS,
		""
	},
	{
		"InstrumentMultiSample",
		InstrumentMultiSample,
		METH_VARARGS,
		""
	},
	{
		"PercussionSample",
		PercussionSample,
		METH_VARARGS,
		""
	},
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"BasicSamplers_module", /* name of module */
	"",          /* module documentation, may be NULL */
	-1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
	s_Methods
};

PyMODINIT_FUNC PyInit_PyBasicSamplers(void)
{
	return PyModule_Create(&cModPyDem);
}

