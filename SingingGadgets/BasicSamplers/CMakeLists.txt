cmake_minimum_required (VERSION 3.0)

find_package(PythonLibs 3 REQUIRED)

set(SOURCES
../../CPPUtils/DSPUtil/complex.cpp
../../CPPUtils/DSPUtil/fft.cpp
BasicSamplers.cpp
PercussionSampler.cpp
InstrumentSingleSampler.cpp
InstrumentMultiSampler.cpp
FrequencyDetection.cpp
)


set(HEADERS 
../../CPPUtils/General/RefCounted.h
../../CPPUtils/General/Deferred.h
../../CPPUtils/General/WavBuf.h
../../CPPUtils/DSPUtil/complex.h
../../CPPUtils/DSPUtil/fft.h
Sample.h
PercussionSampler.h
InstrumentSingleSampler.h
InstrumentMultiSampler.h
FrequencyDetection.h
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
add_library (BasicSamplers SHARED ${SOURCES} ${HEADERS})
if (WIN32) 
set_target_properties(BasicSamplers PROPERTIES SUFFIX ".pyd")
else()
set_target_properties(BasicSamplers PROPERTIES SUFFIX ".so")
endif()
set_target_properties(BasicSamplers PROPERTIES PREFIX "Py")

target_link_libraries(BasicSamplers ${LINK_LIBS})

if (WIN32)
install(TARGETS BasicSamplers RUNTIME DESTINATION SingingGadgets)
else()
install(TARGETS BasicSamplers DESTINATION SingingGadgets)
endif()
