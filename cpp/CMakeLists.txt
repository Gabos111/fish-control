cmake_minimum_required(VERSION 3.5)
project(fish_control)

# ensure CMake can locate yaml-cpp on Debian platforms
list(APPEND CMAKE_PREFIX_PATH "/usr/lib/aarch64-linux-gnu/cmake/yaml-cpp")

 find_package(yaml-cpp REQUIRED)

# locate pigpiod_if2 client library (daemon interface)
find_library(PIGPIOD_LIBRARY pigpiod_if2
  PATHS /usr/lib /usr/local/lib
)
if (NOT PIGPIOD_LIBRARY)
  message(FATAL_ERROR "Could not find pigpiod_if2: please install libpigpio-dev")
endif()

# ---- locate the installed SDK libs ----
find_library(DSDK_CPP_LIB NAMES dxl_sbc_cpp PATHS /usr/local/lib)
find_library(DSDK_C_LIB   NAMES dxl_sbc_c   PATHS /usr/local/lib)

# ---- add include paths ----
include_directories(
  ${CMAKE_SOURCE_DIR}/include      # project headers (Kinematics.h, etc.)
  ${PIGPIO_INCLUDE_DIR}            # pigpio headers
  /usr/local/include/dynamixel_sdk               # DynamixelSDK headers
)

# ---- build your executable ----
 add_executable(fish_control
   src/main.cpp
   src/Kinematics.cpp
   src/DynamixelSDKWrapper.cpp
   src/PigpioServo.cpp
   src/Logger.cpp
 )

# ---- link against all deps ----
 target_link_libraries(fish_control
   yaml-cpp
   ${PIGPIOD_LIBRARY}
   ${DSDK_CPP_LIB}
   ${DSDK_C_LIB}
 )

 install(TARGETS fish_control
  RUNTIME DESTINATION bin
)