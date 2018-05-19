#include <Python.h>
#include <WavBuf.h>
#include "SentenceDescriptor.h"
#include "SentenceGeneratorCPU.h"
#include <math.h>

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

static PyObject* GenerateSentence(PyObject *self, PyObject *args)
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
	GenerateSentenceCPU(sentence, ptr, (unsigned)len);

	return res.pyWavBuf;
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
		"GenerateSentence",
		GenerateSentence,
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

PyMODINIT_FUNC PyInit_PyVoiceSampler(void) {
	
	return PyModule_Create(&cModPyDem);
}
