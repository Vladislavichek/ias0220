#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "encoders_interfaces::encoders_interfaces__rosidl_generator_py" for configuration ""
set_property(TARGET encoders_interfaces::encoders_interfaces__rosidl_generator_py APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(encoders_interfaces::encoders_interfaces__rosidl_generator_py PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libencoders_interfaces__rosidl_generator_py.so"
  IMPORTED_SONAME_NOCONFIG "libencoders_interfaces__rosidl_generator_py.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS encoders_interfaces::encoders_interfaces__rosidl_generator_py )
list(APPEND _IMPORT_CHECK_FILES_FOR_encoders_interfaces::encoders_interfaces__rosidl_generator_py "${_IMPORT_PREFIX}/lib/libencoders_interfaces__rosidl_generator_py.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
