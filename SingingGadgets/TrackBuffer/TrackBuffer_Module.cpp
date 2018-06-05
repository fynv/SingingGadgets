#include <Python.h>
#include "TrackBuffer.h"
#include "WavBuf.h"
#include "WriteWav.h"
#include "ReadWav.h"

#ifndef max
#define max(a,b)            (((a) > (b)) ? (a) : (b))
#endif

#ifndef min
#define min(a,b)            (((a) < (b)) ? (a) : (b))
#endif

void WriteToWav(TrackBuffer& track, const char* fileName)
{
	unsigned numSamples = track.NumberOfSamples();
	unsigned chn = track.NumberOfChannels();
	unsigned sampleRate = track.Rate();
	float volume = track.AbsoluteVolume();
	float pan = track.Pan();

	WriteWav writer;
	writer.OpenFile(fileName);
	writer.WriteHeader(sampleRate, numSamples, chn);

	unsigned localBufferSize = track.GetLocalBufferSize();
	float *buffer = new float[localBufferSize*chn];
	unsigned pos = 0;
	while (numSamples > 0)
	{
		unsigned writeCount = min(numSamples, localBufferSize);
		track.GetSamples(pos, writeCount, buffer);
		writer.WriteSamples(buffer, writeCount, volume, pan);
		numSamples -= writeCount;
		pos += writeCount;
	}

	delete[] buffer;
}

void ReadFromWav(TrackBuffer& track, const char* fileName)
{
	unsigned numSamples;
	unsigned chn;
	unsigned sampleRate;

	ReadWav reader;
	reader.OpenFile(fileName);
	reader.ReadHeader(sampleRate, numSamples, chn);

	unsigned localBufferSize = track.GetLocalBufferSize();

	WavBuffer buf;
	buf.m_sampleRate = (float)sampleRate;
	buf.Allocate(chn, localBufferSize);

	while (numSamples > 0)
	{
		unsigned readCount = min(numSamples, localBufferSize);
		float maxv;
		reader.ReadSamples(buf.m_data, readCount, maxv);
		buf.m_sampleNum = readCount;
		track.WriteBlend(buf);
		track.MoveCursor((float)readCount / (float)track.Rate()*1000.0f);
		numSamples -= readCount;
	}
}

typedef std::vector<TrackBuffer_deferred> TrackBufferMap;
TrackBufferMap s_TrackBufferMap;

static void ConvertWavBuf(const PyWavBuf& in, WavBuffer& out)
{
	out.m_sampleRate = in.GetSampleRate();
	out.m_channelNum = in.GetNumChannels();
	in.GetDataPtrAndLen(out.m_data, *(ssize_t*)(&out.m_sampleNum));
	out.m_sampleNum /= out.m_channelNum;
	out.m_alignPos = in.GetAlignPos();
	out.m_volume = in.GetVolume();
	out.m_pan = in.GetPan();
}


static PyObject* InitTrackBuffer(PyObject *self, PyObject *args)
{
	unsigned chn;
	if (!PyArg_ParseTuple(args, "I", &chn))
		return NULL;

	TrackBuffer_deferred buffer(44100, chn);
	unsigned id = (unsigned)s_TrackBufferMap.size();
	s_TrackBufferMap.push_back(buffer);
	return PyLong_FromUnsignedLong((unsigned long)(id));
}


static PyObject* DelTrackBuffer(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	if (!PyArg_ParseTuple(args, "I", &BufferId))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	buffer.Abondon();

	return PyLong_FromLong(0);
}

static PyObject* TrackBufferSetVolume(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	float volume;
	if (!PyArg_ParseTuple(args, "If", &BufferId, &volume))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	buffer->SetVolume(volume);

	return PyLong_FromLong(0);
}


static PyObject* TrackBufferGetVolume(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	if (!PyArg_ParseTuple(args, "I", &BufferId))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	return PyFloat_FromDouble((double)buffer->Volume());
}


static PyObject* TrackBufferSetPan(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	float pan;
	if (!PyArg_ParseTuple(args, "If", &BufferId, &pan))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	buffer->SetPan(pan);

	return PyLong_FromLong(0);
}


static PyObject* TrackBufferGetPan(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	if (!PyArg_ParseTuple(args, "I", &BufferId))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	return PyFloat_FromDouble((double)buffer->Pan());
}

static PyObject* TrackBufferGetNumberOfSamples(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	if (!PyArg_ParseTuple(args, "I", &BufferId))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	return PyLong_FromLong((long)buffer->NumberOfSamples());
}

static PyObject* TrackBufferGetNumberOfChannels(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	if (!PyArg_ParseTuple(args, "I", &BufferId))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	return PyLong_FromLong((long)buffer->NumberOfChannels());
}

