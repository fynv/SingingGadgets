cmake_minimum_required (VERSION 3.0)

find_package(PythonLibs 3 REQUIRED)

set(SOURCES
WavUtils.cpp
)

set(HEADERS 
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
add_library (WavUtils SHARED ${SOURCES} ${HEADERS})
if (WIN32) 
set_target_properties(WavUtils PROPERTIES SUFFIX ".pyd")
else()
set_target_properties(WavUtils PROPERTIES SUFFIX ".so")
endif()
set_target_properties(WavUtils PROPERTIES PREFIX "Py")

target_link_libraries(WavUtils ${LINK_LIBS})

if (WIN32) 
install(TARGETS WavUtils RUNTIME DESTINATION SingingGadgets)
else()
install(TARGETS WavUtils DESTINATION SingingGadgets)
endif()

