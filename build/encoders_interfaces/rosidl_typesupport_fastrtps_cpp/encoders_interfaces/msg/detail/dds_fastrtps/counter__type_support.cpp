// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from encoders_interfaces:msg/Counter.idl
// generated code does not contain a copyright notice
#include "encoders_interfaces/msg/detail/counter__rosidl_typesupport_fastrtps_cpp.hpp"
#include "encoders_interfaces/msg/detail/counter__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace encoders_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_encoders_interfaces
cdr_serialize(
  const encoders_interfaces::msg::Counter & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: count_left
  cdr << ros_message.count_left;
  // Member: count_right
  cdr << ros_message.count_right;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_encoders_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  encoders_interfaces::msg::Counter & ros_message)
{
  // Member: count_left
  cdr >> ros_message.count_left;

  // Member: count_right
  cdr >> ros_message.count_right;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_encoders_interfaces
get_serialized_size(
  const encoders_interfaces::msg::Counter & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: count_left
  {
    size_t item_size = sizeof(ros_message.count_left);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: count_right
  {
    size_t item_size = sizeof(ros_message.count_right);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_encoders_interfaces
max_serialized_size_Counter(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: count_left
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: count_right
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = encoders_interfaces::msg::Counter;
    is_plain =
      (
      offsetof(DataType, count_right) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _Counter__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const encoders_interfaces::msg::Counter *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Counter__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<encoders_interfaces::msg::Counter *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Counter__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const encoders_interfaces::msg::Counter *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Counter__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Counter(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Counter__callbacks = {
  "encoders_interfaces::msg",
  "Counter",
  _Counter__cdr_serialize,
  _Counter__cdr_deserialize,
  _Counter__get_serialized_size,
  _Counter__max_serialized_size
};

static rosidl_message_type_support_t _Counter__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Counter__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace encoders_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_encoders_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<encoders_interfaces::msg::Counter>()
{
  return &encoders_interfaces::msg::typesupport_fastrtps_cpp::_Counter__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, encoders_interfaces, msg, Counter)() {
  return &encoders_interfaces::msg::typesupport_fastrtps_cpp::_Counter__handle;
}

#ifdef __cplusplus
}
#endif
