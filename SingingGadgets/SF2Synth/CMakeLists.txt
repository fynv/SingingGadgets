cmake_minimum_required (VERSION 3.0)

find_package(PythonLibs 3 REQUIRED)

set(SOURCES
Synth.cpp
SF2Synth.cpp
SF2Synth_Module.cpp
)

set(HEADERS 
Synth.h
SF2Synth.h
)


set (INCLUDE_DIR
${PYTHON_INCLUDE_DIRS}
.
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
add_library (SF2Synth SHARED ${SOURCES} ${HEADERS})
if (WIN32) 
set_target_properties(SF2Synth PROPERTIES SUFFIX ".pyd")
else()
set_target_properties(SF2Synth PROPERTIES SUFFIX ".so")
endif()
set_target_properties(SF2Synth PROPERTIES PREFIX "Py")

target_link_libraries(SF2Synth ${LINK_LIBS})

install(TARGETS SF2Synth 
		RUNTIME DESTINATION SingingGadgets)




