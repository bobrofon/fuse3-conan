cmake_minimum_required(VERSION 2.8.12)
project(PackageTest C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include(FindPkgConfig)
pkg_check_modules(fuse3 REQUIRED IMPORTED_TARGET fuse3)

add_executable(example example.c)
target_link_libraries(example PkgConfig::fuse3)
