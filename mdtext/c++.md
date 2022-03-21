## google gflags

处理命令行参数

### 定义命令行参数

- DEFINE_bool: 布尔类型
- DEFINE_int32: 32 位整数
- DEFINE_int64: 64 位整数
- DEFINE_uint64: 无符号 64 位整数
- DEFINE_double: 浮点类型 double
- DEFINE_string: C++ string 类型

eg:

```
DEFINE_string(host, "127.0.0.1", "the server host"); (name,value,explain)

DEFINE_int32(port, 12306, "the server port");
```

### 解析命令行参数

```
google::ParseCommandLineFlags(&argc, &argv, true);
```

### 问题

如果同一种类型参数有多个怎么办?

在main函数中的形式是：

```
int main(int argc, char *argv[])
```

## lambda表达式

形式：

```
[函数对象参数] (操作符重载函数参数) mutable 或 exception 声明 -> 返回值类型 {函数体}

```

## transform

transform(first,last,result,op);//first是容器的首迭代器，last为容器的末迭代器，result为存放结果的容器，op为要进行操作的一元函数对象或sturct、class。



## fuction

std::function 一个类模板。

```
template<class R, class ... Args>
class function<R<Args...>;
· R:被调用函数的返回类型
· Args... :被调用函数的形参
```

类模板std :: function是一个通用的多态函数包装器。 std :: function的实例可以存储，复制和调用任何可调用的目标 ：包括函数，lambda表达式，绑定表达式或其他函数对象，以及指向成员函数和指向数据成员的指针。当std::function对象未包裹任何实际的可调用元素，调用该std::function对象将抛出std::bad_function_call异常

## 单例模式 instance()

一个类只能有一个对象被创建。

## 断言函数assert

原理：assert的作用是现计算表达式 expression ，如果其值为假（即为0），那么它先向stderr打印一条出错信息，然后通过调用 abort 来终止程序运行。

## const 关键字

### const修饰类成员函数

const 修饰类成员函数，其目的是防止成员函数修改被调用对象的值，如果我们不想修改一个调用对象的值，所有的成员函数都应当声明为 const 成员函数。

**注意：**const 关键字不能与 static 关键字同时使用，因为 static 关键字修饰静态成员函数，静态成员函数不含有 this 指针，即不能实例化，const 成员函数必须具体到某一实例。

```
//eg
int func_name() const
```



## 编译

g++  test.cc

g++ test.cc -o out_name
