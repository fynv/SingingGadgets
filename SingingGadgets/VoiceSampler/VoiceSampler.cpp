#include <Python.h>
#include <WavBuf.h>
#include "SentenceDescriptor.h"
#include "SentenceGeneratorCPU.h"
#ifdef HAVE_CUDA
#include "SentenceGeneratorCUDA.h"
#include <cuda_runtime.h>
#endif
#include <math.h>

#include "VoiceUtil.h"
#include "FrequencyDetection.h"
using namespace VoiceUtil;

static bool s_have_cuda = false;

static SentenceDescriptor_Deferred CreateSentenceDescriptor(PyObject *input)
{
	SentenceDescriptor_Deferred sentence;

	PyObject* o_pieces = PyDict_GetItemString(input, "pieces");
	ssize_t num_pieces = PyList_Size(o_pieces);
	std::vector<Piece>& pieces = sentence->pieces;
	for (ssize_t i = 0; i < num_pieces; i++)
	{
		Piece piece;
		PyObject* o_piece = PyList_GetItem(o_pieces, i);

		PyObject* o_src = PyDict_GetItemString(o_piece, "src");
		Source& src = piece.src;
		{
			PyObject* o_wav = PyDict_GetItemString(o_src, "wav");
			Wav& wav = src.wav;

			char* p;  ssize_t len;
			PyBytes_AsStringAndSize(o_wav, &p, &len);
			len /= sizeof(float);
			wav.buf = (float*)p;
			wav.len = (unsigned)len;

			PyObject* o_frq = PyDict_GetItemString(o_src, "frq");
			FrqData& frq = src.frq;

			frq.interval = (int)PyLong_AsLong(PyDict_GetItemString(o_frq, "interval"));
			frq.key = PyFloat_AsDouble(PyDict_GetItemString(o_frq, "key"));

			PyObject* o_data = PyDict_GetItemString(o_frq, "data");
			ssize_t num_datapnts = PyList_Size(o_data);
			std::vector<FrqDataPoint>& data = frq.data;
			for (ssize_t j = 0; j < num_datapnts; j++)
			{
				FrqDataPoint datapnt;
				PyObject* o_datapnt = PyList_GetItem(o_data, j);
				datapnt.freq = PyFloat_AsDouble(PyTuple_GetItem(o_datapnt, 0));
				datapnt.dyn = PyFloat_AsDouble(PyTuple_GetItem(o_datapnt, 1));
				data.push_back(datapnt);
			}
		}		

		PyObject* o_map = PyDict_GetItemString(o_piece, "map");
		ssize_t num_ctrlpnts = PyList_Size(o_map);
		std::vector<SourceMapCtrlPnt>& srcMap = piece.srcMap;
		for (ssize_t j = 0; j < num_ctrlpnts; j++)
		{
			SourceMapCtrlPnt ctrlpnt;
			PyObject* o_ctrlpnt = PyList_GetItem(o_map, j);
			ctrlpnt.srcPos = (float)PyFloat_AsDouble(PyTuple_GetItem(o_ctrlpnt, 0));
			ctrlpnt.dstPos = (float)PyFloat_AsDouble(PyTuple_GetItem(o_ctrlpnt, 1));
			if (j < num_ctrlpnts - 1)
			{
				ctrlpnt.isVowel = (int)PyLong_AsLong(PyTuple_GetItem(o_ctrlpnt, 2));
			}
			else
			{
				ctrlpnt.isVowel = 0;
			}
			srcMap.push_back(ctrlpnt);
		}
		pieces.push_back(piece);
	}

	PyObject* o_piece_map = PyDict_GetItemString(input, "piece_map");
	ssize_t num_ctrlpnts = PyList_Size(o_piece_map);
	std::vector<GeneralCtrlPnt>& piece_map = sentence->piece_map;
	for (ssize_t i = 0; i < num_ctrlpnts; i++)
	{
		GeneralCtrlPnt ctrlpnt;
		PyObject* o_ctrlpnt = PyList_GetItem(o_piece_map, i);
		ctrlpnt.value = (float)PyFloat_AsDouble(PyTuple_GetItem(o_ctrlpnt, 0));
		ctrlpnt.dstPos = (float)PyFloat_AsDouble(PyTuple_GetItem(o_ctrlpnt, 1));
		piece_map.push_back(ctrlpnt);
	}

	PyObject* o_freq_map = PyDict_GetItemString(input, "freq_map");
	num_ctrlpnts = PyList_Size(o_freq_map);
	std::vector<GeneralCtrlPnt>& freq_map = sentence->freq_map;
	for (ssize_t i = 0; i < num_ctrlpnts; i++)
	{
		GeneralCtrlPnt ctrlpnt;
		PyObject* o_ctrlpnt = PyList_GetItem(o_freq_map, i);
		ctrlpnt.value = (float)PyFloat_AsDouble(PyTuple_GetItem(o_ctrlpnt, 0));
		ctrlpnt.dstPos = (float)PyFloat_AsDouble(PyTuple_GetItem(o_ctrlpnt, 1));
		freq_map.push_back(ctrlpnt);
	}

	PyObject* o_volume_map = PyDict_GetItemString(input, "volume_map");
	num_ctrlpnts = PyList_Size(o_volume_map);
	std::vector<GeneralCtrlPnt>& volume_map = sentence->volume_map;
	for (ssize_t i = 0; i < num_ctrlpnts; i++)
	{
		GeneralCtrlPnt ctrlpnt;
		PyObject* o_ctrlpnt = PyList_GetItem(o_volume_map, i);
		ctrlpnt.value = (float)PyFloat_AsDouble(PyTuple_GetItem(o_ctrlpnt, 0));
		ctrlpnt.dstPos = (float)PyFloat_AsDouble(PyTuple_GetItem(o_ctrlpnt, 1));
		volume_map.push_back(ctrlpnt);
	}

	return sentence;
}

