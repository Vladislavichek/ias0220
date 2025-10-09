// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from encoders_interfaces:msg/Counter.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "encoders_interfaces/msg/detail/counter__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace encoders_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void Counter_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) encoders_interfaces::msg::Counter(_init);
}

void Counter_fini_function(void * message_memory)
{
  auto typed_message = static_cast<encoders_interfaces::msg::Counter *>(message_memory);
  typed_message->~Counter();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Counter_message_member_array[2] = {
  {
    "count_left",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(encoders_interfaces::msg::Counter, count_left),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "count_right",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(encoders_interfaces::msg::Counter, count_right),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Counter_message_members = {
  "encoders_interfaces::msg",  // message namespace
  "Counter",  // message name
  2,  // number of fields
  sizeof(encoders_interfaces::msg::Counter),
  Counter_message_member_array,  // message members
  Counter_init_function,  // function to initialize message memory (memory has to be allocated)
  Counter_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Counter_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Counter_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace encoders_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<encoders_interfaces::msg::Counter>()
{
  return &::encoders_interfaces::msg::rosidl_typesupport_introspection_cpp::Counter_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, encoders_interfaces, msg, Counter)() {
  return &::encoders_interfaces::msg::rosidl_typesupport_introspection_cpp::Counter_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
