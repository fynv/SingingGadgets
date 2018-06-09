#include <Python.h>
#include <WavBuf.h>

#define PI 3.14159265359f

PyObject* GeneratePureSin(PyObject *self, PyObject *args)
{
	float freq = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 0));
	float fduration = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	float sampleRate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));

	float fNumOfSamples = fduration*sampleRate*0.001f;
	ssize_t len = (ssize_t)ceilf(fNumOfSamples);
	float sampleFreq = freq / sampleRate;

	PyWavBuf res;
	res.SetSampleRate(sampleRate);
	res.SetNumChannels(1);
	res.Allocate(len);

	float* ptr;
	res.GetDataPtrAndLen(ptr, len);

	ssize_t j;

	float wave = 1.0f;
	float Dwave = 0.0f;
	float a = powf(2.0f * PI*sampleFreq, 2.0f);

	for (j = 0; j<len; j++)
	{
		float amplitude = sinf(PI*(float)j / (float)len);

		ptr[j] = amplitude*wave;

		float DDwave = -a*wave;
		Dwave += DDwave;
		wave += Dwave;
	}

	return res.pyWavBuf;
}

PyObject* GenerateSquare(PyObject *self, PyObject *args)
{
	float freq = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 0));
	float fduration = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	float sampleRate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));

	float fNumOfSamples = fduration*sampleRate*0.001f;
	ssize_t len = (ssize_t)ceilf(fNumOfSamples);
	float sampleFreq = freq / sampleRate;

	PyWavBuf res;
	res.SetSampleRate(sampleRate);
	res.SetNumChannels(1);
	res.Allocate(len);

	float* ptr;
	res.GetDataPtrAndLen(ptr, len);

	ssize_t j;

	for (j = 0; j<len; j++)
	{
		float x = sampleFreq*j;
		x = x - floor(x);
		float wave = x > 0.5f ? -1.0f : 1.0f;
		ptr[j] = wave;
	}

	return res.pyWavBuf;
}

PyObject* GenerateTriangle(PyObject *self, PyObject *args)
{
	float freq = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 0));
	float fduration = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	float sampleRate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));

	float fNumOfSamples = fduration*sampleRate*0.001f;
	ssize_t len = (ssize_t)ceilf(fNumOfSamples);
	float sampleFreq = freq / sampleRate;

	PyWavBuf res;
	res.SetSampleRate(sampleRate);
	res.SetNumChannels(1);
	res.Allocate(len);

	float* ptr;
	res.GetDataPtrAndLen(ptr, len);

	ssize_t j;

	for (j = 0; j<len; j++)
	{
		float amplitude = 1.0f - 2.0f*fabsf((float)j / (float)(len - 1) - 0.5f);

		float x = sampleFreq*j;
		x = x - floor(x);

		float wave = x > 0.5f ? (x - 0.75f)*4.0f : (0.25f - x)*4.0f;
		ptr[j] = wave*amplitude;
	}

	return res.pyWavBuf;
}


PyObject* GenerateSawtooth(PyObject *self, PyObject *args)
{
	float freq = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 0));
	float fduration = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	float sampleRate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));

	float fNumOfSamples = fduration*sampleRate*0.001f;
	ssize_t len = (ssize_t)ceilf(fNumOfSamples);
	float sampleFreq = freq / sampleRate;

	PyWavBuf res;
	res.SetSampleRate(sampleRate);
	res.SetNumChannels(1);
	res.Allocate(len);

	float* ptr;
	res.GetDataPtrAndLen(ptr, len);

	ssize_t j;

	for (j = 0; j<len; j++)
	{
		float amplitude = 1.0f - ((float)j / (float)(len - 1));
		float phase = sampleFreq*j;
		float wave = 1.0f - 2.0f*(phase - floor(phase));
		ptr[j] = amplitude*wave;
	}

	return res.pyWavBuf;
}


