// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from encoders_interfaces:msg/Counter.idl
// generated code does not contain a copyright notice

#ifndef ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__TRAITS_HPP_
#define ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "encoders_interfaces/msg/detail/counter__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace encoders_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Counter & msg,
  std::ostream & out)
{
  out << "{";
  // member: count_left
  {
    out << "count_left: ";
    rosidl_generator_traits::value_to_yaml(msg.count_left, out);
    out << ", ";
  }

  // member: count_right
  {
    out << "count_right: ";
    rosidl_generator_traits::value_to_yaml(msg.count_right, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Counter & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: count_left
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "count_left: ";
    rosidl_generator_traits::value_to_yaml(msg.count_left, out);
    out << "\n";
  }

  // member: count_right
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "count_right: ";
    rosidl_generator_traits::value_to_yaml(msg.count_right, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Counter & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace encoders_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use encoders_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const encoders_interfaces::msg::Counter & msg,
  std::ostream & out, size_t indentation = 0)
{
  encoders_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use encoders_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const encoders_interfaces::msg::Counter & msg)
{
  return encoders_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<encoders_interfaces::msg::Counter>()
{
  return "encoders_interfaces::msg::Counter";
}

template<>
inline const char * name<encoders_interfaces::msg::Counter>()
{
  return "encoders_interfaces/msg/Counter";
}

template<>
struct has_fixed_size<encoders_interfaces::msg::Counter>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<encoders_interfaces::msg::Counter>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<encoders_interfaces::msg::Counter>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__TRAITS_HPP_
