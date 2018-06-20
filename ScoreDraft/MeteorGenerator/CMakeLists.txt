cmake_minimum_required (VERSION 3.0)

find_package(PythonLibs 3 REQUIRED)

set(SOURCES
MeteorGenerator.cpp
)

set(HEADERS
SubListLookUp.h 
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
add_library (MeteorGenerator SHARED ${SOURCES} ${HEADERS})
if (WIN32) 
set_target_properties(MeteorGenerator PROPERTIES SUFFIX ".pyd")
else()
set_target_properties(MeteorGenerator PROPERTIES SUFFIX ".so")
endif()
set_target_properties(MeteorGenerator PROPERTIES PREFIX "Py")

target_link_libraries(MeteorGenerator ${LINK_LIBS})

if (WIN32) 
install(TARGETS MeteorGenerator RUNTIME DESTINATION ScoreDraft)
else()
install(TARGETS MeteorGenerator DESTINATION ScoreDraft)
endif()