PyObject* GenerateNaivePiano(PyObject *self, PyObject *args)
{
	float freq = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 0));
	float fduration = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	float sampleRate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));

	float fNumOfSamples = fduration*sampleRate*0.001f;
	ssize_t len = (ssize_t)ceilf(fNumOfSamples);
	float sampleFreq = freq / sampleRate;

	PyWavBuf res;
	res.SetSampleRate(sampleRate);
	res.SetNumChannels(1);
	res.Allocate(len);

	float* ptr;
	res.GetDataPtrAndLen(ptr, len);

	ssize_t j;

	for (j = 0; j<len; j++)
	{
		float x = sampleFreq*j;
		x = x - floor(x);

		float x2 = (float)j / fNumOfSamples;

		float amplitude = 1.0f - powf(x2 - 0.5f, 3.0f)*8.0f;
		float wave = (1.0f + 0.5f*cos(2 * PI*x * 5))*sin(PI*x)* powf(1.0f - 2.0f * x, 3.0f);

		ptr[j] = amplitude*wave;
	}

	return res.pyWavBuf;
}

inline float rand01()
{
	float f = (float)rand() / (float)RAND_MAX;
	if (f < 0.0000001f) f = 0.0000001f;
	if (f > 0.9999999f) f = 0.9999999f;
	return f;
}

PyObject* GenerateBottleBlow(PyObject *self, PyObject *args)
{
	float freq = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 0));
	float fduration = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));
	float sampleRate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));

	float fNumOfSamples = fduration*sampleRate*0.001f;
	ssize_t len = (ssize_t)ceilf(fNumOfSamples);
	float sampleFreq = freq / sampleRate;

	PyWavBuf res;
	res.SetSampleRate(sampleRate);
	res.SetNumChannels(1);
	res.Allocate(len);

	float* ptr;
	res.GetDataPtrAndLen(ptr, len);

	ssize_t j;

	float out = 0.0f;
	float Dout = 0.0f;

	//float FreqCut = 1.0f / 5000.0f;
	float k = 0.02f;
	float FreqCut = k*sampleFreq;
	float a = powf(2 * PI, 2.0f)*sqrtf(powf(FreqCut, 4.0f) + powf(sampleFreq, 4.0f));
	//float b = 2 * PI * powf(2.0f*(sqrtf(powf(FreqCut, 4.0f) + powf(sampleFreq, 4.0f)) - powf(sampleFreq, 2.0f)),0.5f);
	float b = 2 * PI * FreqCut*FreqCut / sampleFreq;

	float ampfac = powf(FreqCut, 1.5f);

	for (j = 0; j < len; j++)
	{
		float x2 = (float)j / fNumOfSamples;
		float amplitude = 1.0f - powf(x2 - 0.5f, 3.0f)*8.0f;

		ptr[j] = amplitude*out*ampfac;

		//float e = randGauss();
		float e = rand01() - 0.5f;
		float DDout = e - b*Dout - a*out;
		Dout += DDout;
		out += Dout;

	}

	return res.pyWavBuf;
}

static PyMethodDef s_Methods[] = {
	{
		"GeneratePureSin",
		GeneratePureSin,
		METH_VARARGS,
		""
	},
	{
		"GenerateSquare",
		GenerateSquare,
		METH_VARARGS,
		""
	},
	{
		"GenerateTriangle",
		GenerateTriangle,
		METH_VARARGS,
		""
	},
	{
		"GenerateSawtooth",
		GenerateSawtooth,
		METH_VARARGS,
		""
	},
	{
		"GenerateNaivePiano",
		GenerateNaivePiano,
		METH_VARARGS,
		""
	},
	{
		"GenerateBottleBlow",
		GenerateBottleBlow,
		METH_VARARGS,
		""
	},
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"SimpleInstruments_module", /* name of module */
	"",          /* module documentation, may be NULL */
	-1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
	s_Methods
};

PyMODINIT_FUNC PyInit_PySimpleInstruments(void) {
	return PyModule_Create(&cModPyDem);
}

