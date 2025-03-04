project(Localization)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

cmake_minimum_required (VERSION 3.10)

# -g allows for gdb debugging
# turn on -03 for best performance
add_definitions(-std=c++14 -O3)

set(CXX_FLAGS "-pthread -fPIC -DNDEBUG -Wextra")
set(CMAKE_CXX_FLAGS "${CXX_FLAGS} -Wl,-Bstatic -lboost_filesystem -Wl,-Bdynamic")

set(sources c3-main.cpp helper.cpp)

set(CARLALIB_DIR ${CMAKE_SOURCE_DIR}/libcarla-install/lib)
set(carla_libs  ${CARLALIB_DIR}/libboost_filesystem.a ${CARLALIB_DIR}/libboost_program_options.a ${CARLALIB_DIR}/libboost_python38.a ${CARLALIB_DIR}/libboost_system.a ${CARLALIB_DIR}/libcarla_client.a ${CARLALIB_DIR}/librpc.a ${CARLALIB_DIR}/libDebugUtils.a ${CARLALIB_DIR}/libDetour.a ${CARLALIB_DIR}/libDetourCrowd.a ${CARLALIB_DIR}/libDetourTileCache.a ${CARLALIB_DIR}/libRecast.a)

link_directories(libcarla-install/lib)
include_directories(libcarla-install/include)
include_directories(/opt/carla-simulator/Plugins/carlaviz/backend/third_party/LibCarla/source)
include_directories(libcarla-install/include/system)
include_directories(rpclib/include)
include_directories(/home/ka/carla/LibCarla/source)
include_directories(/home/daniel/Self_Driving_Car_Engineer/nd0013_cd2693_Exercise_Starter_Code/Lesson_7_Project_Scan_Matching_Localization/rcplib/rpclib/include)
include_directories(/home/daniel/Self_Driving_Car_Engineer/nd0013_cd2693_Exercise_Starter_Code/Lesson_7_Project_Scan_Matching_Localization/rcplib/rpclib/include/rpc/msgpack)
include_directories(/home/daniel/Self_Driving_Car_Engineer/nd0013_cd2693_Exercise_Starter_Code/Lesson_7_Project_Scan_Matching_Localization/rcplib/rpclib/include/rpc)
include_directories("/usr/include/eigen3")
include_directories(/usr/local/include)
include_directories(/home/daniel/recastnavigation/Recast/Include)

find_package(PCL 1.2 REQUIRED)
find_package(Boost 1.71.0 COMPONENTS filesystem REQUIRED)



include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
include_directories(${Boost_INCLUDE_DIRS})

if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")

endif(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")

add_executable(cloud_loc ${sources} )

target_link_libraries(cloud_loc ${PCL_LIBRARIES} ${carla_libs} ${Boost_LIBRARIES})