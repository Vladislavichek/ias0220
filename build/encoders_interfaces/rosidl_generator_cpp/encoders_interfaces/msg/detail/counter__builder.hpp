// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from encoders_interfaces:msg/Counter.idl
// generated code does not contain a copyright notice

#ifndef ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__BUILDER_HPP_
#define ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "encoders_interfaces/msg/detail/counter__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace encoders_interfaces
{

namespace msg
{

namespace builder
{

class Init_Counter_count_right
{
public:
  explicit Init_Counter_count_right(::encoders_interfaces::msg::Counter & msg)
  : msg_(msg)
  {}
  ::encoders_interfaces::msg::Counter count_right(::encoders_interfaces::msg::Counter::_count_right_type arg)
  {
    msg_.count_right = std::move(arg);
    return std::move(msg_);
  }

private:
  ::encoders_interfaces::msg::Counter msg_;
};

class Init_Counter_count_left
{
public:
  Init_Counter_count_left()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Counter_count_right count_left(::encoders_interfaces::msg::Counter::_count_left_type arg)
  {
    msg_.count_left = std::move(arg);
    return Init_Counter_count_right(msg_);
  }

private:
  ::encoders_interfaces::msg::Counter msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::encoders_interfaces::msg::Counter>()
{
  return encoders_interfaces::msg::builder::Init_Counter_count_left();
}

}  // namespace encoders_interfaces

#endif  // ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__BUILDER_HPP_