static PyObject* TrackBufferGetAlignPos(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	if (!PyArg_ParseTuple(args, "I", &BufferId))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	return PyLong_FromLong((long)buffer->AlignPos());
}

static PyObject* TrackBufferGetCursor(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	if (!PyArg_ParseTuple(args, "I", &BufferId))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	return PyFloat_FromDouble((double)buffer->GetCursor());
}

static PyObject* TrackBufferSetCursor(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	float cursor;
	if (!PyArg_ParseTuple(args, "If", &BufferId, &cursor))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	buffer->SetCursor(cursor);

	return PyLong_FromLong(0);
}

static PyObject* TrackBufferMoveCursor(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	float cursor_delta;
	if (!PyArg_ParseTuple(args, "If", &BufferId, &cursor_delta))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	buffer->MoveCursor(cursor_delta);

	return PyLong_FromLong(0);
}

static PyObject* MixTrackBufferList(PyObject *self, PyObject *args)
{
	unsigned TargetTrackBufferId = (unsigned)PyLong_AsUnsignedLong(PyTuple_GetItem(args, 0));
	PyObject *list = PyTuple_GetItem(args, 1);

	TrackBuffer_deferred targetBuffer = s_TrackBufferMap[TargetTrackBufferId];  

	size_t bufferCount = PyList_Size(list);
	TrackBuffer_deferred* bufferList = new TrackBuffer_deferred[bufferCount];
	for (size_t i = 0; i < bufferCount; i++)
	{
		unsigned long listId = PyLong_AsUnsignedLong(PyList_GetItem(list, i));
		bufferList[i] = s_TrackBufferMap[listId];  
	}

	targetBuffer->CombineTracks((unsigned)bufferCount, bufferList);
	delete[] bufferList;

	return PyLong_FromUnsignedLong(0);
}


static PyObject* WriteTrackBufferToWav(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	const char* fn;
	if (!PyArg_ParseTuple(args, "Is", &BufferId, &fn))
		return NULL;

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	WriteToWav(*buffer, fn);

	return PyLong_FromUnsignedLong(0);
}

static PyObject* ReadTrackBufferFromWav(PyObject *self, PyObject *args)
{
	unsigned BufferId;
	const char* fn;
	if (!PyArg_ParseTuple(args, "Is", &BufferId, &fn))
		return NULL;
	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];
	ReadFromWav(*buffer, fn);

	return PyLong_FromUnsignedLong(0);
}

static PyObject* TrackBufferWriteBlend(PyObject *self, PyObject *args)
{
	unsigned BufferId = (unsigned)PyLong_AsUnsignedLong(PyTuple_GetItem(args, 0));
	PyWavBuf pyWavBuf;
	pyWavBuf.pyWavBuf = PyTuple_GetItem(args, 1);

	TrackBuffer_deferred buffer = s_TrackBufferMap[BufferId];

	WavBuffer wavBuf;
	ConvertWavBuf(pyWavBuf, wavBuf);
	buffer->WriteBlend(wavBuf);

	return PyLong_FromUnsignedLong(0);
}

static PyMethodDef s_Methods[] = {
	{
		"InitTrackBuffer",
		InitTrackBuffer,
		METH_VARARGS,
		""
	},
	{
		"DelTrackBuffer",
		DelTrackBuffer,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferSetVolume",
		TrackBufferSetVolume,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferGetVolume",
		TrackBufferGetVolume,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferSetPan",
		TrackBufferSetPan,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferGetPan",
		TrackBufferGetPan,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferGetNumberOfSamples",
		TrackBufferGetNumberOfSamples,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferGetNumberOfChannels",
		TrackBufferGetNumberOfChannels,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferGetAlignPos",
		TrackBufferGetAlignPos,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferGetCursor",
		TrackBufferGetCursor,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferSetCursor",
		TrackBufferSetCursor,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferMoveCursor",
		TrackBufferMoveCursor,
		METH_VARARGS,
		""
	},
	{
		"MixTrackBufferList",
		MixTrackBufferList,
		METH_VARARGS,
		""
	},
	{
		"WriteTrackBufferToWav",
		WriteTrackBufferToWav,
		METH_VARARGS,
		""
	},
	{
		"ReadTrackBufferFromWav",
		ReadTrackBufferFromWav,
		METH_VARARGS,
		""
	},
	{
		"TrackBufferWriteBlend",
		TrackBufferWriteBlend,
		METH_VARARGS,
		""
	},
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"TrackBuffer_module", /* name of module */
	"",          /* module documentation, may be NULL */
	-1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
	s_Methods
};

PyMODINIT_FUNC PyInit_PyTrackBuffer(void) {
	return PyModule_Create(&cModPyDem);
}
