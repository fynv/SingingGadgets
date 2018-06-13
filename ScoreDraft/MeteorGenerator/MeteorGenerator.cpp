#include <Python.h>
#include <vector>
#include "SubListLookUp.h"

struct VisNote
{
	unsigned instrumentId;
	int pitch;
	float start;
	float end;
};

struct VisBeat
{
	unsigned percId;
	float start;
	float end;
};


struct VisSinging
{
	unsigned singerId;
	std::string lyric;
	std::vector<float> pitch;
	float start;
	float end;
};

class Meteor
{
	std::vector<VisNote> m_notes;
	std::vector<VisBeat> m_beats;
	std::vector<VisSinging> m_singings;

	SubLists m_notes_sublists;
	SubLists m_beats_sublists;
	SubLists m_singing_sublists;

	void _updateSublists()
	{
		m_notes_sublists.SetData(m_notes, 3.0f);
		m_beats_sublists.SetData(m_beats, 3.0f);
		m_singing_sublists.SetData(m_singings, 3.0f);
	}

public:

	void InstEvent(PyObject* o_event)
	{
		VisNote note;
		note.instrumentId = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(o_event, "id"));
		double freq = PyFloat_AsDouble(PyDict_GetItemString(o_event, "freq"));
		note.pitch = (int)floor(log(freq / 261.626)*12.0 / log(2.0) + 0.5);
		note.start = (float)(PyFloat_AsDouble(PyDict_GetItemString(o_event, "offset"))/1000.0);
		note.end = note.start + (float)(PyFloat_AsDouble(PyDict_GetItemString(o_event, "fduration")) / 1000.0);
		m_notes.push_back(note);
	}

	void PercEvent(PyObject* o_event)
	{
		VisBeat beat;
		beat.percId = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(o_event, "id"));
		beat.start = (float)(PyFloat_AsDouble(PyDict_GetItemString(o_event, "offset")) / 1000.0);
		beat.end = beat.start + (float)(PyFloat_AsDouble(PyDict_GetItemString(o_event, "fduration")) / 1000.0);
		m_beats.push_back(beat);
	}

	void SingEvent(PyObject* o_event)
	{
		unsigned id = (unsigned)PyLong_AsUnsignedLong(PyDict_GetItemString(o_event, "id"));
		PyObject* o_syllableList = PyDict_GetItemString(o_event, "syllableList");
		unsigned count = (unsigned)PyList_Size(o_syllableList);
		double pos = PyFloat_AsDouble(PyDict_GetItemString(o_event, "offset")) / 1000.0;
		for (unsigned i = 0; i < count; i++)
		{
			PyObject* o_syllable = PyList_GetItem(o_syllableList, i);

			VisSinging sing;
			sing.singerId = id;
			sing.lyric = _PyUnicode_AsString(PyDict_GetItemString(o_syllable,"lyric"));
			sing.start = (float)pos;

			PyObject* o_ctrlPnts = PyDict_GetItemString(o_syllable, "ctrlPnts");
			unsigned num_ctrlPnts = (unsigned)PyList_Size(o_ctrlPnts);

			double totalLen = 0.0;
			std::vector<double> freqs;
			std::vector<double> durations;
			freqs.resize(num_ctrlPnts);
			durations.resize(num_ctrlPnts);
			for (unsigned j = 0; j < num_ctrlPnts; j++)
			{
				PyObject* o_ctrlPnt = PyList_GetItem(o_ctrlPnts, j);
				double freq = PyFloat_AsDouble(PyTuple_GetItem(o_ctrlPnt, 0));
				double duration = PyFloat_AsDouble(PyTuple_GetItem(o_ctrlPnt, 1))/1000.0;
				freqs[j] = freq;
				durations[j] = duration;
				totalLen += duration;
			}

			sing.end = sing.start + totalLen;
			double pitchPerSec = 50.0;
			double secPerPitchSample = 1.0 / pitchPerSec;

			unsigned pitchLen = (unsigned)ceil(totalLen*pitchPerSec);
			sing.pitch.resize(pitchLen);
			unsigned pitchPos = 0;
			double fPitchPos = 0.0;
			double nextPitchPos = 0.0;			

			for (unsigned j = 0; j < num_ctrlPnts; j++)
			{
				double duration = durations[j];
				double freq1 = freqs[j];
				double freq2 = j < num_ctrlPnts - 1 ? freqs[j + 1] : freq1;
				double thisPitchPos = nextPitchPos;
				nextPitchPos += duration;

				for (; fPitchPos < nextPitchPos && pitchPos<pitchLen; fPitchPos += secPerPitchSample, pitchPos++)
				{
					double k = (fPitchPos - thisPitchPos) / duration;
					sing.pitch[pitchPos] = (float)(freq1*(1.0f - k) + freq2*k);
				}
			}

			std::vector<float> temp;
			temp.resize(pitchLen);
			temp[0] = sing.pitch[0];
			temp[pitchLen - 1] = sing.pitch[pitchLen - 1];

			for (unsigned i = 1; i < pitchLen - 1; i++)
			{
				temp[i] = 0.25f*(sing.pitch[i - 1] + sing.pitch[i + 1]) + 0.5f*sing.pitch[i];
			}

			for (unsigned i = 0; i < pitchLen; i++)
			{
				sing.pitch[i] = logf(temp[i] / 261.626f)*12.0f / logf(2.0f);
			}

			m_singings.push_back(sing);
			pos += totalLen;
		}
	}

	void SaveToFile(const char* filename)
	{
		_updateSublists();
		FILE *fp = fopen(filename, "wb");
		unsigned countNotes = (unsigned)m_notes.size();
		fwrite(&countNotes, sizeof(unsigned), 1, fp);
		fwrite(&m_notes[0], sizeof(VisNote), countNotes, fp);
		m_notes_sublists.SaveToFile(fp);
		unsigned countBeats = (unsigned)m_beats.size();
		fwrite(&countBeats, sizeof(unsigned), 1, fp);
		fwrite(&m_beats[0], sizeof(VisBeat), countBeats, fp);
		m_beats_sublists.SaveToFile(fp);
		unsigned countSinging = (unsigned)m_singings.size();
		fwrite(&countSinging, sizeof(unsigned), 1, fp);
		for (unsigned i = 0; i < countSinging; i++)
		{
			const VisSinging& singing = m_singings[i];
			fwrite(&singing.singerId, sizeof(unsigned), 1, fp);
			unsigned char len = (unsigned char)singing.lyric.length();
			fwrite(&len, 1, 1, fp);
			if (len>0)
				fwrite(singing.lyric.data(), 1, len, fp);
			unsigned count = (unsigned)singing.pitch.size();
			fwrite(&count, sizeof(unsigned), 1, fp);
			fwrite(singing.pitch.data(), sizeof(float), count, fp);
			fwrite(&singing.start, sizeof(float), 2, fp);
		}
		m_singing_sublists.SaveToFile(fp);
		fclose(fp);
	}
};

