# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_IAS_0220_250620_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED IAS_0220_250620_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(IAS_0220_250620_FOUND FALSE)
  elseif(NOT IAS_0220_250620_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(IAS_0220_250620_FOUND FALSE)
  endif()
  return()
endif()
set(_IAS_0220_250620_CONFIG_INCLUDED TRUE)

# output package information
if(NOT IAS_0220_250620_FIND_QUIETLY)
  message(STATUS "Found IAS_0220_250620: 0.0.0 (${IAS_0220_250620_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'IAS_0220_250620' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${IAS_0220_250620_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(IAS_0220_250620_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${IAS_0220_250620_DIR}/${_extra}")
endforeach()