static PyObject* GenerateSentenceX(PyObject *self, PyObject *args, bool cuda)
{
	SentenceDescriptor_Deferred sentence =
		CreateSentenceDescriptor(PyTuple_GetItem(args, 0));

	std::vector<Piece>& pieces = sentence->pieces;
	float falignPos = -pieces[0].srcMap[0].dstPos;

	for (size_t i = 0; i < pieces.size(); i++)
	{
		Piece& piece = pieces[i];
		std::vector<SourceMapCtrlPnt>& srcMap = piece.srcMap;
		for (size_t j = 0; j < srcMap.size(); j++)
		{
			srcMap[j].dstPos += falignPos;
		}
	}

	std::vector<GeneralCtrlPnt>& piece_map = sentence->piece_map;
	std::vector<GeneralCtrlPnt>& freq_map = sentence->freq_map;
	std::vector<GeneralCtrlPnt>& volume_map = sentence->volume_map;

	for (size_t i = 0; i < piece_map.size(); i++)
		piece_map[i].dstPos += falignPos;

	for (size_t i = 0; i < freq_map.size(); i++)
		freq_map[i].dstPos += falignPos;

	for (size_t i = 0; i < volume_map.size(); i++)
		volume_map[i].dstPos += falignPos;

	float flen = freq_map[freq_map.size() - 1].dstPos;

	PyWavBuf res;
	float rate = res.GetSampleRate();
	unsigned alignPos = (unsigned)(falignPos*0.001f*rate + 0.5f);
	res.SetAlignPos(alignPos);

	ssize_t len = (ssize_t)ceilf(flen*0.001f*rate);
	res.Allocate(len);
	
	float* ptr;
	res.GetDataPtrAndLen(ptr, len);	

#ifdef HAVE_CUDA
	if (cuda && s_have_cuda)
		GenerateSentenceCUDA(sentence, ptr, (unsigned)len);
	else
#endif
		GenerateSentenceCPU(sentence, ptr, (unsigned)len);

	return res.pyWavBuf;
}

