// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from encoders_interfaces:msg/Counter.idl
// generated code does not contain a copyright notice

#ifndef ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__STRUCT_HPP_
#define ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__encoders_interfaces__msg__Counter __attribute__((deprecated))
#else
# define DEPRECATED__encoders_interfaces__msg__Counter __declspec(deprecated)
#endif

namespace encoders_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Counter_
{
  using Type = Counter_<ContainerAllocator>;

  explicit Counter_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->count_left = 0ll;
      this->count_right = 0ll;
    }
  }

  explicit Counter_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->count_left = 0ll;
      this->count_right = 0ll;
    }
  }

  // field types and members
  using _count_left_type =
    int64_t;
  _count_left_type count_left;
  using _count_right_type =
    int64_t;
  _count_right_type count_right;

  // setters for named parameter idiom
  Type & set__count_left(
    const int64_t & _arg)
  {
    this->count_left = _arg;
    return *this;
  }
  Type & set__count_right(
    const int64_t & _arg)
  {
    this->count_right = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    encoders_interfaces::msg::Counter_<ContainerAllocator> *;
  using ConstRawPtr =
    const encoders_interfaces::msg::Counter_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<encoders_interfaces::msg::Counter_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<encoders_interfaces::msg::Counter_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      encoders_interfaces::msg::Counter_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<encoders_interfaces::msg::Counter_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      encoders_interfaces::msg::Counter_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<encoders_interfaces::msg::Counter_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<encoders_interfaces::msg::Counter_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<encoders_interfaces::msg::Counter_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__encoders_interfaces__msg__Counter
    std::shared_ptr<encoders_interfaces::msg::Counter_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__encoders_interfaces__msg__Counter
    std::shared_ptr<encoders_interfaces::msg::Counter_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Counter_ & other) const
  {
    if (this->count_left != other.count_left) {
      return false;
    }
    if (this->count_right != other.count_right) {
      return false;
    }
    return true;
  }
  bool operator!=(const Counter_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Counter_

// alias to use template instance with default allocator
using Counter =
  encoders_interfaces::msg::Counter_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace encoders_interfaces

#endif  // ENCODERS_INTERFACES__MSG__DETAIL__COUNTER__STRUCT_HPP_
