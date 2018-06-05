#include <Python.h>


static PyObject* S16ToF32(PyObject *self, PyObject *args)
{
	char* p;

	PyObject* o_s16bytes = PyTuple_GetItem(args, 0);
	ssize_t len;
	PyBytes_AsStringAndSize(o_s16bytes, &p, &len);
	len /= sizeof(short);
	short* s16bytes = (short*)p;

	PyObject* o_f32bytes = PyBytes_FromStringAndSize(nullptr, len*sizeof(float));
	PyBytes_AsStringAndSize(o_f32bytes, &p, &len);
	len /= sizeof(float);
	float* f32bytes = (float*)p;

	for (ssize_t i = 0; i < len; i++)
		f32bytes[i] = (float)s16bytes[i] / 32767.0f;

	return o_f32bytes;
}

static PyObject* F32ToS16(PyObject *self, PyObject *args)
{
	char* p;

	PyObject* o_f32bytes = PyTuple_GetItem(args, 0);
	ssize_t len;
	PyBytes_AsStringAndSize(o_f32bytes, &p, &len);
	len /= sizeof(float);
	float* f32bytes = (float*)p;

	float amplitude = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 1));

	PyObject* o_s16bytes = PyBytes_FromStringAndSize(nullptr, len*sizeof(short));
	PyBytes_AsStringAndSize(o_s16bytes, &p, &len);
	len /= sizeof(short);
	short* s16bytes = (short*)p;

	for (ssize_t i = 0; i < len; i++)
		s16bytes[i] = (short)(f32bytes[i] * 32767.0f*amplitude + 0.5f);

	return o_s16bytes;
}

static PyObject* MaxValueF32(PyObject *self, PyObject *args)
{
	char* p;

	PyObject* o_f32bytes = PyTuple_GetItem(args, 0);
	ssize_t len;
	PyBytes_AsStringAndSize(o_f32bytes, &p, &len);
	len /= sizeof(float);
	float* f32bytes = (float*)p;

	float maxV = 0.0f;
	for (ssize_t i = 0; i < len; i++)
	{
		float v = fabsf(f32bytes[i]);
		if (v > maxV) maxV = v;
	}

	return PyFloat_FromDouble((double)maxV);
}

static PyObject* ZeroBuf(PyObject *self, PyObject *args)
{
	char* p;
	PyObject* bytes = PyTuple_GetItem(args, 0);
	ssize_t len;
	PyBytes_AsStringAndSize(bytes, &p, &len);
	memset(p, 0, len);

	return PyLong_FromLong(0);
}

static PyObject* MixF32(PyObject *self, PyObject *args)
{
	PyObject* list = PyTuple_GetItem(args, 0);
	unsigned numBufs = (unsigned)PyList_Size(list);
	unsigned maxLen = 0;
	for (unsigned i = 0; i < numBufs; i++)
	{
		PyObject* o_f32bytes = PyList_GetItem(list, i);
		ssize_t len = PyBytes_Size(o_f32bytes);
		len /= sizeof(float);

		if (maxLen < len)
			maxLen = (unsigned)len;
	}
	char* pOut;
	PyObject* outBuf = PyBytes_FromStringAndSize(nullptr, maxLen*sizeof(float));
	ssize_t outlen;
	PyBytes_AsStringAndSize(outBuf, &pOut, &outlen);
	outlen /= sizeof(float);
	float* f32Out = (float*)pOut;
	memset(f32Out, 0, maxLen*sizeof(float));

	for (unsigned i = 0; i < numBufs; i++)
	{
		char* p;
		PyObject* o_f32bytes = PyList_GetItem(list, i);
		ssize_t len;
		PyBytes_AsStringAndSize(o_f32bytes, &p, &len);
		len /= sizeof(float);
		float* f32bytes = (float*)p;

		for (unsigned j = 0; j < len; j++)
			f32Out[j] += f32bytes[j];
	}

	return outBuf;
}

static PyMethodDef s_Methods[] = {
	{
		"S16ToF32",
		S16ToF32,
		METH_VARARGS,
		""
	},
	{
		"F32ToS16",
		F32ToS16,
		METH_VARARGS,
		""
	},
	{
		"MaxValueF32",
		MaxValueF32,
		METH_VARARGS,
		""
	},
	{
		"ZeroBuf",
		ZeroBuf,
		METH_VARARGS,
		""
	},
	{
		"MixF32",
		MixF32,
		METH_VARARGS,
		""
	},
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"WavUtils_module", /* name of module */
	"",          /* module documentation, may be NULL */
	-1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
	s_Methods
};

PyMODINIT_FUNC PyInit_PyWavUtils(void)
{
	return PyModule_Create(&cModPyDem);
}
