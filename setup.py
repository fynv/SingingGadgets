from setuptools import setup, Extension
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


VoiceSampler_Src=[
	'CPPUtils/DSPUtil/complex.cpp',
	'CPPUtils/DSPUtil/fft.cpp',
	'SingingGadgets/VoiceSampler/VoiceSampler.cpp',
	'SingingGadgets/VoiceSampler/SentenceGeneratorGeneral.cpp',
	'SingingGadgets/VoiceSampler/SentenceGeneratorCPU.cpp'
]

VoiceSampler_IncludeDirs=[
	'SingingGadgets/VoiceSampler',
	'CPPUtils/General',
	'CPPUtils/DSPUtil'
]

module_VoiceSampler = Extension(
	'SingingGadgets.PyVoiceSampler',
	sources = VoiceSampler_Src,
	include_dirs = VoiceSampler_IncludeDirs)

TrackBuffer_Src=[
	'SingingGadgets/TrackBuffer/ReadWav.cpp',
	'SingingGadgets/TrackBuffer/WriteWav.cpp',
	'SingingGadgets/TrackBuffer/TrackBuffer.cpp',
	'SingingGadgets/TrackBuffer/TrackBuffer_Module.cpp'
]

TrackBuffer_IncludeDirs=[
	'SingingGadgets/TrackBuffer',
	'CPPUtils/General'
]

module_TrackBuffer = Extension(
	'SingingGadgets.PyTrackBuffer',
	sources = TrackBuffer_Src,
	include_dirs = TrackBuffer_IncludeDirs)

setup(
	name = 'SingingGadgets',
	version = '0.0.1',
	description = 'Low level tools for singing synthesis',
	long_description=long_description,
	long_description_content_type='text/markdown',  
	url='https://github.com/fynv/SingingGadgets',
	author='Fei Yang',
	author_email='hyangfeih@gmail.com',
	keywords='synthesizer PSOLA HNM',
	packages=['SingingGadgets'],
	ext_modules=[module_VoiceSampler, module_TrackBuffer],
	project_urls={  
        'Source': 'https://github.com/pypa/sampleproject/',
        'Documentation': 'https://scoredraft.org'
    },
)

