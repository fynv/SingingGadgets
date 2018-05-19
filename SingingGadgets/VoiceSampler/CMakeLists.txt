cmake_minimum_required (VERSION 3.0)

find_package(PythonLibs 3 REQUIRED)

set(SOURCES
../../CPPUtils/DSPUtil/complex.cpp
../../CPPUtils/DSPUtil/fft.cpp
VoiceSampler.cpp
SentenceGeneratorGeneral.cpp
SentenceGeneratorCPU.cpp
)

set(HEADERS 
../../CPPUtils/General/RefCounted.h
../../CPPUtils/General/Deferred.h
../../CPPUtils/General/WavBuf.h
../../CPPUtils/DSPUtil/complex.h
../../CPPUtils/DSPUtil/fft.h
VoiceUtil.h
SentenceDescriptor.h
SentenceGeneratorGeneral.h
SentenceGeneratorCPU.h
)


set (INCLUDE_DIR
${PYTHON_INCLUDE_DIRS}
.
../../CPPUtils/General
../../CPPUtils/DSPUtil
)

set (LINK_LIBS 
${PYTHON_LIBRARIES}
)


if (WIN32) 
set (DEFINES  ${DEFINES}
-D"_CRT_SECURE_NO_DEPRECATE"  
-D"_SCL_SECURE_NO_DEPRECATE" 
)
else()
add_definitions(-std=c++0x)
add_compile_options(-fPIC)
endif()

include_directories(${INCLUDE_DIR})
add_definitions(${DEFINES})
add_library (VoiceSampler SHARED ${SOURCES} ${HEADERS})
if (WIN32) 
set_target_properties(VoiceSampler PROPERTIES SUFFIX ".pyd")
else()
set_target_properties(VoiceSampler PROPERTIES SUFFIX ".so")
endif()
set_target_properties(VoiceSampler PROPERTIES PREFIX "Py")

target_link_libraries(VoiceSampler ${LINK_LIBS})

install(TARGETS VoiceSampler 
		RUNTIME DESTINATION SingingGadgets)


