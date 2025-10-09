// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from encoders_interfaces:msg/Counter.idl
// generated code does not contain a copyright notice
#include "encoders_interfaces/msg/detail/counter__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
encoders_interfaces__msg__Counter__init(encoders_interfaces__msg__Counter * msg)
{
  if (!msg) {
    return false;
  }
  // count_left
  // count_right
  return true;
}

void
encoders_interfaces__msg__Counter__fini(encoders_interfaces__msg__Counter * msg)
{
  if (!msg) {
    return;
  }
  // count_left
  // count_right
}

bool
encoders_interfaces__msg__Counter__are_equal(const encoders_interfaces__msg__Counter * lhs, const encoders_interfaces__msg__Counter * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // count_left
  if (lhs->count_left != rhs->count_left) {
    return false;
  }
  // count_right
  if (lhs->count_right != rhs->count_right) {
    return false;
  }
  return true;
}

bool
encoders_interfaces__msg__Counter__copy(
  const encoders_interfaces__msg__Counter * input,
  encoders_interfaces__msg__Counter * output)
{
  if (!input || !output) {
    return false;
  }
  // count_left
  output->count_left = input->count_left;
  // count_right
  output->count_right = input->count_right;
  return true;
}

encoders_interfaces__msg__Counter *
encoders_interfaces__msg__Counter__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  encoders_interfaces__msg__Counter * msg = (encoders_interfaces__msg__Counter *)allocator.allocate(sizeof(encoders_interfaces__msg__Counter), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(encoders_interfaces__msg__Counter));
  bool success = encoders_interfaces__msg__Counter__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
encoders_interfaces__msg__Counter__destroy(encoders_interfaces__msg__Counter * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    encoders_interfaces__msg__Counter__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
encoders_interfaces__msg__Counter__Sequence__init(encoders_interfaces__msg__Counter__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  encoders_interfaces__msg__Counter * data = NULL;

  if (size) {
    data = (encoders_interfaces__msg__Counter *)allocator.zero_allocate(size, sizeof(encoders_interfaces__msg__Counter), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = encoders_interfaces__msg__Counter__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        encoders_interfaces__msg__Counter__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
encoders_interfaces__msg__Counter__Sequence__fini(encoders_interfaces__msg__Counter__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      encoders_interfaces__msg__Counter__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

encoders_interfaces__msg__Counter__Sequence *
encoders_interfaces__msg__Counter__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  encoders_interfaces__msg__Counter__Sequence * array = (encoders_interfaces__msg__Counter__Sequence *)allocator.allocate(sizeof(encoders_interfaces__msg__Counter__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = encoders_interfaces__msg__Counter__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
encoders_interfaces__msg__Counter__Sequence__destroy(encoders_interfaces__msg__Counter__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    encoders_interfaces__msg__Counter__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
encoders_interfaces__msg__Counter__Sequence__are_equal(const encoders_interfaces__msg__Counter__Sequence * lhs, const encoders_interfaces__msg__Counter__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!encoders_interfaces__msg__Counter__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
encoders_interfaces__msg__Counter__Sequence__copy(
  const encoders_interfaces__msg__Counter__Sequence * input,
  encoders_interfaces__msg__Counter__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(encoders_interfaces__msg__Counter);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    encoders_interfaces__msg__Counter * data =
      (encoders_interfaces__msg__Counter *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!encoders_interfaces__msg__Counter__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          encoders_interfaces__msg__Counter__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!encoders_interfaces__msg__Counter__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
