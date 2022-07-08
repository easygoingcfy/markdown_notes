# c++

中文：https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/contents/

官方：https://google.github.io/styleguide/cppguide.html

## 1. 头文件

### 1.1 Self-contained 

头文件应该能够自给自足（self-contained,也就是可以作为第一个头文件被引入），以 `.h` 结尾。至于用来插入文本的文件，说到底它们并不是头文件，所以应以 `.inc` 结尾。不允许分离出 `-inl.h` 头文件的做法.

### 1.2  #define 保护

所有头文件都应该有 `#define` 保护来防止头文件被多重包含, 命名格式当是: 

```
<PROJECT>_<PATH>_<FILE>_H_
```

为保证唯一性, 头文件的命名应该基于所在项目源代码树的全路径. 例如, 项目 `foo` 中的头文件 `foo/src/bar/baz.h` 可按如下方式保护:

```c++
#ifndef FOO_BAR_BAZ_H_
#define FOO_BAR_BAZ_H_
...
#endif // FOO_BAR_BAZ_H_
```

### 1.3 前置声明

尽可能地避免使用前置声明。使用 `#include` 包含需要的头文件即可。

**定义：**

> 所谓「前置声明」（forward declaration）是类、函数和模板的纯粹声明，没伴随着其定义.

**优点：**

> - 前置声明能够节省编译时间，多余的 `#include` 会迫使编译器展开更多的文件，处理更多的输入。
> - 前置声明能够节省不必要的重新编译的时间。 `#include` 使代码因为头文件中无关的改动而被重新编译多次。

**缺点：**

> - 前置声明隐藏了依赖关系，头文件改动时，用户的代码会跳过必要的重新编译过程。
>
> - 前置声明可能会被库的后续更改所破坏。前置声明函数或模板有时会妨碍头文件开发者变动其 API. 例如扩大形参类型，加个自带默认参数的模板形参等等。
>
> - 前置声明来自命名空间 `std::` 的 symbol 时，其行为未定义。
>
> - 很难判断什么时候该用前置声明，什么时候该用 `#include` 。极端情况下，用前置声明代替 `#include` 甚至都会暗暗地改变代码的含义：
>
>   > ```
>   > // b.h:
>   > struct B {};
>   > struct D : B {};
>   > 
>   > // good_user.cc:
>   > #include "b.h"
>   > void f(B*);
>   > void f(void*);
>   > void test(D* x) { f(x); }  // calls f(B*)
>   > ```
>
> > 如果 `#include` 被 `B` 和 `D` 的前置声明替代， `test()` 就会调用 `f(void*)` .
>
> - 前置声明了不少来自头文件的 symbol 时，就会比单单一行的 `include` 冗长。
> - 仅仅为了能前置声明而重构代码（比如用指针成员代替对象成员）会使代码变得更慢更复杂.

**结论：**

> - 尽量避免前置声明那些定义在其他项目中的实体.
> - 函数：总是使用 `#include`.
> - 类模板：优先使用 `#include`.

### 1.4 内联函数

只有当函数只有 10 行甚至更少时才将其定义为内联函数.

**结论:**

> 一个较为合理的经验准则是, 不要内联超过 10 行的函数. 谨慎对待析构函数, 析构函数往往比其表面看起来要更长, 因为有隐含的成员和基类析构函数被调用!
>
> 另一个实用的经验准则: 内联那些包含循环或 `switch` 语句的函数常常是得不偿失 (除非在大多数情况下, 这些循环或 `switch` 语句从不被执行).
>
> 有些函数即使声明为内联的也不一定会被编译器内联, 这点很重要; 比如虚函数和递归函数就不会被正常内联. 通常, 递归函数不应该声明成内联函数.（YuleFox 注: 递归调用堆栈的展开并不像循环那么简单, 比如递归层数在编译时可能是未知的, 大多数编译器都不支持内联递归函数). 虚函数内联的主要原因则是想把它的函数体放在类定义内, 为了图个方便, 抑或是当作文档描述其行为, 比如精短的存取函数.

### 1.5  `#include` 的路径及顺序

使用标准的头文件包含顺序可增强可读性, 避免隐藏依赖: 相关头文件, C 库, C++ 库, 其他库的 .h, 本项目内的 .h.

#### 头文件的次序

1. `dir2/foo2.h` (优先位置, 详情如下)
2. C 系统文件
3. C++ 系统文件
4. 其他库的 `.h` 文件
5. 本项目内 `.h` 文件

举例来说, `google-awesome-project/src/foo/internal/fooserver.cc` 的包含次序如下:

> ```
> #include "foo/public/fooserver.h" // 优先位置
> 
> #include <sys/types.h>
> #include <unistd.h>
> 
> #include <hash_map>
> #include <vector>
> 
> #include "base/basictypes.h"
> #include "base/commandlineflags.h"
> #include "foo/public/bar.h"
> ```

### 1.6 笔记

1. 标准化函数参数顺序可以提高可读性和易维护性
2. 避免多重包含是学编程时最基本的要求
3. 前置声明是为了降低编译依赖，防止修改一个头文件引发多米诺效应;
4. 注意，前置声明的类是不完全类型（incomplete type），我们只能定义指向该类型的指针或引用，或者声明（但不能定义）以不完全类型作为参数或者返回类型的函数。毕竟编译器不知道不完全类型的定义，我们不能创建其类的任何对象，也不能声明成类内部的数据成员。
5. 类内部的函数一般会自动内联。所以某函数一旦不需要内联，其定义就不要再放在头文件里，而是放到对应的 `.cc` 文件里。这样可以保持头文件的类相当精炼，也很好地贯彻了声明与定义分离的原则。
6. 在 `#include` 中插入空行以分割相关头文件, C 库, C++ 库, 其他库的 `.h` 和本项目内的 `.h` 是个好习惯。

## 2. 作用域

### 2.1. 命名空间

**tips**

鼓励在 `.cc` 文件内使用匿名命名空间或 `static` 声明. 使用具名的命名空间时, 其名称可基于项目名或相对路径. 禁止使用 using 指示（using-directive）。禁止使用内联命名空间（inline namespace）。

**定义:**

> 命名空间将全局作用域细分为独立的, 具名的作用域, 可有效防止全局作用域的命名冲突.

**优点:**

> 虽然类已经提供了（可嵌套的）命名轴线 (YuleFox 注: 将命名分割在不同类的作用域内), 命名空间在这基础上又封装了一层.
>
> 举例来说, 两个不同项目的全局作用域都有一个类 `Foo`, 这样在编译或运行时造成冲突. 如果每个项目将代码置于不同命名空间中, `project1::Foo` 和 `project2::Foo` 作为不同符号自然不会冲突.
>
> 内联命名空间会自动把内部的标识符放到外层作用域，比如：
>
> ```
> namespace X {
> inline namespace Y {
> void foo();
> }  // namespace Y
> }  // namespace X
> ```
>
> `X::Y::foo()` 与 `X::foo()` 彼此可代替。内联命名空间主要用来保持跨版本的 ABI 兼容性。

**缺点:**

> 命名空间具有迷惑性, 因为它们使得区分两个相同命名所指代的定义更加困难。
>
> 内联命名空间很容易令人迷惑，毕竟其内部的成员不再受其声明所在命名空间的限制。内联命名空间只在大型版本控制里有用。
>
> 有时候不得不多次引用某个定义在许多嵌套命名空间里的实体，使用完整的命名空间会导致代码的冗长。
>
> 在头文件中使用匿名空间导致违背 C++ 的唯一定义原则 (One Definition Rule (ODR)).

**结论:**

