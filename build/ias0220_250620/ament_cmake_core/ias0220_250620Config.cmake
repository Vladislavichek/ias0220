# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_ias0220_250620_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED ias0220_250620_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(ias0220_250620_FOUND FALSE)
  elseif(NOT ias0220_250620_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(ias0220_250620_FOUND FALSE)
  endif()
  return()
endif()
set(_ias0220_250620_CONFIG_INCLUDED TRUE)

# output package information
if(NOT ias0220_250620_FIND_QUIETLY)
  message(STATUS "Found ias0220_250620: 0.0.0 (${ias0220_250620_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'ias0220_250620' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${ias0220_250620_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(ias0220_250620_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${ias0220_250620_DIR}/${_extra}")
endforeach()
