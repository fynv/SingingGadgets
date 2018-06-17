#include <Python.h>
#include <WavBuf.h>
#include "fft.h"
#include <vector>
#include "Deferred.h"

inline float rand01()
{
	float f = (float)rand() / (float)RAND_MAX;
	if (f < 0.0000001f) f = 0.0000001f;
	if (f > 0.9999999f) f = 0.9999999f;
	return f;
}

static Deferred<std::vector<float>> GeneratePinkNoise(float period)
{
	unsigned uLen = (unsigned)ceilf(period);
	unsigned l = 0;
	unsigned fftLen = 1;
	while (fftLen < uLen)
	{
		fftLen <<= 1;
		l++;
	}

	std::vector<DComp> fftData(fftLen);
	memset(&fftData[0], 0, sizeof(DComp)*fftLen);

	for (unsigned i = 1; i < (unsigned)(period) / 2; i++)
	{
		float amplitude = (float)fftLen / sqrtf((float)i);
		float phase = rand01()*(float)(2.0*PI);
		fftData[i].Re = (double)(amplitude*cosf(phase));
		fftData[i].Im = (double)(amplitude*sinf(phase));

		fftData[fftLen - i].Re = fftData[i].Re;
		fftData[fftLen - i].Im = -fftData[i].Im;
	}

	ifft(&fftData[0], l);

	unsigned pnLen = (unsigned)ceilf(period*2.0f);

	Deferred<std::vector<float>> ret;
	ret->resize(pnLen);

	float rate = (float)fftLen / period;
	for (unsigned i = 0; i < pnLen; i++)
	{
		int ipos1 = (int)ceilf(((float)i - 0.5f)*rate);
		if (ipos1 < 0) ipos1 = 0;
		int ipos2 = (int)floorf(((float)i + 0.5f)*rate);
		int count = ipos2 - ipos1 + 1;

		float sum = 0.0f;
		for (int ipos = ipos1; ipos <= ipos2; ipos++)
		{
			int _ipos = ipos;
			while (_ipos >= fftLen) _ipos -= fftLen;
			sum += (float)fftData[_ipos].Re;
		}
		(*ret)[i] = sum / (float)count;
	}
	return ret;
}

PyObject* KarplusStrongGenerate(PyObject *self, PyObject *args)
{
	float freq = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 0));
	float fduration = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	float sampleRate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));
	float cut_freq = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 3));
	float loop_gain = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 4));
	float sustain_gain = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 5));

	float sustain_periods = logf(0.01f) / logf(sustain_gain);
	float fNumOfSamples = fduration*sampleRate*0.001f;

	float period = sampleRate / freq;
	Deferred<std::vector<float>> pinkNoise = GeneratePinkNoise(period);

	float sustainLen = sustain_periods*period;
	ssize_t totalLen = (ssize_t)ceilf(fNumOfSamples + sustainLen);

	PyWavBuf res;
	res.SetSampleRate(sampleRate);
	res.SetNumChannels(1);
	res.Allocate(totalLen);

	float* ptr;
	res.GetDataPtrAndLen(ptr, totalLen);

	cut_freq = cut_freq / 261.626f* freq;
	float a = (float)(1.0 - exp(-2.0*PI* cut_freq / sampleRate));

	unsigned pos = 0;
	while (pos < totalLen)
	{
		float value = 0.0f;
		if ((float)pos < period*2.0f)
			value += (*pinkNoise)[pos] * 0.5f*(cosf(((float)pos - period) / period*PI) + 1.0f);

		if ((float)pos >= period)
		{
			float gain = (float)pos < fNumOfSamples ? loop_gain : sustain_gain;

			float refPos = (float)pos - period;

			int refPos1 = (int)refPos;
			int refPos2 = refPos1 + 1;
			float frac = refPos - (float)refPos1;

			// linear interpolation
			float ref = ptr[refPos1] * (1.0f - frac) + ptr[refPos2] * frac;

			value += gain*a*ref + (1.0f - a)*ptr[pos - 1];
		}


		ptr[pos] = value;
		pos++;
	}

	return res.pyWavBuf;

}

static PyMethodDef s_Methods[] = {
	{
		"KarplusStrongGenerate",
		KarplusStrongGenerate,
		METH_VARARGS,
		""
	},
	{ NULL, NULL, 0, NULL }
};


static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"KarplusStrong_module", /* name of module */
	"",          /* module documentation, may be NULL */
	-1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
	s_Methods
};

PyMODINIT_FUNC PyInit_PyKarplusStrong(void) {
	return PyModule_Create(&cModPyDem);
}