static PyObject* GenerateMeteor(PyObject *self, PyObject *args)
{
	Meteor meteor;

	PyObject* o_eventList = PyTuple_GetItem(args, 0);
	unsigned count = (unsigned)PyList_Size(o_eventList);

	enum EventType
	{
		Inst,
		Perc,
		Sing
	};

	for (unsigned i = 0; i < count; i++)
	{
		PyObject* o_event = PyList_GetItem(o_eventList, i);
		EventType type = (EventType)PyLong_AsUnsignedLong(PyDict_GetItemString(o_event, "type"));
		switch (type)
		{
		case Inst:
			meteor.InstEvent(o_event);
			break;
		case Perc:
			meteor.PercEvent(o_event);
			break;
		case Sing:
			meteor.SingEvent(o_event);
			break;
		}
	}

	const char* filename = _PyUnicode_AsString(PyTuple_GetItem(args, 1));
	meteor.SaveToFile(filename);

	return PyLong_FromLong(0);
}

static PyMethodDef s_Methods[] = {
	{
		"GenerateMeteor",
		GenerateMeteor,
		METH_VARARGS,
		""
	},
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef cModPyDem =
{
	PyModuleDef_HEAD_INIT,
	"MeteorGenerator_module", /* name of module */
	"",          /* module documentation, may be NULL */
	-1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
	s_Methods
};

PyMODINIT_FUNC PyInit_PyMeteorGenerator(void)
{
	return PyModule_Create(&cModPyDem);
}
