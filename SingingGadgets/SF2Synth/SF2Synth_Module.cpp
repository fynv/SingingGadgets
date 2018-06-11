#include <Python.h>
#include "Synth.h"
#include "SF2Synth.h"

static PyObject* Synth(PyObject *self, PyObject *args)
{
	PyObject* obj_input = PyTuple_GetItem(args, 0);

	ssize_t len_in;
	char* p_in;
	PyBytes_AsStringAndSize(obj_input, &p_in, &len_in);
	len_in /= sizeof(float);
	float* input = (float*)p_in;

	PyObject* obj_outbuf = PyTuple_GetItem(args, 1);

	ssize_t len_out;
	char* p_out;
	PyBytes_AsStringAndSize(obj_outbuf, &p_out, &len_out);
	len_out /= sizeof(float);
	float* outputBuffer = (float*)p_out;

	unsigned numSamples = (unsigned) PyLong_AsUnsignedLong(PyTuple_GetItem(args, 2));

	NoteState ns;
	PyObject* obj_ns = PyTuple_GetItem(args, 3);
	ns.sourceSamplePosition = PyFloat_AsDouble(PyDict_GetItemString(obj_ns, "sourceSamplePosition"));
	PyObject* obj_lowpass = PyDict_GetItemString(obj_ns, "lowPass");
	ns.lowPass.z1 = PyFloat_AsDouble(PyDict_GetItemString(obj_lowpass, "z1"));
	ns.lowPass.z2 = PyFloat_AsDouble(PyDict_GetItemString(obj_lowpass, "z2"));

	SynthCtrl control;
	PyObject* obj_ctrl = PyTuple_GetItem(args, 4);
	control.outputmode = (OutputMode)PyLong_AsUnsignedLong(PyDict_GetItemString(obj_ctrl, "outputmode"));
	control.loopStart = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(obj_ctrl, "loopStart"));
	control.loopEnd = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(obj_ctrl, "loopEnd"));
	control.end = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(obj_ctrl, "end"));
	control.panFactorLeft = (float)PyFloat_AsDouble(PyDict_GetItemString(obj_ctrl, "panFactorLeft"));
	control.panFactorRight = (float)PyFloat_AsDouble(PyDict_GetItemString(obj_ctrl, "panFactorRight"));
	control.effect_sample_block = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(obj_ctrl, "effect_sample_block"));
	PyObject* obj_controlPnts = PyDict_GetItemString(obj_ctrl, "controlPnts");

	unsigned numCtrlPns = (unsigned)PyList_Size(obj_controlPnts);
	for (unsigned i = 0; i < numCtrlPns; i++)
	{
		PyObject* obj_ctrlPnt = PyList_GetItem(obj_controlPnts, i);
		SynthCtrlPnt ctrlPnt;
		ctrlPnt.looping = PyObject_IsTrue(PyDict_GetItemString(obj_ctrlPnt, "looping"))?1:0;
		ctrlPnt.gainMono = (float)PyFloat_AsDouble(PyDict_GetItemString(obj_ctrlPnt, "gainMono"));
		ctrlPnt.pitchRatio = PyFloat_AsDouble(PyDict_GetItemString(obj_ctrlPnt, "pitchRatio"));

		PyObject* obj_lowPass = PyDict_GetItemString(obj_ctrlPnt, "lowPass");
		ctrlPnt.lowPass.active = PyObject_IsTrue(PyDict_GetItemString(obj_lowPass, "active")) ? 1 : 0;
		ctrlPnt.lowPass.a0 = PyFloat_AsDouble(PyDict_GetItemString(obj_lowPass, "a0"));
		ctrlPnt.lowPass.a1 = PyFloat_AsDouble(PyDict_GetItemString(obj_lowPass, "a1"));
		ctrlPnt.lowPass.b1 = PyFloat_AsDouble(PyDict_GetItemString(obj_lowPass, "b1"));
		ctrlPnt.lowPass.b2 = PyFloat_AsDouble(PyDict_GetItemString(obj_lowPass, "b2"));

		control.controlPnts.push_back(ctrlPnt);
	}

	Synth(input, outputBuffer, numSamples, ns, control);

	PyDict_SetItemString(obj_ns, "sourceSamplePosition", PyFloat_FromDouble(ns.sourceSamplePosition));
	PyDict_SetItemString(obj_lowpass, "z1", PyFloat_FromDouble(ns.lowPass.z1));
	PyDict_SetItemString(obj_lowpass, "z2", PyFloat_FromDouble(ns.lowPass.z2));

	return PyLong_FromLong(0);
}

