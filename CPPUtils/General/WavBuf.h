#ifndef _WavBuf_h
#define _WavBuf_h

#include <Python.h>

struct PyWavBuf
{
	PyObject* pyWavBuf;
	
	PyWavBuf()
	{
		pyWavBuf = PyDict_New();
		PyDict_SetItemString(pyWavBuf, "sample_rate", PyFloat_FromDouble(44100.0));
		PyDict_SetItemString(pyWavBuf, "num_channels", PyLong_FromLong(1));
		PyObject* dataBuf = PyBytes_FromStringAndSize(nullptr, 0);
		PyDict_SetItemString(pyWavBuf, "data", dataBuf);
		PyDict_SetItemString(pyWavBuf, "align_pos", PyLong_FromLong(0));
		PyDict_SetItemString(pyWavBuf, "volume", PyFloat_FromDouble(1.0));
		PyDict_SetItemString(pyWavBuf, "pan", PyFloat_FromDouble(0.0));
	}
	PyWavBuf(PyObject* in)
	{
		pyWavBuf = in;
	}

	float GetSampleRate() const
	{
		return (float)PyFloat_AsDouble(PyDict_GetItemString(pyWavBuf, "sample_rate"));
	}

	void SetSampleRate(float sampleRate)
	{
		PyDict_SetItemString(pyWavBuf, "sample_rate", PyFloat_FromDouble((double)sampleRate));
	}

	int GetNumChannels() const
	{
		return (int)PyLong_AsLong(PyDict_GetItemString(pyWavBuf, "num_channels"));
	}

	void SetNumChannels(int chn)
	{
		PyDict_SetItemString(pyWavBuf, "num_channels", PyLong_FromLong((long)chn));
	}

	void GetDataPtrAndLen(float*& ptr, ssize_t& len) const
	{
		PyObject* dataBuf = PyDict_GetItemString(pyWavBuf, "data");
		char* p;
		ssize_t size;
		PyBytes_AsStringAndSize(dataBuf, &p, &size);
		ptr = (float*)p;
		len = size / sizeof(float);
	}

	void Allocate(ssize_t len)
	{
		PyObject* dataBuf = PyBytes_FromStringAndSize(nullptr, sizeof(float)*len);
		PyDict_SetItemString(pyWavBuf, "data", dataBuf);
	}

	int GetAlignPos() const
	{
		return (int)PyLong_AsLong(PyDict_GetItemString(pyWavBuf, "align_pos"));
	}

	void SetAlignPos(int align_pos)
	{
		PyDict_SetItemString(pyWavBuf, "align_pos", PyLong_FromLong((long)align_pos));
	}

	float GetVolume() const
	{
		return (float)PyFloat_AsDouble(PyDict_GetItemString(pyWavBuf, "volume"));
	}

	void SetVolume(float volume)
	{
		PyDict_SetItemString(pyWavBuf, "volume", PyFloat_FromDouble((double)volume));
	}

	float GetPan() const
	{
		return (float)PyFloat_AsDouble(PyDict_GetItemString(pyWavBuf, "pan"));
	}

	void SetPan(float pan)
	{
		PyDict_SetItemString(pyWavBuf, "pan", PyFloat_FromDouble((double)pan));
	}

};

#endif

