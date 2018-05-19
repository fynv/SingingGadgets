#include <Python.h>
#include "FrqData.h"

static PyObject* LoadFrq(PyObject *self, PyObject *args)
{
	const char* fn;
	if (!PyArg_ParseTuple(args, "s", &fn))
		return nullptr;

	FrqData frqData;
	if (!frqData.ReadFromFile(fn))
		return nullptr;

	PyObject* ret = PyDict_New();
	PyDict_SetItemString(ret, "interval", PyLong_FromLong((long)frqData.m_window_interval));
	PyDict_SetItemString(ret, "key", PyFloat_FromDouble(frqData.m_key_freq));

	PyObject* frqList = PyList_New(frqData.size());
	for (unsigned i = 0; i < (unsigned)frqData.size(); i++)
	{
		PyObject* dataPoint = PyTuple_New(2);
		PyTuple_SetItem(dataPoint, 0, PyFloat_FromDouble(frqData[i].freq));
		PyTuple_SetItem(dataPoint, 1, PyFloat_FromDouble(frqData[i].dyn));
		PyList_SetItem(frqList, i, dataPoint);
	}
	PyDict_SetItemString(ret, "data", frqList);

	return ret;
}

static PyMethodDef s_Methods[] = {
	{
		"LoadFrq",
		LoadFrq,
		METH_VARARGS,
		""
	},
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"UTAUUtils_module", /* name of module */
	"",          /* module documentation, may be NULL */
	-1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
	s_Methods
};

PyMODINIT_FUNC PyInit_PyUTAUUtils(void) {

	return PyModule_Create(&cModPyDem);
}
