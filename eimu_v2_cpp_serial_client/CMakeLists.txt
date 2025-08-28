cmake_minimum_required(VERSION 3.16)
project(eimu_v2_cpp LANGUAGES CXX)

include_directories(include)

add_executable( read_imu examples/read_imu.cpp )
target_link_libraries( read_imu serial )

