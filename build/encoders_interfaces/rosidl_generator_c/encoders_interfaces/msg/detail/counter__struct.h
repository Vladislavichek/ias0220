// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from encoders_interfaces:msg/Counter.idl
// generated code does not contain a copyright notice

#ifndef ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__STRUCT_H_
#define ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Counter in the package encoders_interfaces.
typedef struct encoders_interfaces__msg__Counter
{
  int64_t count_left;
  int64_t count_right;
} encoders_interfaces__msg__Counter;

// Struct for a sequence of encoders_interfaces__msg__Counter.
typedef struct encoders_interfaces__msg__Counter__Sequence
{
  encoders_interfaces__msg__Counter * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} encoders_interfaces__msg__Counter__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__STRUCT_H_