> 根据下文将要提到的策略合理使用命名空间.
>
> - 遵守 [命名空间命名](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/scoping/naming.html#namespace-names) 中的规则。
>
> - 像之前的几个例子中一样，在命名空间的最后注释出命名空间的名字。
>
> - 用命名空间把文件包含, [gflags](https://gflags.github.io/gflags/) 的声明/定义, 以及类的前置声明以外的整个源文件封装起来, 以区别于其它命名空间:
>
>   > ```
>   > // .h 文件
>   > namespace mynamespace {
>   > 
>   > // 所有声明都置于命名空间中
>   > // 注意不要使用缩进
>   > class MyClass {
>   >     public:
>   >     ...
>   >     void Foo();
>   > };
>   > 
>   > } // namespace mynamespace
>   > ```
>   >
>   > ```
>   > // .cc 文件
>   > namespace mynamespace {
>   > 
>   > // 函数定义都置于命名空间中
>   > void MyClass::Foo() {
>   >     ...
>   > }
>   > 
>   > } // namespace mynamespace
>   > ```
>   >
>   > 更复杂的 `.cc` 文件包含更多, 更复杂的细节, 比如 gflags 或 using 声明。
>   >
>   > ```
>   > #include "a.h"
>   > 
>   > DEFINE_FLAG(bool, someflag, false, "dummy flag");
>   > 
>   > namespace a {
>   > 
>   > ...code for a...                // 左对齐
>   > 
>   > } // namespace a
>   > ```
>
> - 不要在命名空间 `std` 内声明任何东西, 包括标准库的类前置声明. 在 `std` 命名空间声明实体是未定义的行为, 会导致如不可移植. 声明标准库下的实体, 需要包含对应的头文件.
>
> - 不应该使用 *using 指示* 引入整个命名空间的标识符号。
>
>   > ```
>   > // 禁止 —— 污染命名空间
>   > using namespace foo;
>   > ```
>
> - 不要在头文件中使用 *命名空间别名* 除非显式标记内部命名空间使用。因为任何在头文件中引入的命名空间都会成为公开API的一部分。
>
>   > ```
>   > // 在 .cc 中使用别名缩短常用的命名空间
>   > namespace baz = ::foo::bar::baz;
>   > ```
>   >
>   > ```
>   > // 在 .h 中使用别名缩短常用的命名空间
>   > namespace librarian {
>   > namespace impl {  // 仅限内部使用
>   > namespace sidetable = ::pipeline_diagnostics::sidetable;
>   > }  // namespace impl
>   > 
>   > inline void my_inline_function() {
>   >   // 限制在一个函数中的命名空间别名
>   >   namespace baz = ::foo::bar::baz;
>   >   ...
>   > }
>   > }  // namespace librarian
>   > ```
>
> - 禁止用内联命名空间

### 2.2 匿名命名空间和静态变量

**tips**

> 在 `.cc` 文件中定义一个不需要被外部引用的变量时，可以将它们放在匿名命名空间或声明为 `static` 。但是不要在 `.h` 文件中这么做。

**定义:**

> 所有置于匿名命名空间的声明都具有内部链接性，函数和变量可以经由声明为 `static` 拥有内部链接性，这意味着你在这个文件中声明的这些标识符都不能在另一个文件中被访问。即使两个文件声明了完全一样名字的标识符，它们所指向的实体实际上是完全不同的。

**结论:**

> 推荐、鼓励在 `.cc` 中对于不需要在其他地方引用的标识符使用内部链接性声明，但是不要在 `.h` 中使用。
>
> 匿名命名空间的声明和具名的格式相同，在最后注释上 `namespace` :
>
> ```c++
> namespace {
> ...
> }  // namespace
> ```

### 2.3  非成员函数、静态成员函数和全局函数

**tips**

> 使用静态成员函数或命名空间内的非成员函数, 尽量不要用裸的全局函数. 将一系列函数直接置于命名空间中，不要用类的静态方法模拟出命名空间的效果，类的静态方法应当和类的实例或静态数据紧密相关.

**优点:**

> 某些情况下, 非成员函数和静态成员函数是非常有用的, 将非成员函数放在命名空间内可避免污染全局作用域.

**缺点:**

> 将非成员函数和静态成员函数作为新类的成员或许更有意义, 当它们需要访问外部资源或具有重要的依赖关系时更是如此.

**结论:**

> 有时, 把函数的定义同类的实例脱钩是有益的, 甚至是必要的. 这样的函数可以被定义成静态成员, 或是非成员函数. 非成员函数不应依赖于外部变量, 应尽量置于某个命名空间内. 相比单纯为了封装若干不共享任何静态数据的静态成员函数而创建类, 不如使用 [2.1. 命名空间](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/scoping/#namespaces) 。举例而言，对于头文件 `myproject/foo_bar.h` , 应当使用
>
> ```
> namespace myproject {
> namespace foo_bar {
> void Function1();
> void Function2();
> }  // namespace foo_bar
> }  // namespace myproject
> ```
>
> 而非
>
> ```
> namespace myproject {
> class FooBar {
>  public:
>   static void Function1();
>   static void Function2();
> };
> }  // namespace myproject
> ```
>
> 定义在同一编译单元的函数, 被其他编译单元直接调用可能会引入不必要的耦合和链接时依赖; 静态成员函数对此尤其敏感. 可以考虑提取到新类中, 或者将函数置于独立库的命名空间内.
>
> 如果你必须定义非成员函数, 又只是在 `.cc` 文件中使用它, 可使用匿名 [2.1. 命名空间](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/scoping/#namespaces) 或 `static` 链接关键字 (如 `static int Foo() {...}`) 限定其作用域.

### 2.4 局部变量

**tips**

将函数变量尽可能置于最小作用域内, 并在变量声明时进行初始化.

C++ 允许在函数的任何位置声明变量. 我们提倡在尽可能小的作用域中声明变量, 离第一次使用越近越好. 这使得代码浏览者更容易定位变量声明的位置, 了解变量的类型和初始值. 特别是，应使用初始化的方式替代声明再赋值, 比如:

> ```
> int i;
> i = f(); // 坏——初始化和声明分离
> 
> int j = g(); // 好——初始化时声明
> 
> vector<int> v;
> v.push_back(1); // 用花括号初始化更好
> v.push_back(2);
> 
> vector<int> v = {1, 2}; // 好——v 一开始就初始化
> ```

属于 `if`, `while` 和 `for` 语句的变量应当在这些语句中正常地声明，这样子这些变量的作用域就被限制在这些语句中了，举例而言:

> ```
> while (const char* p = strchr(str, '/')) str = p + 1;
> ```

**Warning**

有一个例外, 如果变量是一个对象, 每次进入作用域都要调用其构造函数, 每次退出作用域都要调用其析构函数. 这会导致效率降低.

```
// 低效的实现
for (int i = 0; i < 1000000; ++i) {
    Foo f;                  // 构造函数和析构函数分别调用 1000000 次!
    f.DoSomething(i);
}
```

在循环作用域外面声明这类变量要高效的多:

```
Foo f;                      // 构造函数和析构函数只调用 1 次
for (int i = 0; i < 1000000; ++i) {
    f.DoSomething(i);
}
```

### 2.5 静态和全局变量

**tip**

> 禁止定义静态储存周期非POD变量，禁止使用含有副作用的函数初始化POD全局变量，因为多编译单元中的静态变量执行时的构造和析构顺序是未明确的，这将导致代码的不可移植

禁止使用类的 [静态储存周期](http://zh.cppreference.com/w/cpp/language/storage_duration#.E5.AD.98.E5.82.A8.E6.9C.9F) 变量：由于构造和析构函数调用顺序的不确定性，它们会导致难以发现的 bug 。不过 `constexpr` 变量除外，毕竟它们又不涉及动态初始化或析构。

静态生存周期的对象，即包括了全局变量，静态变量，静态类成员变量和函数静态变量，都必须是原生数据类型 (POD : Plain Old Data): 即 int, char 和 float, 以及 POD 类型的指针、数组和结构体。

静态变量的构造函数、析构函数和初始化的顺序在 C++ 中是只有部分明确的，甚至随着构建变化而变化，导致难以发现的 bug. 所以除了禁用类类型的全局变量，我们也不允许用函数返回值来初始化 POD 变量，除非该函数（比如 `getenv()` 或 `getpid()` ）不涉及任何全局变量。函数作用域里的静态变量除外，毕竟它的初始化顺序是有明确定义的，而且只会在指令执行到它的声明那里才会发生。

> Note
>
> 同一个编译单元内是明确的，静态初始化优先于动态初始化，初始化顺序按照声明顺序进行，销毁则逆序。不同的编译单元之间初始化和销毁顺序属于未明确行为 (unspecified behaviour)。

同理，全局和静态变量在程序中断时会被析构，无论所谓中断是从 `main()` 返回还是对 `exit()` 的调用。析构顺序正好与构造函数调用的顺序相反。但既然构造顺序未定义，那么析构顺序当然也就不定了。比如，在程序结束时某静态变量已经被析构了，但代码还在跑——比如其它线程——并试图访问它且失败；再比如，一个静态 string 变量也许会在一个引用了前者的其它变量析构之前被析构掉。

改善以上析构问题的办法之一是用 `quick_exit()` 来代替 `exit()` 并中断程序。它们的不同之处是前者不会执行任何析构，也不会执行 `atexit()` 所绑定的任何 handlers. 如果您想在执行 `quick_exit()` 来中断时执行某 handler（比如刷新 log），您可以把它绑定到 `_at_quick_exit()`. 如果您想在 `exit()` 和 `quick_exit()` 都用上该 handler, 都绑定上去。

综上所述，我们只允许 POD 类型的静态变量，即完全禁用 `vector` (使用 C 数组替代) 和 `string` (使用 `const char []`)。

如果您确实需要一个 `class` 类型的静态或全局变量，可以考虑在 `main()` 函数或 `pthread_once()` 内初始化一个指针且永不回收。注意只能用 raw 指针，别用智能指针，毕竟后者的析构函数涉及到上文指出的不定顺序问题。

> Note
>
> 上文提及的静态变量泛指静态生存周期的对象, 包括: 全局变量, 静态变量, 静态类成员变量, 以及函数静态变量.

### 2.6 笔记

1. `cc` 中的匿名命名空间可避免命名冲突, 限定作用域, 避免直接使用 `using` 关键字污染命名空间;
2. 嵌套类符合局部使用原则, 只是不能在其他头文件中前置声明, 尽量不要 `public`;
3. 尽量不用全局函数和全局变量, 考虑作用域和命名空间限制, 尽量单独形成编译单元;
4. 多线程中的全局变量 (含静态成员变量) 不要使用 `class` 类型 (含 STL 容器), 避免不明确行为导致的 bug.
5. 作用域的使用, 除了考虑名称污染, 可读性之外, 主要是为降低耦合, 提高编译/执行效率.
6. 注意「using 指示（using-directive）」和「using 声明（using-declaration）」的区别。
7. 匿名命名空间说白了就是文件作用域，就像 C static 声明的作用域一样，后者已经被 C++ 标准提倡弃用。
8. 局部变量在声明的同时进行显式值初始化，比起隐式初始化再赋值的两步过程要高效，同时也贯彻了计算机体系结构重要的概念「局部性（locality）」。
9. 注意别在循环犯大量构造和析构的低级错误

## 3. 类

### 3.1 构造函数的职责

**总述**

不要在构造函数中调用虚函数, 也不要在无法报出错误时进行可能失败的初始化.

**定义**

在构造函数中可以进行各种初始化操作.

**优点**

> - 无需考虑类是否被初始化.
> - 经过构造函数完全初始化后的对象可以为 `const` 类型, 也能更方便地被标准容器或算法使用.

**缺点**

> - 如果在构造函数内调用了自身的虚函数, 这类调用是不会重定向到子类的虚函数实现. 即使当前没有子类化实现, 将来仍是隐患.
> - 在没有使程序崩溃 (因为并不是一个始终合适的方法) 或者使用异常 (因为已经被 [禁用](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/others/#exceptions) 了) 等方法的条件下, 构造函数很难上报错误
> - 如果执行失败, 会得到一个初始化失败的对象, 这个对象有可能进入不正常的状态, 必须使用 `bool IsValid()` 或类似这样的机制才能检查出来, 然而这是一个十分容易被疏忽的方法.
> - 构造函数的地址是无法被取得的, 因此, 举例来说, 由构造函数完成的工作是无法以简单的方式交给其他线程的.

**结论**

> 构造函数不允许调用虚函数. 如果代码允许, 直接终止程序是一个合适的处理错误的方式. 否则, 考虑用 `Init()` 方法或工厂函数.
>
> 构造函数不得调用虚函数, 或尝试报告一个非致命错误. 如果对象需要进行有意义的 (non-trivial) 初始化, 考虑使用明确的 Init() 方法或使用工厂模式. Avoid `Init()` methods on objects with no other states that affect which public methods may be called (此类形式的半构造对象有时无法正确工作).

### 3.2 隐式类型转换

**总述**

不要定义隐式类型转换. 对于转换运算符和单参数构造函数, 请使用 `explicit` 关键字.

**定义**

> 隐式类型转换允许一个某种类型 (称作 *源类型*) 的对象被用于需要另一种类型 (称作 *目的类型*) 的位置, 例如, 将一个 `int` 类型的参数传递给需要 `double` 类型的函数.
>
> 除了语言所定义的隐式类型转换, 用户还可以通过在类定义中添加合适的成员定义自己需要的转换. 在源类型中定义隐式类型转换, 可以通过目的类型名的类型转换运算符实现 (例如 `operator bool()`). 在目的类型中定义隐式类型转换, 则通过以源类型作为其唯一参数 (或唯一无默认值的参数) 的构造函数实现.
>
> `explicit` 关键字可以用于构造函数或 (在 C++11 引入) 类型转换运算符, 以保证只有当目的类型在调用点被显式写明时才能进行类型转换, 例如使用 `cast`. 这不仅作用于隐式类型转换, 还能作用于 C++11 的列表初始化语法:
>
> ```
> class Foo {
>   explicit Foo(int x, double y);
>   ...
> };
> 
> void Func(Foo f);
> ```
>
> 此时下面的代码是不允许的:
>
> ```
> Func({42, 3.14});  // Error
> ```
>
> 这一代码从技术上说并非隐式类型转换, 但是语言标准认为这是 `explicit` 应当限制的行为.

**优点**

> - 有时目的类型名是一目了然的, 通过避免显式地写出类型名, 隐式类型转换可以让一个类型的可用性和表达性更强.
> - 隐式类型转换可以简单地取代函数重载.
> - 在初始化对象时, 列表初始化语法是一种简洁明了的写法.

**缺点**

> - 隐式类型转换会隐藏类型不匹配的错误. 有时, 目的类型并不符合用户的期望, 甚至用户根本没有意识到发生了类型转换.
> - 隐式类型转换会让代码难以阅读, 尤其是在有函数重载的时候, 因为这时很难判断到底是哪个函数被调用.
> - 单参数构造函数有可能会被无意地用作隐式类型转换.
> - 如果单参数构造函数没有加上 `explicit` 关键字, 读者无法判断这一函数究竟是要作为隐式类型转换, 还是作者忘了加上 `explicit` 标记.
> - 并没有明确的方法用来判断哪个类应该提供类型转换, 这会使得代码变得含糊不清.
> - 如果目的类型是隐式指定的, 那么列表初始化会出现和隐式类型转换一样的问题, 尤其是在列表中只有一个元素的时候.

**结论**

> 在类型定义中, 类型转换运算符和单参数构造函数都应当用 `explicit` 进行标记. 一个例外是, 拷贝和移动构造函数不应当被标记为 `explicit`, 因为它们并不执行类型转换. 对于设计目的就是用于对其他类型进行透明包装的类来说, 隐式类型转换有时是必要且合适的. 这时应当联系项目组长并说明特殊情况.
>
> 不能以一个参数进行调用的构造函数不应当加上 `explicit`. 接受一个 `std::initializer_list` 作为参数的构造函数也应当省略 `explicit`, 以便支持拷贝初始化 (例如 `MyType m = {1, 2};`).

## 7. 命名约定

### 7.1 通用命名规则

**总述**

函数命名, 变量命名, 文件命名要有描述性; 少用缩写.

**说明**

尽可能使用描述性的命名, 别心疼空间, 毕竟相比之下让代码易于新读者理解更重要. 不要用只有项目开发者能理解的缩写, 也不要通过砍掉几个字母来缩写单词.

```
int price_count_reader;    // 无缩写
int num_errors;            // "num" 是一个常见的写法
int num_dns_connections;   // 人人都知道 "DNS" 是什么

int n;                     // 毫无意义.
int nerr;                  // 含糊不清的缩写.
int n_comp_conns;          // 含糊不清的缩写.
int wgc_connections;       // 只有贵团队知道是什么意思.
int pc_reader;             // "pc" 有太多可能的解释了.
int cstmr_id;              // 删减了若干字母.
```

注意, 一些特定的广为人知的缩写是允许的, 例如用 `i` 表示迭代变量和用 `T` 表示模板参数.

模板参数的命名应当遵循对应的分类: 类型模板参数应当遵循 [类型命名](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/naming/#type-names) 的规则, 而非类型模板应当遵循 [变量命名](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/naming/#variable-names) 的规则.

### 7.2 文件命名

**总述**

文件名要全部小写, 可以包含下划线 (`_`) 或连字符 (`-`), 依照项目的约定. 如果没有约定, 那么 “`_`” 更好.

**说明**

可接受的文件命名示例:

- `my_useful_class.cc`
- `my-useful-class.cc`
- `myusefulclass.cc`
- `myusefulclass_test.cc` // `_unittest` 和 `_regtest` 已弃用.

C++ 文件要以 `.cc` 结尾, 头文件以 `.h` 结尾. 专门插入文本的文件则以 `.inc` 结尾, 参见 [头文件自足](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/headers/#self-contained-headers).

不要使用已经存在于 `/usr/include` 下的文件名 (Yang.Y 注: 即编译器搜索系统头文件的路径), 如 `db.h`.

通常应尽量让文件名更加明确. `http_server_logs.h` 就比 `logs.h` 要好. 定义类时文件名一般成对出现, 如 `foo_bar.h` 和 `foo_bar.cc`, 对应于类 `FooBar`.

内联函数必须放在 `.h` 文件中. 如果内联函数比较短, 就直接放在 `.h` 中.

### 7.3 类型命名(驼峰)

**总述**

类型名称的每个单词首字母均大写, 不包含下划线: `MyExcitingClass`, `MyExcitingEnum`.

**说明**

所有类型命名 —— 类, 结构体, 类型定义 (`typedef`), 枚举, 类型模板参数 —— 均使用相同约定, 即以大写字母开始, 每个单词首字母均大写, 不包含下划线. 例如:

```
// 类和结构体
class UrlTable { ...
class UrlTableTester { ...
struct UrlTableProperties { ...

// 类型定义
typedef hash_map<UrlTableProperties *, string> PropertiesMap;

// using 别名
using PropertiesMap = hash_map<UrlTableProperties *, string>;

// 枚举
enum UrlTableErrors { ...
```

### 7.4 变量命名

**总述**

变量 (包括函数参数) 和数据成员名一律小写, 单词之间用下划线连接. **类的成员变量以下划线结尾**, 但结构体的就不用, 如: `a_local_variable`, `a_struct_data_member`, `a_class_data_member_`.

**说明**

#### 普通变量命名	

举例:

```
string table_name;  // 好 - 用下划线.
string tablename;   // 好 - 全小写.

string tableName;  // 差 - 混合大小写
```

#### 类数据成员

不管是静态的还是非静态的, 类数据成员都可以和普通变量一样, 但要接下划线.

```
class TableInfo {
  ...
 private:
  string table_name_;  // 好 - 后加下划线.
  string tablename_;   // 好.
  static Pool<TableInfo>* pool_;  // 好.
};
```

#### 结构体变量

不管是静态的还是非静态的, 结构体数据成员都可以和普通变量一样, 不用像类那样接下划线:

```
struct UrlTableProperties {
  string name;
  int num_entries;
  static Pool<UrlTableProperties>* pool;
};
```

结构体与类的使用讨论, 参考 [结构体 vs. 类](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/classes/#structs-vs-classes).

### 7.5 常量命名

**总述**

声明为 `constexpr` 或 `const` 的变量, 或在程序运行期间其值始终保持不变的, 命名时以 “k” 开头, 大小写混合. 例如:

```
const int kDaysInAWeek = 7;
```

**说明**

所有具有静态存储类型的变量 (例如静态变量或全局变量, 参见 [存储类型](http://en.cppreference.com/w/cpp/language/storage_duration#Storage_duration)) 都应当以此方式命名. 对于其他存储类型的变量, 如自动变量等, 这条规则是可选的. 如果不采用这条规则, 就按照一般的变量命名规则.

### 7.6 函数命名

**总述**

**常规函数使用大小写混合, 取值和设值函数则要求与变量名匹配**: `MyExcitingFunction()`, `MyExcitingMethod()`, `my_exciting_member_variable()`, `set_my_exciting_member_variable()`.

**说明**

一般来说, 函数名的每个单词首字母大写 (即 “驼峰变量名” 或 “帕斯卡变量名”), 没有下划线. 对于首字母缩写的单词, 更倾向于将它们视作一个单词进行首字母大写 (例如, 写作 `StartRpc()` 而非 `StartRPC()`).

```
AddTableEntry()
DeleteUrl()
OpenFileOrDie()
```

(同样的命名规则同时适用于类作用域与命名空间作用域的常量, 因为它们是作为 API 的一部分暴露对外的, 因此应当让它们看起来像是一个函数, 因为在这时, 它们实际上是一个对象而非函数的这一事实对外不过是一个无关紧要的实现细节.)

取值和设值函数的命名与变量一致. 一般来说它们的名称与实际的成员变量对应, 但并不强制要求. 例如 `int count()` 与 `void set_count(int count)`.

### 7.7 命名空间命名

**总述**

命名空间以小写字母命名. 最高级命名空间的名字取决于项目名称. 要注意避免嵌套命名空间的名字之间和常见的顶级命名空间的名字之间发生冲突.

顶级命名空间的名称应当是项目名或者是该命名空间中的代码所属的团队的名字. 命名空间中的代码, 应当存放于和命名空间的名字匹配的文件夹或其子文件夹中.

注意 [不使用缩写作为名称](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/naming/#general-naming-rules) 的规则同样适用于命名空间. 命名空间中的代码极少需要涉及命名空间的名称, 因此没有必要在命名空间中使用缩写.

要避免嵌套的命名空间与常见的顶级命名空间发生名称冲突. 由于名称查找规则的存在, 命名空间之间的冲突完全有可能导致编译失败. 尤其是, 不要创建嵌套的 `std` 命名空间. 建议使用更独特的项目标识符 (`websearch::index`, `websearch::index_util`) 而非常见的极易发生冲突的名称 (比如 `websearch::util`).

对于 `internal` 命名空间, 要当心加入到同一 `internal` 命名空间的代码之间发生冲突 (由于内部维护人员通常来自同一团队, 因此常有可能导致冲突). 在这种情况下, 请使用文件名以使得内部名称独一无二 (例如对于 `frobber.h`, 使用 `websearch::index::frobber_internal`).

### 7.8 枚举命名

**总述**

枚举的命名应当和 [常量](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/naming/#constant-names) 或 [宏](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/naming/#macro-names) 一致: `kEnumName` 或是 `ENUM_NAME`.

**说明**

单独的枚举值应该优先采用 [常量](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/naming/#constant-names) 的命名方式. 但 [宏](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/naming/#macro-names) 方式的命名也可以接受. 枚举名 `UrlTableErrors` (以及 `AlternateUrlTableErrors`) 是类型, 所以要用大小写混合的方式.

```
enum UrlTableErrors {
    kOK = 0,
    kErrorOutOfMemory,
    kErrorMalformedInput,
};
enum AlternateUrlTableErrors {
    OK = 0,
    OUT_OF_MEMORY = 1,
    MALFORMED_INPUT = 2,
};
```

2009 年 1 月之前, 我们一直建议采用 [宏](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/naming/#macro-names) 的方式命名枚举值. 由于枚举值和宏之间的命名冲突, 直接导致了很多问题. 由此, 这里改为优先选择常量风格的命名方式. 新代码应该尽可能优先使用常量风格. 但是老代码没必要切换到常量风格, 除非宏风格确实会产生编译期问题.

### 7.9 宏命名

**总述**

你并不打算 [使用宏](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/others/#preprocessor-macros), 对吧? 如果你一定要用, 像这样命名: `MY_MACRO_THAT_SCARES_SMALL_CHILDREN`.

**说明**

参考 [预处理宏](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/others/#preprocessor-macros); 通常 *不应该* 使用宏. 如果不得不用, 其命名像枚举命名一样全部大写, 使用下划线:

```c++
#define ROUND(x) ...
#define PI_ROUNDED 3.0
```

### 7.10  命名规则的特例

**总述**

如果你命名的实体与已有 C/C++ 实体相似, 可参考现有命名策略.

`bigopen()`: 函数名, 参照 `open()` 的形式

```
uint`: `typedef
```

`bigpos`: `struct` 或 `class`, 参照 `pos` 的形式

`sparse_hash_map`: STL 型实体; 参照 STL 命名约定

```
LONGLONG_MAX`: 常量, 如同 `INT_MAX
```

## 8. 注释

### 8.1 注释风格

**总述**

使用 `//` 或 `/* */`, 统一就好.

**说明**

`//` 或 `/* */` 都可以; 但 `//` *更* 常用. 要在如何注释及注释风格上确保统一.

### 8.2. 文件注释

**总述**

在每一个文件开头加入版权公告.

文件注释描述了该文件的内容. 如果一个文件只声明, 或实现, 或测试了一个对象, 并且这个对象已经在它的声明处进行了详细的注释, 那么就没必要再加上文件注释. 除此之外的其他文件都需要文件注释.

**说明**

#### 法律公告和作者信息

每个文件都应该包含许可证引用. 为项目选择合适的许可证版本.(比如, Apache 2.0, BSD, LGPL, GPL)

如果你对原始作者的文件做了重大修改, 请考虑删除原作者信息.

#### 文件内容

如果一个 `.h` 文件声明了多个概念, 则文件注释应当对文件的内容做一个大致的说明, 同时说明各概念之间的联系. 一个一到两行的文件注释就足够了, 对于每个概念的详细文档应当放在各个概念中, 而不是文件注释中.

不要在 `.h` 和 `.cc` 之间复制注释, 这样的注释偏离了注释的实际意义.

### 8.3. 类注释

**总述**

每个类的定义都要附带一份注释, 描述类的功能和用法, 除非它的功能相当明显.

```
// Iterates over the contents of a GargantuanTable.
// Example:
//    GargantuanTableIterator* iter = table->NewIterator();
//    for (iter->Seek("foo"); !iter->done(); iter->Next()) {
//      process(iter->key(), iter->value());
//    }
//    delete iter;
class GargantuanTableIterator {
  ...
};
```

**说明**

类注释应当为读者理解如何使用与何时使用类提供足够的信息, 同时应当提醒读者在正确使用此类时应当考虑的因素. 如果类有任何同步前提, 请用文档说明. 如果该类的实例可被多线程访问, 要特别注意文档说明多线程环境下相关的规则和常量使用.

如果你想用一小段代码演示这个类的基本用法或通常用法, 放在类注释里也非常合适.

如果类的声明和定义分开了(例如分别放在了 `.h` 和 `.cc` 文件中), 此时, 描述类用法的注释应当和接口定义放在一起, 描述类的操作和实现的注释应当和实现放在一起.

### 8.4. 函数注释

**总述**

函数声明处的注释描述函数功能; 定义处的注释描述函数实现.

**说明**

#### 函数声明

基本上每个函数声明处前都应当加上注释, 描述函数的功能和用途. 只有在函数的功能简单而明显时才能省略这些注释(例如, 简单的取值和设值函数). 注释使用叙述式 (“Opens the file”) 而非指令式 (“Open the file”); 注释只是为了描述函数, 而不是命令函数做什么. 通常, 注释不会描述函数如何工作. 那是函数定义部分的事情.

函数声明处注释的内容:

- 函数的输入输出.
- 对类成员函数而言: 函数调用期间对象是否需要保持引用参数, 是否会释放这些参数.
- 函数是否分配了必须由调用者释放的空间.
- 参数是否可以为空指针.
- 是否存在函数使用上的性能隐患.
- 如果函数是可重入的, 其同步前提是什么?

举例如下:

```
// Returns an iterator for this table.  It is the client's
// responsibility to delete the iterator when it is done with it,
// and it must not use the iterator once the GargantuanTable object
// on which the iterator was created has been deleted.
//
// The iterator is initially positioned at the beginning of the table.
//
// This method is equivalent to:
//    Iterator* iter = table->NewIterator();
//    iter->Seek("");
//    return iter;
// If you are going to immediately seek to another place in the
// returned iterator, it will be faster to use NewIterator()
// and avoid the extra seek.
Iterator* GetIterator() const;
```

但也要避免罗罗嗦嗦, 或者对显而易见的内容进行说明. 下面的注释就没有必要加上 “否则返回 false”, 因为已经暗含其中了:

```
// Returns true if the table cannot hold any more entries.
bool IsTableFull();
```

注释函数重载时, 注释的重点应该是函数中被重载的部分, 而不是简单的重复被重载的函数的注释. 多数情况下, 函数重载不需要额外的文档, 因此也没有必要加上注释.

注释构造/析构函数时, 切记读代码的人知道构造/析构函数的功能, 所以 “销毁这一对象” 这样的注释是没有意义的. 你应当注明的是注明构造函数对参数做了什么 (例如, 是否取得指针所有权) 以及析构函数清理了什么. 如果都是些无关紧要的内容, 直接省掉注释. 析构函数前没有注释是很正常的.

#### 函数定义

如果函数的实现过程中用到了很巧妙的方式, 那么在函数定义处应当加上解释性的注释. 例如, 你所使用的编程技巧, 实现的大致步骤, 或解释如此实现的理由. 举个例子, 你可以说明为什么函数的前半部分要加锁而后半部分不需要.

*不要* 从 `.h` 文件或其他地方的函数声明处直接复制注释. 简要重述函数功能是可以的, 但注释重点要放在如何实现上.

### 8.5. 变量注释

**总述**

通常变量名本身足以很好说明变量用途. 某些情况下, 也需要额外的注释说明.

**说明**

#### 类数据成员

每个类数据成员 (也叫实例变量或成员变量) 都应该用注释说明用途. 如果有非变量的参数(例如特殊值, 数据成员之间的关系, 生命周期等)不能够用类型与变量名明确表达, 则应当加上注释. 然而, 如果变量类型与变量名已经足以描述一个变量, 那么就不再需要加上注释.

特别地, 如果变量可以接受 `NULL` 或 `-1` 等警戒值, 须加以说明. 比如:

```
private:
 // Used to bounds-check table accesses. -1 means
 // that we don't yet know how many entries the table has.
 int num_total_entries_;
```

#### 全局变量

和数据成员一样, 所有全局变量也要注释说明含义及用途, 以及作为全局变量的原因. 比如:

```
// The total number of tests cases that we run through in this regression test.
const int kNumTestCases = 6;
```

### 8.6. 实现注释

**总述**

对于代码中巧妙的, 晦涩的, 有趣的, 重要的地方加以注释.

**说明**

#### 代码前注释

巧妙或复杂的代码段前要加注释. 比如:

```
// Divide result by two, taking into account that x
// contains the carry from the add.
for (int i = 0; i < result->size(); i++) {
  x = (x << 8) + (*result)[i];
  (*result)[i] = x >> 1;
  x &= 1;
}
```

#### 行注释

比较隐晦的地方要在行尾加入注释. 在行尾空两格进行注释. 比如:

```
// If we have enough memory, mmap the data portion too.
mmap_budget = max<int64>(0, mmap_budget - index_->length());
if (mmap_budget >= data_size_ && !MmapData(mmap_chunk_bytes, mlock))
  return;  // Error already logged.
```

注意, 这里用了两段注释分别描述这段代码的作用, 和提示函数返回时错误已经被记入日志.

如果你需要连续进行多行注释, 可以使之对齐获得更好的可读性:

```
DoSomething();                  // Comment here so the comments line up.
DoSomethingElseThatIsLonger();  // Two spaces between the code and the comment.
{ // One space before comment when opening a new scope is allowed,
  // thus the comment lines up with the following comments and code.
  DoSomethingElse();  // Two spaces before line comments normally.
}
std::vector<string> list{
                    // Comments in braced lists describe the next element...
                    "First item",
                    // .. and should be aligned appropriately.
"Second item"};
DoSomething(); /* For trailing block comments, one space is fine. */
```

#### 函数参数注释

如果函数参数的意义不明显, 考虑用下面的方式进行弥补:

- 如果参数是一个字面常量, 并且这一常量在多处函数调用中被使用, 用以推断它们一致, 你应当用一个常量名让这一约定变得更明显, 并且保证这一约定不会被打破.
- 考虑更改函数的签名, 让某个 `bool` 类型的参数变为 `enum` 类型, 这样可以让这个参数的值表达其意义.
- 如果某个函数有多个配置选项, 你可以考虑定义一个类或结构体以保存所有的选项, 并传入类或结构体的实例. 这样的方法有许多优点, 例如这样的选项可以在调用处用变量名引用, 这样就能清晰地表明其意义. 同时也减少了函数参数的数量, 使得函数调用更易读也易写. 除此之外, 以这样的方式, 如果你使用其他的选项, 就无需对调用点进行更改.
- 用具名变量代替大段而复杂的嵌套表达式.
- 万不得已时, 才考虑在调用点用注释阐明参数的意义.

比如下面的示例的对比:

```
// What are these arguments?
const DecimalNumber product = CalculateProduct(values, 7, false, nullptr);
```

和

```
ProductOptions options;
options.set_precision_decimals(7);
options.set_use_cache(ProductOptions::kDontUseCache);
const DecimalNumber product =
    CalculateProduct(values, options, /*completion_callback=*/nullptr);
```

哪个更清晰一目了然.

#### 不允许的行为

不要描述显而易见的现象, *永远不要* 用自然语言翻译代码作为注释, 除非即使对深入理解 C++ 的读者来说代码的行为都是不明显的. 要假设读代码的人 C++ 水平比你高, 即便他/她可能不知道你的用意:

你所提供的注释应当解释代码 *为什么* 要这么做和代码的目的, 或者最好是让代码自文档化.

比较这样的注释:

```
// Find the element in the vector.  <-- 差: 这太明显了!
auto iter = std::find(v.begin(), v.end(), element);
if (iter != v.end()) {
  Process(element);
}
```

和这样的注释:

```
// Process "element" unless it was already processed.
auto iter = std::find(v.begin(), v.end(), element);
if (iter != v.end()) {
  Process(element);
}
```

自文档化的代码根本就不需要注释. 上面例子中的注释对下面的代码来说就是毫无必要的:

```
if (!IsAlreadyProcessed(element)) {
  Process(element);
}
```

### 8.7. 标点, 拼写和语法

**总述**

注意标点, 拼写和语法; 写的好的注释比差的要易读的多.

**说明**

注释的通常写法是包含正确大小写和结尾句号的完整叙述性语句. 大多数情况下, 完整的句子比句子片段可读性更高. 短一点的注释, 比如代码行尾注释, 可以随意点, 但依然要注意风格的一致性.

虽然被别人指出该用分号时却用了逗号多少有些尴尬, 但清晰易读的代码还是很重要的. 正确的标点, 拼写和语法对此会有很大帮助.

### 8.8. TODO 注释

**总述**

对那些临时的, 短期的解决方案, 或已经够好但仍不完美的代码使用 `TODO` 注释.

`TODO` 注释要使用全大写的字符串 `TODO`, 在随后的圆括号里写上你的名字, 邮件地址, bug ID, 或其它身份标识和与这一 `TODO` 相关的 issue. 主要目的是让添加注释的人 (也是可以请求提供更多细节的人) 可根据规范的 `TODO` 格式进行查找. 添加 `TODO` 注释并不意味着你要自己来修正, 因此当你加上带有姓名的 `TODO` 时, 一般都是写上自己的名字.

```
// TODO(kl@gmail.com): Use a "*" here for concatenation operator.
// TODO(Zeke) change this to use relations.
// TODO(bug 12345): remove the "Last visitors" feature
```

如果加 `TODO` 是为了在 “将来某一天做某事”, 可以附上一个非常明确的时间 “Fix by November 2005”), 或者一个明确的事项 (“Remove this code when all clients can handle XML responses.”).

### 8.9. 弃用注释

**总述**

通过弃用注释（`DEPRECATED` comments）以标记某接口点已弃用.

您可以写上包含全大写的 `DEPRECATED` 的注释, 以标记某接口为弃用状态. 注释可以放在接口声明前, 或者同一行.

在 `DEPRECATED` 一词后, 在括号中留下您的名字, 邮箱地址以及其他身份标识.

弃用注释应当包涵简短而清晰的指引, 以帮助其他人修复其调用点. 在 C++ 中, 你可以将一个弃用函数改造成一个内联函数, 这一函数将调用新的接口.

仅仅标记接口为 `DEPRECATED` 并不会让大家不约而同地弃用, 您还得亲自主动修正调用点（callsites）, 或是找个帮手.

修正好的代码应该不会再涉及弃用接口点了, 着实改用新接口点. 如果您不知从何下手, 可以找标记弃用注释的当事人一起商量.

### 译者 (YuleFox) 笔记

1. 关于注释风格, 很多 C++ 的 coders 更喜欢行注释, C coders 或许对块注释依然情有独钟, 或者在文件头大段大段的注释时使用块注释;
2. 文件注释可以炫耀你的成就, 也是为了捅了篓子别人可以找你;
3. 注释要言简意赅, 不要拖沓冗余, 复杂的东西简单化和简单的东西复杂化都是要被鄙视的;
4. 对于 Chinese coders 来说, 用英文注释还是用中文注释, it is a problem, 但不管怎样, 注释是为了让别人看懂, 难道是为了炫耀编程语言之外的你的母语或外语水平吗；
5. 注释不要太乱, 适当的缩进才会让人乐意看. 但也没有必要规定注释从第几列开始 (我自己写代码的时候总喜欢这样), UNIX/LINUX 下还可以约定是使用 tab 还是 space, 个人倾向于 space;
6. TODO 很不错, 有时候, 注释确实是为了标记一些未完成的或完成的不尽如人意的地方, 这样一搜索, 就知道还有哪些活要干, 日志都省了.

## 9. 格式

### 9.1. 行长度

**总述**

每一行代码字符数不超过 80.

我们也认识到这条规则是有争议的, 但很多已有代码都遵照这一规则, 因此我们感觉一致性更重要.

**优点**

提倡该原则的人认为强迫他们调整编辑器窗口大小是很野蛮的行为. 很多人同时并排开几个代码窗口, 根本没有多余的空间拉伸窗口. 大家都把窗口最大尺寸加以限定, 并且 80 列宽是传统标准. 那么为什么要改变呢?

**缺点**

反对该原则的人则认为更宽的代码行更易阅读. 80 列的限制是上个世纪 60 年代的大型机的古板缺陷; 现代设备具有更宽的显示屏, 可以很轻松地显示更多代码.

**结论**

80 个字符是最大值.

如果无法在不伤害易读性的条件下进行断行, 那么注释行可以超过 80 个字符, 这样可以方便复制粘贴. 例如, 带有命令示例或 URL 的行可以超过 80 个字符.

包含长路径的 `#include` 语句可以超出80列.

[头文件保护](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/headers/#define-guard) 可以无视该原则.

### 9.2. 非 ASCII 字符

**总述**

尽量不使用非 ASCII 字符, 使用时必须使用 UTF-8 编码.

**说明**

即使是英文, 也不应将用户界面的文本硬编码到源代码中, 因此非 ASCII 字符应当很少被用到. 特殊情况下可以适当包含此类字符. 例如, 代码分析外部数据文件时, 可以适当硬编码数据文件中作为分隔符的非 ASCII 字符串; 更常见的是 (不需要本地化的) 单元测试代码可能包含非 ASCII 字符串. 此类情况下, 应使用 UTF-8 编码, 因为很多工具都可以理解和处理 UTF-8 编码.

十六进制编码也可以, 能增强可读性的情况下尤其鼓励 —— 比如 `"\xEF\xBB\xBF"`, 或者更简洁地写作 `u8"\uFEFF"`, 在 Unicode 中是 *零宽度 无间断* 的间隔符号, 如果不用十六进制直接放在 UTF-8 格式的源文件中, 是看不到的.

(Yang.Y 注: `"\xEF\xBB\xBF"` 通常用作 UTF-8 with BOM 编码标记)

使用 `u8` 前缀把带 `uXXXX` 转义序列的字符串字面值编码成 UTF-8. 不要用在本身就带 UTF-8 字符的字符串字面值上, 因为如果编译器不把源代码识别成 UTF-8, 输出就会出错.

别用 C++11 的 `char16_t` 和 `char32_t`, 它们和 UTF-8 文本没有关系, `wchar_t` 同理, 除非你写的代码要调用 Windows API, 后者广泛使用了 `wchar_t`.

### 9.3. 空格还是制表位

**总述**

只使用空格, 每次缩进 2 个空格.

**说明**

我们使用空格缩进. 不要在代码中使用制表符. 你应该设置编辑器将制表符转为空格.

### 9.4. 函数声明与定义

**总述**

返回类型和函数名在同一行, 参数也尽量放在同一行, 如果放不下就对形参分行, 分行方式与 [函数调用](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/formatting/#function-calls) 一致.

**说明**

函数看上去像这样:

```
ReturnType ClassName::FunctionName(Type par_name1, Type par_name2) {
  DoSomething();
  ...
}
```

如果同一行文本太多, 放不下所有参数:

```
ReturnType ClassName::ReallyLongFunctionName(Type par_name1, Type par_name2,
                                             Type par_name3) {
  DoSomething();
  ...
}
```

甚至连第一个参数都放不下:

```
ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
    Type par_name1,  // 4 space indent
    Type par_name2,
    Type par_name3) {
  DoSomething();  // 2 space indent
  ...
}
```

注意以下几点:

- 使用好的参数名.
- 只有在参数未被使用或者其用途非常明显时, 才能省略参数名.
- 如果返回类型和函数名在一行放不下, 分行.
- 如果返回类型与函数声明或定义分行了, 不要缩进.
- 左圆括号总是和函数名在同一行.
- 函数名和左圆括号间永远没有空格.
- 圆括号与参数间没有空格.
- 左大括号总在最后一个参数同一行的末尾处, 不另起新行.
- 右大括号总是单独位于函数最后一行, 或者与左大括号同一行.
- 右圆括号和左大括号间总是有一个空格.
- 所有形参应尽可能对齐.
- 缺省缩进为 2 个空格.
- 换行后的参数保持 4 个空格的缩进.

未被使用的参数, 或者根据上下文很容易看出其用途的参数, 可以省略参数名:

```
class Foo {
 public:
  Foo(Foo&&);
  Foo(const Foo&);
  Foo& operator=(Foo&&);
  Foo& operator=(const Foo&);
};
```

未被使用的参数如果其用途不明显的话, 在函数定义处将参数名注释起来:

```
class Shape {
 public:
  virtual void Rotate(double radians) = 0;
};

class Circle : public Shape {
 public:
  void Rotate(double radians) override;
};

void Circle::Rotate(double /*radians*/) {}

// 差 - 如果将来有人要实现, 很难猜出变量的作用.
void Circle::Rotate(double) {}
```

属性, 和展开为属性的宏, 写在函数声明或定义的最前面, 即返回类型之前:

```
MUST_USE_RESULT bool IsOK();
```

### 9.5. Lambda 表达式

**总述**

Lambda 表达式对形参和函数体的格式化和其他函数一致; 捕获列表同理, 表项用逗号隔开.

**说明**

若用引用捕获, 在变量名和 `&` 之间不留空格.

```
int x = 0;
auto add_to_x = [&x](int n) { x += n; };
```

短 lambda 就写得和内联函数一样.

```
std::set<int> blacklist = {7, 8, 9};
std::vector<int> digits = {3, 9, 1, 8, 4, 7, 1};
digits.erase(std::remove_if(digits.begin(), digits.end(), [&blacklist](int i) {
               return blacklist.find(i) != blacklist.end();
             }),
             digits.end());
```

### 9.6. 函数调用

**总述**

要么一行写完函数调用, 要么在圆括号里对参数分行, 要么参数另起一行且缩进四格. 如果没有其它顾虑的话, 尽可能精简行数, 比如把多个参数适当地放在同一行里.

**说明**

函数调用遵循如下形式：

```
bool retval = DoSomething(argument1, argument2, argument3);
```

如果同一行放不下, 可断为多行, 后面每一行都和第一个实参对齐, 左圆括号后和右圆括号前不要留空格：

```
bool retval = DoSomething(averyveryveryverylongargument1,
                          argument2, argument3);
```

参数也可以放在次行, 缩进四格：

```
if (...) {
  ...
  ...
  if (...) {
    DoSomething(
        argument1, argument2,  // 4 空格缩进
        argument3, argument4);
  }
```

把多个参数放在同一行以减少函数调用所需的行数, 除非影响到可读性. 有人认为把每个参数都独立成行, 不仅更好读, 而且方便编辑参数. 不过, 比起所谓的参数编辑, 我们更看重可读性, 且后者比较好办：

如果一些参数本身就是略复杂的表达式, 且降低了可读性, 那么可以直接创建临时变量描述该表达式, 并传递给函数：

```
int my_heuristic = scores[x] * y + bases[x];
bool retval = DoSomething(my_heuristic, x, y, z);
```

或者放着不管, 补充上注释：

```
bool retval = DoSomething(scores[x] * y + bases[x],  // Score heuristic.
                          x, y, z);
```

如果某参数独立成行, 对可读性更有帮助的话, 那也可以如此做. 参数的格式处理应当以可读性而非其他作为最重要的原则.

此外, 如果一系列参数本身就有一定的结构, 可以酌情地按其结构来决定参数格式：

```
// 通过 3x3 矩阵转换 widget.
my_widget.Transform(x1, x2, x3,
                    y1, y2, y3,
                    z1, z2, z3);
```

### 9.7. 列表初始化格式

**总述**

您平时怎么格式化函数调用, 就怎么格式化 [列表初始化](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/others/#braced-initializer-list).

**说明**

如果列表初始化伴随着名字, 比如类型或变量名, 格式化时将将名字视作函数调用名, {} 视作函数调用的括号. 如果没有名字, 就视作名字长度为零.

```
// 一行列表初始化示范.
return {foo, bar};
functioncall({foo, bar});
pair<int, int> p{foo, bar};

// 当不得不断行时.
SomeFunction(
    {"assume a zero-length name before {"},  // 假设在 { 前有长度为零的名字.
    some_other_function_parameter);
SomeType variable{
    some, other, values,
    {"assume a zero-length name before {"},  // 假设在 { 前有长度为零的名字.
    SomeOtherType{
        "Very long string requiring the surrounding breaks.",  // 非常长的字符串, 前后都需要断行.
        some, other values},
    SomeOtherType{"Slightly shorter string",  // 稍短的字符串.
                  some, other, values}};
SomeType variable{
    "This is too long to fit all in one line"};  // 字符串过长, 因此无法放在同一行.
MyType m = {  // 注意了, 您可以在 { 前断行.
    superlongvariablename1,
    superlongvariablename2,
    {short, interior, list},
    {interiorwrappinglist,
     interiorwrappinglist2}};
```

### 9.8. 条件语句

**总述**

倾向于不在圆括号内使用空格. 关键字 `if` 和 `else` 另起一行.

**说明**

对基本条件语句有两种可以接受的格式. 一种在圆括号和条件之间有空格, 另一种没有.

最常见的是没有空格的格式. 哪一种都可以, 最重要的是 *保持一致*. 如果你是在修改一个文件, 参考当前已有格式. 如果是写新的代码, 参考目录下或项目中其它文件. 还在犹豫的话, 就不要加空格了.

```
if (condition) {  // 圆括号里没有空格.
  ...  // 2 空格缩进.
} else if (...) {  // else 与 if 的右括号同一行.
  ...
} else {
  ...
}
```

如果你更喜欢在圆括号内部加空格:

```
if ( condition ) {  // 圆括号与空格紧邻 - 不常见
  ...  // 2 空格缩进.
} else {  // else 与 if 的右括号同一行.
  ...
}
```

注意所有情况下 `if` 和左圆括号间都有个空格. 右圆括号和左大括号之间也要有个空格:

```
if(condition)     // 差 - IF 后面没空格.
if (condition){   // 差 - { 前面没空格.
if(condition){    // 变本加厉地差.
if (condition) {  // 好 - IF 和 { 都与空格紧邻.
```

如果能增强可读性, 简短的条件语句允许写在同一行. 只有当语句简单并且没有使用 `else` 子句时使用:

```
if (x == kFoo) return new Foo();
if (x == kBar) return new Bar();
```

如果语句有 `else` 分支则不允许:

```
// 不允许 - 当有 ELSE 分支时 IF 块却写在同一行
if (x) DoThis();
else DoThat();
```

通常, 单行语句不需要使用大括号, 如果你喜欢用也没问题; 复杂的条件或循环语句用大括号可读性会更好. 也有一些项目要求 `if` 必须总是使用大括号:

```
if (condition)
  DoSomething();  // 2 空格缩进.

if (condition) {
  DoSomething();  // 2 空格缩进.
}
```

但如果语句中某个 `if-else` 分支使用了大括号的话, 其它分支也必须使用:

```
// 不可以这样子 - IF 有大括号 ELSE 却没有.
if (condition) {
  foo;
} else
  bar;

// 不可以这样子 - ELSE 有大括号 IF 却没有.
if (condition)
  foo;
else {
  bar;
}
// 只要其中一个分支用了大括号, 两个分支都要用上大括号.
if (condition) {
  foo;
} else {
  bar;
}
```

### 9.9. 循环和开关选择语句

**总述**

`switch` 语句可以使用大括号分段, 以表明 cases 之间不是连在一起的. 在单语句循环里, 括号可用可不用. 空循环体应使用 `{}` 或 `continue`.

**说明**

`switch` 语句中的 `case` 块可以使用大括号也可以不用, 取决于你的个人喜好. 如果用的话, 要按照下文所述的方法.

如果有不满足 `case` 条件的枚举值, `switch` 应该总是包含一个 `default` 匹配 (如果有输入值没有 case 去处理, 编译器将给出 warning). 如果 `default` 应该永远执行不到, 简单的加条 `assert`:

```
switch (var) {
  case 0: {  // 2 空格缩进
    ...      // 4 空格缩进
    break;
  }
  case 1: {
    ...
    break;
  }
  default: {
    assert(false);
  }
}
```

在单语句循环里, 括号可用可不用：

```
for (int i = 0; i < kSomeNumber; ++i)
  printf("I love you\n");

for (int i = 0; i < kSomeNumber; ++i) {
  printf("I take it back\n");
}
```

空循环体应使用 `{}` 或 `continue`, 而不是一个简单的分号.

```
while (condition) {
  // 反复循环直到条件失效.
}
for (int i = 0; i < kSomeNumber; ++i) {}  // 可 - 空循环体.
while (condition) continue;  // 可 - contunue 表明没有逻辑.
while (condition);  // 差 - 看起来仅仅只是 while/loop 的部分之一.
```

### 9.10. 指针和引用表达式

**总述**

句点或箭头前后不要有空格. 指针/地址操作符 (`*, &`) 之后不能有空格.

**说明**

下面是指针和引用表达式的正确使用范例:

```
x = *p;
p = &x;
x = r.y;
x = r->y;
```

注意:

- 在访问成员时, 句点或箭头前后没有空格.
- 指针操作符 `*` 或 `&` 后没有空格.

在声明指针变量或参数时, 星号与类型或变量名紧挨都可以:

```
// 好, 空格前置.
char *c;
const string &str;

// 好, 空格后置.
char* c;
const string& str;
int x, *y;  // 不允许 - 在多重声明中不能使用 & 或 *
char * c;  // 差 - * 两边都有空格
const string & str;  // 差 - & 两边都有空格.
```

在单个文件内要保持风格一致, 所以, 如果是修改现有文件, 要遵照该文件的风格.

### 9.11. 布尔表达式

**总述**

如果一个布尔表达式超过 [标准行宽](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/formatting/#line-length), 断行方式要统一一下.

**说明**

下例中, 逻辑与 (`&&`) 操作符总位于行尾:

```
if (this_one_thing > this_other_thing &&
    a_third_thing == a_fourth_thing &&
    yet_another && last_one) {
  ...
}
```

注意, 上例的逻辑与 (`&&`) 操作符均位于行尾. 这个格式在 Google 里很常见, 虽然把所有操作符放在开头也可以. 可以考虑额外插入圆括号, 合理使用的话对增强可读性是很有帮助的. 此外, 直接用符号形式的操作符, 比如 `&&` 和 `~`, 不要用词语形式的 `and` 和 `compl`.

### 9.12. 函数返回值

**总述**

不要在 `return` 表达式里加上非必须的圆括号.

**说明**

只有在写 `x = expr` 要加上括号的时候才在 `return expr;` 里使用括号.

```
return result;                  // 返回值很简单, 没有圆括号.
// 可以用圆括号把复杂表达式圈起来, 改善可读性.
return (some_long_condition &&
        another_condition);
        
return (value);                // 毕竟您从来不会写 var = (value);
return(result);                // return 可不是函数！
```

### 9.13. 变量及数组初始化

**总述**

用 `=`, `()` 和 `{}` 均可.

**说明**

您可以用 `=`, `()` 和 `{}`, 以下的例子都是正确的：

```
int x = 3;
int x(3);
int x{3};
string name("Some Name");
string name = "Some Name";
string name{"Some Name"};
```

请务必小心列表初始化 `{...}` 用 `std::initializer_list` 构造函数初始化出的类型. 非空列表初始化就会优先调用 `std::initializer_list`, 不过空列表初始化除外, 后者原则上会调用默认构造函数. 为了强制禁用 `std::initializer_list` 构造函数, 请改用括号.

```
vector<int> v(100, 1);  // 内容为 100 个 1 的向量.
vector<int> v{100, 1};  // 内容为 100 和 1 的向量.
```

此外, 列表初始化不允许整型类型的四舍五入, 这可以用来避免一些类型上的编程失误.

```
int pi(3.14);  // 好 - pi == 3.
int pi{3.14};  // 编译错误: 缩窄转换.
```

### 9.14. 预处理指令

**总述**

预处理指令不要缩进, 从行首开始.

**说明**

即使预处理指令位于缩进代码块中, 指令也应从行首开始.

```
// 好 - 指令从行首开始
  if (lopsided_score) {
#if DISASTER_PENDING      // 正确 - 从行首开始
    DropEverything();
# if NOTIFY               // 非必要 - # 后跟空格
    NotifyClient();
# endif
#endif
    BackToNormal();
  }
// 差 - 指令缩进
  if (lopsided_score) {
    #if DISASTER_PENDING  // 差 - "#if" 应该放在行开头
    DropEverything();
    #endif                // 差 - "#endif" 不要缩进
    BackToNormal();
  }
```

### 9.15. 类格式

**总述**

访问控制块的声明依次序是 `public:`, `protected:`, `private:`, 每个都缩进 1 个空格.

**说明**

类声明 (下面的代码中缺少注释, 参考 [类注释](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/comments/#class-comments)) 的基本格式如下:

```
class MyClass : public OtherClass {
 public:      // 注意有一个空格的缩进
  MyClass();  // 标准的两空格缩进
  explicit MyClass(int var);
  ~MyClass() {}

  void SomeFunction();
  void SomeFunctionThatDoesNothing() {
  }

  void set_some_var(int var) { some_var_ = var; }
  int some_var() const { return some_var_; }

 private:
  bool SomeInternalFunction();

  int some_var_;
  int some_other_var_;
};
```

注意事项:

- 所有基类名应在 80 列限制下尽量与子类名放在同一行.
- 关键词 `public:`, `protected:`, `private:` 要缩进 1 个空格.
- 除第一个关键词 (一般是 `public`) 外, 其他关键词前要空一行. 如果类比较小的话也可以不空.
- 这些关键词后不要保留空行.
- `public` 放在最前面, 然后是 `protected`, 最后是 `private`.
- 关于声明顺序的规则请参考 [声明顺序](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/classes/#declaration-order) 一节.

### 9.16. 构造函数初始值列表

**总述**

构造函数初始化列表放在同一行或按四格缩进并排多行.

**说明**

下面两种初始值列表方式都可以接受:

```
// 如果所有变量能放在同一行:
MyClass::MyClass(int var) : some_var_(var) {
  DoSomething();
}

// 如果不能放在同一行,
// 必须置于冒号后, 并缩进 4 个空格
MyClass::MyClass(int var)
    : some_var_(var), some_other_var_(var + 1) {
  DoSomething();
}

// 如果初始化列表需要置于多行, 将每一个成员放在单独的一行
// 并逐行对齐
MyClass::MyClass(int var)
    : some_var_(var),             // 4 space indent
      some_other_var_(var + 1) {  // lined up
  DoSomething();
}

// 右大括号 } 可以和左大括号 { 放在同一行
// 如果这样做合适的话
MyClass::MyClass(int var)
    : some_var_(var) {}
```

### 9.17. 命名空间格式化

**总述**

命名空间内容不缩进.

**说明**

[命名空间](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/scoping/#namespaces) 不要增加额外的缩进层次, 例如:

```
namespace {

void foo() {  // 正确. 命名空间内没有额外的缩进.
  ...
}

}  // namespace
```

不要在命名空间内缩进:

```
namespace {

  // 错, 缩进多余了.
  void foo() {
    ...
  }

}  // namespace
```

声明嵌套命名空间时, 每个命名空间都独立成行.

```
namespace foo {
namespace bar {
```

### 9.19. 水平留白

**总述**

水平留白的使用根据在代码中的位置决定. 永远不要在行尾添加没意义的留白.

**说明**

#### 通用

```
void f(bool b) {  // 左大括号前总是有空格.
  ...
int i = 0;  // 分号前不加空格.
// 列表初始化中大括号内的空格是可选的.
// 如果加了空格, 那么两边都要加上.
int x[] = { 0 };
int x[] = {0};

// 继承与初始化列表中的冒号前后恒有空格.
class Foo : public Bar {
 public:
  // 对于单行函数的实现, 在大括号内加上空格
  // 然后是函数实现
  Foo(int b) : Bar(), baz_(b) {}  // 大括号里面是空的话, 不加空格.
  void Reset() { baz_ = 0; }  // 用空格把大括号与实现分开.
  ...
```

添加冗余的留白会给其他人编辑时造成额外负担. 因此, 行尾不要留空格. 如果确定一行代码已经修改完毕, 将多余的空格去掉; 或者在专门清理空格时去掉（尤其是在没有其他人在处理这件事的时候). (Yang.Y 注: 现在大部分代码编辑器稍加设置后, 都支持自动删除行首/行尾空格, 如果不支持, 考虑换一款编辑器或 IDE)

#### 循环和条件语句

```
if (b) {          // if 条件语句和循环语句关键字后均有空格.
} else {          // else 前后有空格.
}
while (test) {}   // 圆括号内部不紧邻空格.
switch (i) {
for (int i = 0; i < 5; ++i) {
switch ( i ) {    // 循环和条件语句的圆括号里可以与空格紧邻.
if ( test ) {     // 圆括号, 但这很少见. 总之要一致.
for ( int i = 0; i < 5; ++i ) {
for ( ; i < 5 ; ++i) {  // 循环里内 ; 后恒有空格, ;  前可以加个空格.
switch (i) {
  case 1:         // switch case 的冒号前无空格.
    ...
  case 2: break;  // 如果冒号有代码, 加个空格.
```

#### 操作符

```
// 赋值运算符前后总是有空格.
x = 0;

// 其它二元操作符也前后恒有空格, 不过对于表达式的子式可以不加空格.
// 圆括号内部没有紧邻空格.
v = w * x + y / z;
v = w*x + y/z;
v = w * (x + z);

// 在参数和一元操作符之间不加空格.
x = -5;
++x;
if (x && !y)
  ...
```

#### 模板和转换

```
// 尖括号(< and >) 不与空格紧邻, < 前没有空格, > 和 ( 之间也没有.
vector<string> x;
y = static_cast<char*>(x);

// 在类型与指针操作符之间留空格也可以, 但要保持一致.
vector<char *> x;
```

### 9.19. 垂直留白

**总述**

垂直留白越少越好.

**说明**

这不仅仅是规则而是原则问题了: 不在万不得已, 不要使用空行. 尤其是: 两个函数定义之间的空行不要超过 2 行, 函数体首尾不要留空行, 函数体中也不要随意添加空行.

基本原则是: 同一屏可以显示的代码越多, 越容易理解程序的控制流. 当然, 过于密集的代码块和过于疏松的代码块同样难看, 这取决于你的判断. 但通常是垂直留白越少越好.

下面的规则可以让加入的空行更有效:

- 函数体内开头或结尾的空行可读性微乎其微.
- 在多重 if-else 块里加空行或许有点可读性.

### 译者 (YuleFox) 笔记

1. 对于代码格式, 因人, 系统而异各有优缺点, 但同一个项目中遵循同一标准还是有必要的;
2. 行宽原则上不超过 80 列, 把 22 寸的显示屏都占完, 怎么也说不过去;
3. 尽量不使用非 ASCII 字符, 如果使用的话, 参考 UTF-8 格式 (尤其是 UNIX/Linux 下, Windows 下可以考虑宽字符), 尽量不将字符串常量耦合到代码中, 比如独立出资源文件, 这不仅仅是风格问题了;
4. UNIX/Linux 下无条件使用空格, MSVC 的话使用 Tab 也无可厚非;
5. 函数参数, 逻辑条件, 初始化列表: 要么所有参数和函数名放在同一行, 要么所有参数并排分行;
6. 除函数定义的左大括号可以置于行首外, 包括函数/类/结构体/枚举声明, 各种语句的左大括号置于行尾, 所有右大括号独立成行;
7. `.`/`->` 操作符前后不留空格, `*`/`&` 不要前后都留, 一个就可, 靠左靠右依各人喜好;
8. 预处理指令/命名空间不使用额外缩进, 类/结构体/枚举/函数/语句使用缩进;
9. 初始化用 `=` 还是 `()` 依个人喜好, 统一就好;
10. `return` 不要加 `()`;
11. 水平/垂直留白不要滥用, 怎么易读怎么来.
12. 关于 UNIX/Linux 风格为什么要把左大括号置于行尾 (`.cc` 文件的函数实现处, 左大括号位于行首), 我的理解是代码看上去比较简约, 想想行首除了函数体被一对大括号封在一起之外, 只有右大括号的代码看上去确实也舒服; Windows 风格将左大括号置于行首的优点是匹配情况一目了然.

### 译者（acgtyrant）笔记

1. 80 行限制事实上有助于避免代码可读性失控, 比如超多重嵌套块, 超多重函数调用等等.
2. Linux 上设置好了 Locale 就几乎一劳永逸设置好所有开发环境的编码, 不像奇葩的 Windows.
3. Google 强调有一对 if-else 时, 不论有没有嵌套, 都要有大括号. Apple 正好 [有栽过跟头](http://coolshell.cn/articles/11112.html) .
4. 其实我主张指针／地址操作符与变量名紧邻, `int* a, b` vs `int *a, b`, 新手会误以为前者的 `b` 是 `int *` 变量, 但后者就不一样了, 高下立判.
5. 在这风格指南里我才刚知道 C++ 原来还有所谓的 [Alternative operator representations](http://en.cppreference.com/w/cpp/language/operator_alternative), 大概没人用吧.
6. 注意构造函数初始值列表（Constructer Initializer List）与列表初始化（Initializer List）是两码事, 我就差点混淆了它们的翻译.
7. 事实上, 如果您熟悉英语本身的书写规则, 就会发现该风格指南在格式上的规定与英语语法相当一脉相承. 比如普通标点符号和单词后面还有文本的话, 总会留一个空格; 特殊符号与单词之间就不用留了, 比如 `if (true)` 中的圆括号与 `true`.
8. 本风格指南没有明确规定 void 函数里要不要用 return 语句, 不过就 Google 开源项目 leveldb 并没有写; 此外从 [Is a blank return statement at the end of a function whos return type is void necessary?](http://stackoverflow.com/questions/9316717/is-a-blank-return-statement-at-the-end-of-a-function-whos-return-type-is-void-ne) 来看, `return;` 比 `return ;` 更约定俗成（事实上 cpplint 会对后者报错, 指出分号前有多余的空格）, 且可用来提前跳出函数栈.

# python

## python 语言规范

### 导入

Tip

仅对包和模块使用导入,而不单独导入函数或者类。`typing`模块例外。

- 定义:

  模块间共享代码的重用机制.

- 优点:

  命名空间管理约定十分简单. 每个标识符的源都用一种一致的方式指示. x.Obj表示Obj对象定义在模块x中.

- 缺点:

  模块名仍可能冲突. 有些模块名太长, 不太方便.

- 结论:

1. 使用 `import x` 来导入包和模块.
2. 使用 `from x import y` , 其中x是包前缀, y是不带前缀的模块名.
3. 使用 `from x import y as z`, 如果两个要导入的模块都叫做y或者y太长了.
4. 仅当缩写 `z` 是通用缩写时才可使用 `import y as z`.(比如 `np` 代表 `numpy`.)

例如, 模块 `sound.effects.echo` 可以用如下方式导入:

```
from sound.effects import echo
...
echo.EchoFilter(input, output, delay=0.7, atten=4)
```

导入时不要使用相对名称. 即使模块在同一个包中, 也要使用完整包名. 这能帮助你避免无意间导入一个包两次.

导入 `typing` 和 [six.moves](https://six.readthedocs.io/#module-six.moves) 模块时可以例外.

### 包

Tip

使用模块的全路径名来导入每个模块

- 优点:

  避免模块名冲突或是因非预期的模块搜索路径导致导入错误. 查找包更容易.

- 缺点:

  部署代码变难, 因为你必须复制包层次.

- 结论:

  所有的新代码都应该用完整包名来导入每个模块.应该像下面这样导入:

yes:

```
# 在代码中引用完整名称 absl.flags (详细情况).
import absl.flags
from doctor.who import jodie

FLAGS = absl.flags.FLAGS
# 在代码中仅引用模块名 flags (常见情况).
from absl import flags
from doctor.who import jodie

FLAGS = flags.FLAGS
```

No: (假设当前文件和 jodie.py 都在目录 doctor/who/ 下)

```
# 没能清晰指示出作者想要导入的模块和最终被导入的模块.
# 实际导入的模块将取决于 sys.path.
import jodie
```

不应假定主入口脚本所在的目录就在 sys.path 中，虽然这种情况是存在的。当主入口脚本所在目录不在 sys.path 中时，代码将假设 import jodie 是导入的一个第三方库或者是一个名为 jodie 的顶层包，而不是本地的 jodie.py

### 异常

Tip

允许使用异常, 但必须小心

- 定义:

  异常是一种跳出代码块的正常控制流来处理错误或者其它异常条件的方式.

- 优点:

  正常操作代码的控制流不会和错误处理代码混在一起. 当某种条件发生时, 它也允许控制流跳过多个框架. 例如, 一步跳出N个嵌套的函数, 而不必继续执行错误的代码.

- 缺点:

  可能会导致让人困惑的控制流. 调用库时容易错过错误情况.

- 结论:

- 异常必须遵守特定条件:

  1. 优先合理的使用内置异常类.比如 `ValueError` 指示了一个程序错误, 比如在方法需要正数的情况下传递了一个负数错误.不要使用 `assert` 语句来验证公共API的参数值. `assert` 是用来保证内部正确性的,而不是用来强制纠正参数使用.若需要使用异常来指示某些意外情况,不要用 `assert`,用 `raise` 语句,例如:

  Yes:

  ```
  def connect_to_next_port(self, minimum):
      """Connects to the next available port.
  
      Args:
          minimum: A port value greater or equal to 1024.
  
      Returns:
          The new minimum port.
  
      Raises:
          ConnectionError: If no available port is found.
      """
      if minimum < 1024:
          # Note that this raising of ValueError is not mentioned in the doc
          # string's "Raises:" section because it is not appropriate to
          # guarantee this specific behavioral reaction to API misuse.
          raise ValueError(f'Min. port must be at least 1024, not {minimum}.')
      port = self._find_next_open_port(minimum)
      if not port:
          raise ConnectionError(
              f'Could not connect to service on port {minimum} or higher.')
      assert port >= minimum, (
          f'Unexpected port {port} when minimum was {minimum}.')
      return port
  ```

  No:

  ```
  def connect_to_next_port(self, minimum):
      """Connects to the next available port.
  
      Args:
      minimum: A port value greater or equal to 1024.
  
      Returns:
      The new minimum port.
      """
      assert minimum >= 1024, 'Minimum port must be at least 1024.'
      port = self._find_next_open_port(minimum)
      assert port is not None
      return port
  ```

  2. 模块或包应该定义自己的特定域的异常基类, 这个基类应该从内建的Exception类继承. 模块的异常基类后缀应该叫做 `Error`.
3. 永远不要使用 `except:` 语句来捕获所有异常, 也不要捕获 `Exception` 或者 `StandardError` , 除非你打算重新触发该异常, 或者你已经在当前线程的最外层(记得还是要打印一条错误消息). 在异常这方面, Python非常宽容, `except:` 真的会捕获包括Python语法错误在内的任何错误. 使用 `except:` 很容易隐藏真正的bug.
  4. 尽量减少try/except块中的代码量. try块的体积越大, 期望之外的异常就越容易被触发. 这种情况下, try/except块将隐藏真正的错误.
5. 使用finally子句来执行那些无论try块中有没有异常都应该被执行的代码. 这对于清理资源常常很有用, 例如关闭文件.

### 全局变量

Tip

避免全局变量

- 定义:

  定义在模块级的变量.

- 优点:

  偶尔有用.

- 缺点:

  导入时可能改变模块行为, 因为导入模块时会对模块级变量赋值.

- 结论:

  避免使用全局变量. 鼓励使用模块级的常量,例如 `MAX_HOLY_HANDGRENADE_COUNT = 3`.注意常量命名必须全部大写,用 `_` 分隔.具体参见 [命名规则](https://google.github.io/styleguide/pyguide.html#s3.16-naming) 若必须要使用全局变量,应在模块内声明全局变量,并在名称前 `_` 使之成为模块内部变量.外部访问必须通过模块级的公共函数.具体参见 [`命名规则 <>`_](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules/#system-message-4)

### 嵌套/局部/内部类或函数

**Tip**

使用内部类或者嵌套函数可以用来覆盖某些局部变量.

- 定义:

  类可以定义在方法, 函数或者类中. 函数可以定义在方法或函数中. 封闭区间中定义的变量对嵌套函数是只读的. (译者注:即内嵌函数可以读外部函数中定义的变量,但是无法改写,除非使用 nonlocal)

- 优点:

  允许定义仅用于有效范围的工具类和函数.在装饰器中比较常用.

- 缺点:

  嵌套类或局部类的实例不能序列化(pickled). 内嵌的函数和类无法直接测试.同时内嵌函数和类会使外部函数的可读性变差.

- 结论:

  使用内部类或者内嵌函数可以忽视一些警告.但是应该避免使用内嵌函数或类,除非是想覆盖某些值.若想对模块的用户隐藏某个函数,不要采用嵌套它来隐藏,应该在需要被隐藏的方法的模块级名称加 `_` 前缀,这样它依然是可以被测试的.

### 推导式&生成式

Tip

可以在简单情况下使用

- 定义:

  列表,字典和集合的推导&生成式提供了一种简洁高效的方式来创建容器和迭代器, 而不必借助map(), filter(), 或者lambda.(译者注: 元组是没有推导式的, `()` 内加类似推导式的句式返回的是个生成器)

- 优点:

  简单的列表推导可以比其它的列表创建方法更加清晰简单. 生成器表达式可以十分高效, 因为它们避免了创建整个列表.

- 缺点:

  复杂的列表推导或者生成器表达式可能难以阅读.

- 结论:

  适用于简单情况. 每个部分应该单独置于一行: 映射表达式, for语句, 过滤器表达式. 禁止多重for语句或过滤器表达式. 复杂情况下还是使用循环.

  Yes:

  ```
  result = [mapping_expr for value in iterable if filter_expr]
  
  result = [{'key': value} for value in iterable
              if a_long_filter_expression(value)]
  
  result = [complicated_transform(x)
              for x in iterable if predicate(x)]
  
  descriptive_name = [
      transform({'key': key, 'value': value}, color='black')
      for key, value in generate_iterable(some_input)
      if complicated_condition_is_met(key, value)
  ]
  
  result = []
  for x in range(10):
      for y in range(5):
          if x * y > 10:
              result.append((x, y))
  
  return {x: complicated_transform(x)
          for x in long_generator_function(parameter)
          if x is not None}
  
  squares_generator = (x**2 for x in range(10))
  
  unique_names = {user.name for user in users if user is not None}
  
  eat(jelly_bean for jelly_bean in jelly_beans
      if jelly_bean.color == 'black')
  ```

  No:

  ```
  result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]
  
  return ((x, y, z)
          for x in xrange(5)
          for y in xrange(5)
          if x != y
          for z in xrange(5)
          if y != z)
  ```

### 默认迭代器和操作符

Tip

如果类型支持, 就使用默认迭代器和操作符. 比如列表, 字典及文件等.

- 定义:

  容器类型, 像字典和列表, 定义了默认的迭代器和关系测试操作符(in和not in)

- 优点:

  默认操作符和迭代器简单高效, 它们直接表达了操作, 没有额外的方法调用. 使用默认操作符的函数是通用的. 它可以用于支持该操作的任何类型.

- 缺点:

  你没法通过阅读方法名来区分对象的类型(例如, has_key()意味着字典). 不过这也是优点.

- 结论:

  如果类型支持, 就使用默认迭代器和操作符, 例如列表, 字典和文件. 内建类型也定义了迭代器方法. 优先考虑这些方法, 而不是那些返回列表的方法. 当然，这样遍历容器时，你将不能修改容器. 除非必要,否则不要使用诸如 dict.iter*() 这类python2的特定迭代方法.

  Yes:

  ```
  for key in adict: ...
  if key not in adict: ...
  if obj in alist: ...
  for line in afile: ...
  for k, v in dict.iteritems(): ...
  ```

  No:

  ```
  for key in adict.keys(): ...
  if not adict.has_key(key): ...
  for line in afile.readlines(): ...
  ```

## 生成器

Tip

按需使用生成器.

- 定义:

  所谓生成器函数, 就是每当它执行一次生成(yield)语句, 它就返回一个迭代器, 这个迭代器生成一个值. 生成值后, 生成器函数的运行状态将被挂起, 直到下一次生成.

- 优点:

  简化代码, 因为每次调用时, 局部变量和控制流的状态都会被保存. 比起一次创建一系列值的函数, 生成器使用的内存更少.

- 缺点:

  没有.

- 结论:

  鼓励使用. 注意在生成器函数的文档字符串中使用”Yields:”而不是”Returns:”.(译者注: 参看 [注释](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/#comments) )

### Lambda函数

Tip

适用于单行函数

- 定义:

  与语句相反, lambda在一个表达式中定义匿名函数. 常用于为 `map()` 和 `filter()` 之类的高阶函数定义回调函数或者操作符.

- 优点:

  方便.

- 缺点:

  比本地函数更难阅读和调试. 没有函数名意味着堆栈跟踪更难理解. 由于lambda函数通常只包含一个表达式, 因此其表达能力有限.

- 结论:

  适用于单行函数. 如果代码超过60-80个字符, 最好还是定义成常规(嵌套)函数.对于常见的操作符，例如乘法操作符，使用 `operator` 模块中的函数以代替lambda函数. 例如, 推荐使用 `operator.mul` , 而不是 `lambda x, y: x * y` .

## 条件表达式

Tip

适用于单行函数

- 定义:

  条件表达式(又名三元运算符)是对于if语句的一种更为简短的句法规则. 例如: `x = 1 if cond else 2` .

- 优点:

  比if语句更加简短和方便.

- 缺点:

  比if语句难于阅读. 如果表达式很长， 难于定位条件.

- 结论:

  适用于单行函数. 写法上推荐真实表达式,if表达式,else表达式每个独占一行.在其他情况下，推荐使用完整的if语句.

  ```
  one_line = 'yes' if predicate(value) else 'no'
  slightly_split = ('yes' if predicate(value)
                  else 'no, nein, nyet')
  the_longest_ternary_style_that_can_be_done = (
      'yes, true, affirmative, confirmed, correct'
      if predicate(value)
      else 'no, false, negative, nay')
  bad_line_breaking = ('yes' if predicate(value) else
                  'no')
  portion_too_long = ('yes'
                      if some_long_module.some_long_predicate_function(
                          really_long_variable_name)
                      else 'no, false, negative, nay')
  ```

### 默认参数值

Tip

适用于大部分情况.

- 定义:

  你可以在函数参数列表的最后指定变量的值, 例如, `def foo(a, b = 0):` . 如果调用foo时只带一个参数, 则b被设为0. 如果带两个参数, 则b的值等于第二个参数.

- 优点:

  你经常会碰到一些使用大量默认值的函数, 但偶尔(比较少见)你想要覆盖这些默认值. 默认参数值提供了一种简单的方法来完成这件事, 你不需要为这些罕见的例外定义大量函数. 同时, Python也不支持重载方法和函数, 默认参数是一种”仿造”重载行为的简单方式.

- 缺点:

  默认参数只在模块加载时求值一次. 如果参数是列表或字典之类的可变类型, 这可能会导致问题. 如果函数修改了对象(例如向列表追加项), 默认值就被修改了.

- 结论:

  鼓励使用, 不过有如下注意事项:不要在函数或方法定义中使用可变对象作为默认值.

  ```
  Yes: def foo(a, b=None):
          if b is None:
              b = []
  Yes: def foo(a, b: Optional[Sequence] = None):
          if b is None:
              b = []
  Yes: def foo(a, b: Sequence = ()):  # Empty tuple OK since tuples are immutable
  No:  def foo(a, b=[]):
      ...
  No:  def foo(a, b=time.time()):  # The time the module was loaded???
      ...
  No:  def foo(a, b=FLAGS.my_thing):  # sys.argv has not yet been parsed...
      ...
  No:  def foo(a, b: Mapping = {}):  # Could still get passed to unchecked code
      ...
  ```

### 特性(properties)

(译者注:参照fluent python.这里将 “property” 译为”特性”,而 “attribute” 译为属性. python中数据的属性和处理数据的方法统称属性”(arrtibute)”, 而在不改变类接口的前提下用来修改数据属性的存取方法我们称为”特性(property)”.)

Tip

访问和设置数据成员时, 你通常会使用简单, 轻量级的访问和设置函数.建议使用特性(properties)来代替它们.

- 定义:

  一种用于包装方法调用的方式. 当运算量不大, 它是获取和设置属性(attribute)的标准方式.

- 优点:

  通过消除简单的属性(attribute)访问时显式的get和set方法调用, 可读性提高了. 允许懒惰的计算. 用Pythonic的方式来维护类的接口. 就性能而言, 当直接访问变量是合理的, 添加访问方法就显得琐碎而无意义. 使用特性(properties)可以绕过这个问题. 将来也可以在不破坏接口的情况下将访问方法加上.

- 缺点:

  特性(properties)是在get和set方法声明后指定, 这需要使用者在接下来的代码中注意: set和get是用于特性(properties)的(除了用 `@property` 装饰器创建的只读属性). 必须继承自object类. 可能隐藏比如操作符重载之类的副作用. 继承时可能会让人困惑. (译者注:这里没有修改原始翻译,其实就是 @property 装饰器是不会被继承的)

- 结论:

  你通常习惯于使用访问或设置方法来访问或设置数据, 它们简单而轻量. 不过我们建议你在新的代码中使用属性. 只读属性应该用 `@property` [装饰器](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Function_and_Method_Decorators) 来创建.如果子类没有覆盖属性, 那么属性的继承可能看上去不明显. 因此使用者必须确保访问方法间接被调用, 以保证子类中的重载方法被属性调用(使用模板方法设计模式).

  ```
  Yes:
      import math
  
      class Square:
          """A square with two properties: a writable area and a read-only perimeter.
  
          To use:
          >>> sq = Square(3)
          >>> sq.area
          9
          >>> sq.perimeter
          12
          >>> sq.area = 16
          >>> sq.side
          4
          >>> sq.perimeter
          16
          """
  
          def __init__(self, side):
              self.side = side
  
          @property
          def area(self):
              """Area of the square."""
              return self._get_area()
  
          @area.setter
          def area(self, area):
              return self._set_area(area)
  
          def _get_area(self):
              """Indirect accessor to calculate the 'area' property."""
              return self.side ** 2
  
          def _set_area(self, area):
              """Indirect setter to set the 'area' property."""
              self.side = math.sqrt(area)
  
          @property
          def perimeter(self):
              return self.side * 4
  ```

### True/False的求值

Tip

尽可能使用隐式false

- 定义:

  Python在布尔上下文中会将某些值求值为false. 按简单的直觉来讲, 就是所有的”空”值都被认为是false. 因此0， None, [], {}, “” 都被认为是false.

- 优点:

  使用Python布尔值的条件语句更易读也更不易犯错. 大部分情况下, 也更快.

- 缺点:

  对C/C++开发人员来说, 可能看起来有点怪.

- 结论:

  尽可能使用隐式的false, 例如: 使用 `if foo:` 而不是 `if foo != []:` . 不过还是有一些注意事项需要你铭记在心:

1. 对于 `None` 等单例对象测试时,使用 `is` 或者 `is not`.当你要测试一个默认值是None的变量或参数是否被设为其它值. 这个值在布尔语义下可能是false!

   (译者注: `is` 比较的是对象的id(), 这个函数返回的通常是对象的内存地址,考虑到CPython的对象重用机制,可能会出现生命周不重叠的两个对象会有相同的id)

2. 永远不要用==将一个布尔量与false相比较. 使用 `if not x:` 代替. 如果你需要区分false和None, 你应该用像 `if not x and x is not None:` 这样的语句.

3. 对于序列(字符串, 列表, 元组), 要注意空序列是false. 因此 `if not seq:` 或者 `if seq:` 比 `if len(seq):` 或 `if not len(seq):` 要更好.

4. 处理整数时, 使用隐式false可能会得不偿失(即不小心将None当做0来处理). 你可以将一个已知是整型(且不是len()的返回结果)的值与0比较.

   > Yes:
   >
   > ```
   > if not users:
   >     print('no users')
   > 
   > if foo == 0:
   >     self.handle_zero()
   > 
   > if i % 10 == 0:
   >     self.handle_multiple_of_ten()
   > 
   > def f(x=None):
   >     if x is None:
   >         x = []
   > ```
   >
   > No:
   >
   > ```
   > if len(users) == 0:
   >     print 'no users'
   > 
   > if foo is not None and not foo:
   >     self.handle_zero()
   > 
   > if not i % 10:
   >     self.handle_multiple_of_ten()
   > 
   > def f(x=None):
   >     x = x or []
   > ```

5. 注意’0’(字符串)会被当做true.

### 过时的语言特性

Tip

尽可能使用字符串方法取代字符串模块. 使用函数调用语法取代apply(). 使用列表推导, for循环取代filter(), map()以及reduce().

- 定义:

  当前版本的Python提供了大家通常更喜欢的替代品.

- 结论:

  我们不使用不支持这些特性的Python版本, 所以没理由不用新的方式.

  ```
  Yes: words = foo.split(':')
  
       [x[1] for x in my_list if x[2] == 5]
  
       map(math.sqrt, data)    # Ok. No inlined lambda expression.
  
       fn(*args, **kwargs)
  No:  words = string.split(foo, ':')
  
       map(lambda x: x[1], filter(lambda x: x[2] == 5, my_list))
  
       apply(fn, args, kwargs)
  ```

### 词法作用域(Lexical Scoping)

推荐使用

- 定义:

  嵌套的Python函数可以引用外层函数中定义的变量, 但是不能够对它们赋值. 变量绑定的解析是使用词法作用域, 也就是基于静态的程序文本. 对一个块中的某个名称的任何赋值都会导致Python将对该名称的全部引用当做局部变量, 甚至是赋值前的处理. 如果碰到global声明, 该名称就会被视作全局变量.一个使用这个特性的例子:

  ```
  def get_adder(summand1):
      """Returns a function that adds numbers to a given number."""
      def adder(summand2):
          return summand1 + summand2
  
      return adder
  ```

  (译者注: 这个例子有点诡异, 你应该这样使用这个函数: `sum = get_adder(summand1)(summand2)` )

- 优点:

  通常可以带来更加清晰, 优雅的代码. 尤其会让有经验的Lisp和Scheme(还有Haskell, ML等)程序员感到欣慰.

- 缺点:

  可能导致让人迷惑的bug. 例如下面这个依据 [PEP-0227](http://www.python.org/dev/peps/pep-0227/) 的例子:

  ```
  i = 4
  def foo(x):
      def bar():
          print i,
      # ...
      # A bunch of code here
      # ...
      for i in x:  # Ah, i *is* local to Foo, so this is what Bar sees
          print i,
      bar()
  ```

​		因此 `foo([1, 2, 3])` 会打印 `1 2 3 3` , 不是 `1 2 3 4` .

​		(译者注: x是一个列表, for循环其实是将x中的值依次赋给i.这样对i的赋值就隐式的发生了, 整个foo函数体中的i都会被当做局部变量, 包括bar()中的那个. 这一点与C++之类的静态语言还是有很大差别的.)

### 函数与方法装饰器

Tip

如果好处很显然, 就明智而谨慎的使用装饰器,避免使用 `staticmethod`以及谨慎使用`classmethod`.

- 定义:

  [用于函数及方法的装饰器](https://docs.python.org/release/2.4.3/whatsnew/node6.html) (也就是@标记). 最常见的装饰器是@classmethod 和@staticmethod, 用于将常规函数转换成类方法或静态方法. 不过, 装饰器语法也允许用户自定义装饰器. 特别地, 对于某个函数 `my_decorator` , 下面的两段代码是等效的:

  ```
  class C(object):
     @my_decorator
     def method(self):
         # method body ...
         
  class C(object):
      def method(self):
          # method body ...
      method = my_decorator(method)
  ```

- 优点:

优雅的在函数上指定一些转换. 该转换可能减少一些重复代码, 保持已有函数不变(enforce invariants), 等.

- 缺点:

装饰器可以在函数的参数或返回值上执行任何操作, 这可能导致让人惊异的隐藏行为. 而且, 装饰器在导入时执行. 从装饰器代码中捕获错误并处理是很困难的.

- 结论:

如果好处很显然, 就明智而谨慎的使用装饰器. 装饰器应该遵守和函数一样的导入和命名规则. 装饰器的python文档应该清晰的说明该函数是一个装饰器. 请为装饰器编写单元测试.

避免装饰器自身对外界的依赖(即不要依赖于文件, socket, 数据库连接等), 因为装饰器运行时这些资源可能不可用(由 `pydoc` 或其它工具导入). 应该保证一个用有效参数调用的装饰器在所有情况下都是成功的.

装饰器是一种特殊形式的”顶级代码”. 参考后面关于 Main 的话题.

除非是为了将方法和现有的API集成，否则不要使用 `staticmethod` .多数情况下，将方法封装成模块级的函数可以达到同样的效果.

谨慎使用 `classmethod` .通常只在定义备选构造函数，或者写用于修改诸如进程级缓存等必要的全局状态的特定类方法才用。

### 线程



## 命名

**tip**

> 模块名写法: `module_name` ;
>
> 包名写法: `package_name` ;
>
> 类名: `ClassName` ;
>
> 方法名: `method_name` ;
>
> 异常名: `ExceptionName` ;
>
> 函数名: `function_name` ;
>
> 全局常量名: `GLOBAL_CONSTANT_NAME` ;
>
> 全局变量名: `global_var_name` ;
>
> 实例名: `instance_var_name` ;
>
> 函数参数名: `function_parameter_name` ;
>
> 局部变量名: `local_var_name` . 
>
> 函数名,变量名和文件名应该是描述性的,尽量避免缩写,特别要避免使用非项目人员不清楚难以理解的缩写,不要通过删除单词中的字母来进行缩写. 始终使用 `.py` 作为文件后缀名,不要用破折号.

**应该避免的名称**

> 1. 单字符名称, 除了计数器和迭代器,作为 `try/except` 中异常声明的 `e`,作为 `with` 语句中文件句柄的 `f`.
> 2. 包/模块名中的连字符(-)
> 3. 双下划线开头并结尾的名称(Python保留, 例如__init__)

**命名约定**

> 1. 所谓”内部(Internal)”表示仅模块内可用, 或者, 在类内是保护或私有的.
> 2. 用单下划线(_)开头表示模块变量或函数是protected的(使用from module import *时不会包含).
> 3. 用双下划线(__)开头的实例变量或方法表示类内私有.
> 4. 将相关的类和顶级函数放在同一个模块里. 不像Java, 没必要限制一个类一个模块.
> 5. 对类名使用大写字母开头的单词(如CapWords, 即Pascal风格), 但是模块名应该用小写加下划线的方式(如lower_with_under.py). 尽管已经有很多现存的模块使用类似于CapWords.py这样的命名, 但现在已经不鼓励这样做, 因为如果模块名碰巧和类名一致, 这会让人困扰.

**文件名**

> 所有python脚本文件都应该以 `.py` 为后缀名且不包含 `-`.若是需要一个无后缀名的可执行文件,可以使用软联接或者包含 `exec "$0.py" "$@"` 的bash脚本.

**Python之父Guido推荐的规范**

| Type                       | Public             | Internal                                                     |
| -------------------------- | ------------------ | ------------------------------------------------------------ |
| Modules                    | lower_with_under   | _lower_with_under                                            |
| Packages                   | lower_with_under   |                                                              |
| Classes                    | CapWords           | _CapWords                                                    |
| Exceptions                 | CapWords           |                                                              |
| Functions                  | lower_with_under() | _lower_with_under()                                          |
| Global/Class Constants     | CAPS_WITH_UNDER    | _CAPS_WITH_UNDER                                             |
| Global/Class Variables     | lower_with_under   | _lower_with_under                                            |
| Instance Variables         | lower_with_under   | _lower_with_under (protected) or __lower_with_under (private) |
| Method Names               | lower_with_under() | _lower_with_under() (protected) or __lower_with_under() (private) |
| Function/Method Parameters | lower_with_under   |                                                              |
| Local Variables            | lower_with_under   |                                                              |

# 其他

## 动词

| 类别                          | 单词                                           |
| ----------------------------- | ---------------------------------------------- |
| 添加/插入/创建/初始化/加载    | add、append、insert、create、initialize、load  |
| 删除/销毁                     | delete、remove、destroy、drop                  |
| 打开/开始/启动                | open、start                                    |
| 关闭/停止                     | close、stop                                    |
| 获取/读取/查找/查询           | get、fetch、acquire、read、search、find、query |
| 设置/重置/放入/写入/释放/刷新 | set、reset、put、write、release、refresh       |
| 发送/推送                     | send、push                                     |
| 接收/拉取                     | receive、pull                                  |
| 提交/撤销/取消                | submit、cancel                                 |
| 收集/采集/选取/选择           | collect、pick、select                          |
| 提取/解析                     | sub、extract、parse                            |
| 编码/解码                     | encode、decode                                 |
| 填充/打包/压缩                | fill、pack、compress                           |
| 清空/拆包/解压                | flush、clear、unpack、decompress               |
| 增加/减少                     | increase、decrease、reduce                     |
| 分隔/拼接                     | split、join、concat                            |
| 过滤/校验/检测                | filter、valid、check                           |

## 名词

| 类别                         | 单词                                                 |
| ---------------------------- | ---------------------------------------------------- |
| 容量/大小/长度               | capacity、size、length                               |
| 实例/上下文                  | instance、context                                    |
| 配置                         | config、settings                                     |
| 头部/前面/前一个/第一个      | header、front、previous、first                       |
| 尾部/后面/后一个/最后一个    | tail、back、next、last                               |
| 区间/区域/某一部分/范围/规模 | range、interval、region、area、section、scope、scale |
| 缓存/缓冲/会话               | cache、buffer、session                               |
| 本地/局部/全局               | local、global                                        |
| 成员/元素                    | member、element                                      |
| 菜单/列表                    | menu、list                                           |
| 源/目标                      | source、destination、target                          |