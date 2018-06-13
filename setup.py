#!/usr/bin/python3

from setuptools import setup, Extension
from codecs import open
import os
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

extra_compile_args=[]
if os.name != 'nt':
	extra_compile_args = ['-std=c++11']

WavUtils_Src=[
	'SingingGadgets/WavUtils/WavUtils.cpp',	
]

module_WavUtils = Extension(
	'SingingGadgets.PyWavUtils',
	sources = WavUtils_Src,
	extra_compile_args=extra_compile_args)

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
	include_dirs = TrackBuffer_IncludeDirs,
	extra_compile_args=extra_compile_args)

VoiceSampler_Src=[
	'CPPUtils/DSPUtil/complex.cpp',
	'CPPUtils/DSPUtil/fft.cpp',
	'SingingGadgets/VoiceSampler/VoiceSampler.cpp',
	'SingingGadgets/VoiceSampler/SentenceGeneratorGeneral.cpp',
	'SingingGadgets/VoiceSampler/SentenceGeneratorCPU.cpp',
	'SingingGadgets/VoiceSampler/FrequencyDetection.cpp'
]

VoiceSampler_IncludeDirs=[
	'SingingGadgets/VoiceSampler',
	'CPPUtils/General',
	'CPPUtils/DSPUtil'
]

module_VoiceSampler = Extension(
	'SingingGadgets.PyVoiceSampler',
	sources = VoiceSampler_Src,
	include_dirs = VoiceSampler_IncludeDirs,
	extra_compile_args=extra_compile_args)

SF2Synth_Src=[
	'SingingGadgets/SF2Synth/SF2Synth_Module.cpp',
	'SingingGadgets/SF2Synth/SF2Synth.cpp',
	'SingingGadgets/SF2Synth/Synth.cpp']

SF2Synth_IncludeDirs=[
	'SingingGadgets/SF2Synth'
]

module_SF2Synth = Extension(
	'SingingGadgets.PySF2Synth',
	sources = SF2Synth_Src,
	include_dirs = SF2Synth_IncludeDirs,
	extra_compile_args=extra_compile_args)

module_SimpleInstruments = Extension(
	'SingingGadgets.PySimpleInstruments',
	sources = ['SingingGadgets/SimpleInstruments/SimpleInstruments.cpp'],
	include_dirs = ['CPPUtils/General'],
	extra_compile_args=extra_compile_args)

BasicSamplers_Src=[
	'CPPUtils/DSPUtil/complex.cpp',
	'CPPUtils/DSPUtil/fft.cpp',
	'SingingGadgets/BasicSamplers/BasicSamplers.cpp',
	'SingingGadgets/BasicSamplers/PercussionSampler.cpp',
	'SingingGadgets/BasicSamplers/InstrumentSingleSampler.cpp',
	'SingingGadgets/BasicSamplers/InstrumentMultiSampler.cpp',
	'SingingGadgets/BasicSamplers/FrequencyDetection.cpp'
]

BasicSamplers_IncludeDirs=[
	'SingingGadgets/BasicSamplers',
	'CPPUtils/General',
	'CPPUtils/DSPUtil'
]

module_BasicSamplers = Extension(
	'SingingGadgets.PyBasicSamplers',
	sources = BasicSamplers_Src,
	include_dirs = BasicSamplers_IncludeDirs,
	extra_compile_args=extra_compile_args)

MeteorGenerator_Src=[
	'ScoreDraft/MeteorGenerator/MeteorGenerator.cpp',	
]

module_MeteorGenerator = Extension(
	'ScoreDraft.PyMeteorGenerator',
	sources = MeteorGenerator_Src,
	extra_compile_args=extra_compile_args)


setup(
	name = 'SingingGadgets',
	version = '0.0.2',
	description = 'Low level tools for singing synthesis',
	long_description=long_description,
	long_description_content_type='text/markdown',  
	url='https://github.com/fynv/SingingGadgets',
	author='Fei Yang',
	author_email='hyangfeih@gmail.com',
	keywords='synthesizer PSOLA HNM',
	packages=['SingingGadgets','ScoreDraft'],
	package_data={  
        'ScoreDraft': ['TTLyricSet.data', 'VCCVLyricSet.data'],
    },
	ext_modules=[module_WavUtils, module_TrackBuffer, module_VoiceSampler, module_SF2Synth, module_SimpleInstruments, module_BasicSamplers, module_MeteorGenerator],
	project_urls={  
        'Source': 'https://github.com/fynv/SingingGadgets',
        'Documentation': 'https://scoredraft.org'
    },
)

