cmake_minimum_required (VERSION 3.0)

find_package(PythonLibs 3 REQUIRED)

set(SOURCES
SimpleInstruments.cpp
)

set(HEADERS 
../../CPPUtils/General/RefCounted.h
../../CPPUtils/General/Deferred.h
../../CPPUtils/General/WavBuf.h
)


set (INCLUDE_DIR
${PYTHON_INCLUDE_DIRS}
.
../../CPPUtils/General
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
add_library (SimpleInstruments SHARED ${SOURCES} ${HEADERS})
if (WIN32) 
set_target_properties(SimpleInstruments PROPERTIES SUFFIX ".pyd")
else()
set_target_properties(SimpleInstruments PROPERTIES SUFFIX ".so")
endif()
set_target_properties(SimpleInstruments PROPERTIES PREFIX "Py")

target_link_libraries(SimpleInstruments ${LINK_LIBS})

if (WIN32)
install(TARGETS SimpleInstruments RUNTIME DESTINATION SingingGadgets)
else()
install(TARGETS SimpleInstruments DESTINATION SingingGadgets)
endif()

