
set(PYTHON
__init__.py

Singer.py
UtauDraft.py
Notes.py
RapChinese.py
CVVCChineseConverter.py
XiaYYConverter.py
JPVCVConverter.py
TsuroVCVConverter.py
TTEnglishConverter.py
VCCVEnglishConverter.py
TTLyricSet.data
VCCVLyricSet.data

Instrument.py
SimpleInstruments.py
InstrumentSampler.py
SF2Instrument.py
KarplusStrongInstrument.py

Percussion.py
PercussionSampler.py

Document.py
Meteor.py

Catalog.py
)

install(FILES ${PYTHON} DESTINATION ScoreDraft)