static PyObject* GenerateSentence(PyObject *self, PyObject *args)
{
	return GenerateSentenceX(self, args, false);
}

static PyObject* GenerateSentenceCUDA(PyObject *self, PyObject *args)
{
	return GenerateSentenceX(self, args, true);
}

static PyObject* HaveCUDA(PyObject *self, PyObject *args)
{
	return s_have_cuda ? Py_True : Py_False;
}

void DetectFreqs(const Buffer& buf, std::vector<float>& frequencies, std::vector<float>& dynamics, unsigned step)
{
	unsigned halfWinLen = 1024;
	float* temp = new float[halfWinLen * 2];

	for (unsigned center = 0; center < buf.m_data.size(); center += step)
	{
		Window win;
		win.CreateFromBuffer(buf, (float)center, (float)halfWinLen);

		for (int i = -(int)halfWinLen; i < (int)halfWinLen; i++)
			temp[i + halfWinLen] = win.GetSample(i);

		float freq;
		float dyn;
		fetchFrequency(halfWinLen * 2, temp, buf.m_sampleRate, freq, dyn);

		frequencies.push_back(freq);
		dynamics.push_back(dyn);
	}

	delete[] temp;

}

static PyObject* DetectFrq(PyObject *self, PyObject *args)
{
	char* p;

	PyObject* o_f32bytes = PyTuple_GetItem(args, 0);
	ssize_t len;
	PyBytes_AsStringAndSize(o_f32bytes, &p, &len);
	len /= sizeof(float);
	float* f32bytes = (float*)p;

	int interval = (int)PyLong_AsLong(PyTuple_GetItem(args, 1));

	Buffer buf;
	buf.m_sampleRate = 44100;
	buf.Allocate(len);
	memcpy(buf.m_data.data(), f32bytes, sizeof(float)*len);

	std::vector<float> frequencies;
	std::vector<float> dynamics;
	DetectFreqs(buf, frequencies, dynamics, interval);

	float ave = 0.0f;
	float count = 0.0f;
	for (unsigned i = 0; i < (unsigned)frequencies.size(); i++)
	{
		if (frequencies[i] > 55.0f)
		{
			count += 1.0f;
			ave += frequencies[i];
		}
	}
	ave = ave / count;

	PyObject *ret = PyDict_New();
	PyDict_SetItemString(ret, "interval", PyLong_FromLong((long)interval));
	PyDict_SetItemString(ret, "key", PyFloat_FromDouble((double)ave));
	PyObject* data = PyList_New(frequencies.size());
	for (unsigned i = 0; i < (unsigned)frequencies.size(); i++)
	{
		PyObject* tuple = PyTuple_New(2);
		PyTuple_SetItem(tuple, 0, PyFloat_FromDouble((double)frequencies[i]));
		PyTuple_SetItem(tuple, 1, PyFloat_FromDouble((double)dynamics[i]));
		PyList_SetItem(data, i, tuple);
	}

	PyDict_SetItemString(ret, "data", data);

	return ret;
}

static PyMethodDef s_Methods[] = {
	{
		"GenerateSentence",
		GenerateSentence,
		METH_VARARGS,
		""
	},
	{
		"GenerateSentenceCUDA",
		GenerateSentenceCUDA,
		METH_VARARGS,
		""
	},
	{
		"HaveCUDA",
		HaveCUDA,
		METH_VARARGS,
		""
	},
	{
		"DetectFrq",
		DetectFrq,
		METH_VARARGS,
		""
	},
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"SingingGadgets_module", /* name of module */
	"",          /* module documentation, may be NULL */
	-1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
	s_Methods
};

PyMODINIT_FUNC PyInit_PyVoiceSampler(void) 
{
#if HAVE_CUDA
	int count;
	cudaGetDeviceCount(&count);
	if (count > 0 && cudaGetLastError() == 0)
	{
		cudaFree(nullptr);
		if (cudaGetLastError() == 0) s_have_cuda = true;
	}
#endif
	return PyModule_Create(&cModPyDem);
}
