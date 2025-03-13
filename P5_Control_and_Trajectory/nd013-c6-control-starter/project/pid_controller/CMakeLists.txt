project(PidController)

cmake_minimum_required(VERSION 3.10)

add_definitions(-std=c++14 -O3)

set(CXX_FLAGS "-pthread -fPIC -DNDEBUG -Wall -Wextra")
set(CMAKE_CXX_FLAGS "${CXX_FLAGS} -Wl,-Bstatic -lcarla_client -lrpc -lboost_filesystem -Wl,-Bdynamic")

set(sources main.cpp behavior_planner_FSM.cpp motion_planner.cpp cubic_spiral.cpp spiral_base.cpp integral.cpp spiral_equations.cpp cost_functions.cpp utils.cpp velocity_profile_generator.cpp pid_controller.cpp)

set(CARLA_SOURCE_DIR /opt/carla-source)
set(CARLA_BUILD_DIR ${CARLA_SOURCE_DIR}/Build)
set(CARLA_BUILD_BOOST_DIR ${CARLA_BUILD_DIR}/boost_1_72_0)
set(CARLA_BUILD_RECAST_DIR ${CARLA_BUILD_DIR}/recastnavigation)
set(CARLA_BUILD_RPCLIB_DIR ${CARLA_BUILD_DIR}/rpclib)

set(CARLA_BUILD_LIBCARLA_DIR ${CARLA_BUILD_DIR}/libcarla-client-build.release/LibCarla/cmake/client)
set(CARLA_BUILD_BOOST_LIB_DIR ${CARLA_BUILD_BOOST_DIR}/lib)
set(CARLA_BUILD_RECAST_LIB_DIR ${CARLA_BUILD_RECAST_DIR}/build/lib)
set(CARLA_BUILD_RPCLIB_LIB_DIR ${CARLA_BUILD_RPCLIB_DIR}/lib)

set(carla_libs 
    /usr/lib/x86_64-linux-gnu/libboost_filesystem.a 
    /usr/lib/x86_64-linux-gnu/libboost_program_options.a 
    /usr/lib/x86_64-linux-gnu/libboost_python38.a 
    /usr/lib/x86_64-linux-gnu/libboost_system.a 
    ${CARLA_BUILD_LIBCARLA_DIR}/libcarla_client.a 
    ${CARLA_BUILD_RPCLIB_LIB_DIR}/librpc.a 
    ${CARLA_BUILD_RECAST_LIB_DIR}/libDebugUtils.a 
    ${CARLA_BUILD_RECAST_LIB_DIR}/libDetour.a 
    ${CARLA_BUILD_RECAST_LIB_DIR}/libDetourCrowd.a 
    ${CARLA_BUILD_RECAST_LIB_DIR}/libDetourTileCache.a 
    ${CARLA_BUILD_RECAST_LIB_DIR}/libRecast.a
)

include_directories(
    /usr/local/include
    ${CARLA_SOURCE_DIR}/LibCarla/source
    ${CARLA_BUILD_BOOST_DIR}/include
    ${CARLA_BUILD_RECAST_DIR}/include
    ${CARLA_BUILD_RPCLIB_DIR}/include
    /usr/include/msgpack
    /usr/include/uWS  # Updated to match actual location
)

link_directories(
    /usr/local/lib
    ${CARLA_BUILD_LIBCARLA_DIR}
    ${CARLA_BUILD_BOOST_LIB_DIR}
    ${CARLA_BUILD_RECAST_LIB_DIR}
    ${CARLA_BUILD_RPCLIB_LIB_DIR}
)

if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
endif()

add_executable(pid_controller ${sources})

target_link_libraries(pid_controller 
    z ssl uv uWS
    ${carla_libs} 
    gtest glog boost_filesystem lapack 
    msgpackc
)