static void unpackEnvelope(PyObject* o_env, tsf_envelope& env)
{
	env.delay = (float)PyFloat_AsDouble(PyDict_GetItemString(o_env, "delay"));
	env.attack = (float)PyFloat_AsDouble(PyDict_GetItemString(o_env, "attack"));
	env.hold = (float)PyFloat_AsDouble(PyDict_GetItemString(o_env, "hold"));
	env.decay = (float)PyFloat_AsDouble(PyDict_GetItemString(o_env, "decay"));
	env.sustain = (float)PyFloat_AsDouble(PyDict_GetItemString(o_env, "sustain"));
	env.release = (float)PyFloat_AsDouble(PyDict_GetItemString(o_env, "release"));
	env.keynumToHold = (float)PyFloat_AsDouble(PyDict_GetItemString(o_env, "keynumToHold"));
	env.keynumToDecay = (float)PyFloat_AsDouble(PyDict_GetItemString(o_env, "keynumToDecay"));
}

static void unpackRegion(PyObject* o_region, tsf_region& region)
{
	region.loop_mode = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "loop_mode"));
	region.sample_rate = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(o_region, "sample_rate"));
	region.offset = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(o_region, "offset"));
	region.end = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(o_region, "end"));
	region.loop_start = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(o_region, "loop_start"));
	region.loop_end = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(o_region, "loop_end"));
	region.transpose = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "transpose"));
	region.tune = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "tune"));
	region.pitch_keycenter = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "pitch_keycenter"));
	region.pitch_keytrack = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "pitch_keytrack"));
	region.attenuation = (float)PyFloat_AsDouble(PyDict_GetItemString(o_region, "attenuation"));
	region.pan = (float)PyFloat_AsDouble(PyDict_GetItemString(o_region, "pan"));
	PyObject* o_ampenv = PyDict_GetItemString(o_region, "ampenv");
	unpackEnvelope(o_ampenv, region.ampenv);
	PyObject* o_modenv = PyDict_GetItemString(o_region, "modenv");
	unpackEnvelope(o_modenv, region.modenv);
	region.initialFilterQ = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "initialFilterQ"));
	region.initialFilterFc = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "initialFilterFc"));
	region.modEnvToPitch = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "modEnvToPitch"));
	region.modEnvToFilterFc = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "modEnvToFilterFc"));
	region.modLfoToFilterFc = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "modLfoToFilterFc"));
	region.modLfoToVolume = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "modLfoToVolume"));
	region.delayModLFO = (float)PyFloat_AsDouble(PyDict_GetItemString(o_region, "delayModLFO"));
	region.freqModLFO = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "freqModLFO"));
	region.modLfoToPitch = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "modLfoToPitch"));
	region.delayVibLFO = (float)PyFloat_AsDouble(PyDict_GetItemString(o_region, "delayVibLFO"));
	region.freqVibLFO = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "freqVibLFO"));
	region.vibLfoToPitch = (int)PyLong_AsLong(PyDict_GetItemString(o_region, "vibLfoToPitch"));
}

static PyObject* SynthRegion(PyObject *self, PyObject *args)
{
	PyObject* obj_input = PyTuple_GetItem(args, 0);

	ssize_t len_in;
	char* p_in;
	PyBytes_AsStringAndSize(obj_input, &p_in, &len_in);
	len_in /= sizeof(float);
	float* input = (float*)p_in;

	tsf_region region;
	PyObject* o_region = PyTuple_GetItem(args, 1);
	unpackRegion(o_region, region);

	float key = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 2));
	float vel = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 3));
	unsigned numSamples = (unsigned)PyLong_AsUnsignedLong(PyTuple_GetItem(args, 4));
	OutputMode outputmode = (OutputMode)PyLong_AsUnsignedLong(PyTuple_GetItem(args, 5));
	float samplerate = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 6));
	float global_gain_db = (float)PyFloat_AsDouble(PyTuple_GetItem(args, 7));

	return SynthRegion(input, region, key, vel, numSamples, outputmode, samplerate, global_gain_db);
}

static PyMethodDef s_Methods[] = {
	{
		"Synth",
		Synth,
		METH_VARARGS,
		""
	},
	{
		"SynthRegion",
		SynthRegion,
		METH_VARARGS,
		""
	},
	{ NULL, NULL, 0, NULL }
};


static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"SF2Synth_module", /* name of module */
	"",          /* module documentation, may be NULL */
	-1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
	s_Methods
};

PyMODINIT_FUNC PyInit_PySF2Synth(void)
{
	return PyModule_Create(&cModPyDem);
}
