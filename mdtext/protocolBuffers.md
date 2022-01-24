## enum 枚举

## 解析和序列化

`SerializeToString()`序列化信息并将其作为字符串返回

`ParseFromString(data)`从给定的字符串解析信息

## 编译

`protoc -I=path --python_out = path file_name`

-I proto文件路径

--python_out 输出文件路径

file_name proto文件名

## import

导入其他proto文件

`import "path/xxx.proto"`

注意，只能在当前文件夹中寻找import的proto文件，如果需要引用的文件在其他文件夹，需要在编译是执行 -I = path 添加引用proto文件的路径。（-I = path 命令就是添加proto文件目录的指令，可以有多条）

## package

声明符，用来防止不同的信息类型有命名冲突。包的声明符会根据使用语言的不同影响生成的代码

## 经验

### 编写一个protocol buffers应用

1. 定义消息格式文件(.proto文件)
2. 编译.proto文件，生成代码文件
3. 使用protocol buffers库提供的API编写应用程序

## google.protobuf

https://googleapis.dev/python/protobuf/latest/google/protobuf.html

### json_format

https://googleapis.dev/python/protobuf/latest/google/protobuf/json_format.html#google.protobuf.json_format.MessageToJson

#### `MessageToDict`

```
google.protobuf.json_format.MessageToDict(message, including_default_value_fields=False, preserving_proto_field_name=False, use_integers_for_enums=False, descriptor_pool=None, float_precision=None)
```

把message转成字典格式，字典编译成json时，符合proto3 json规范

---

#### `MessageToJson`

protobuf消息转换成json格式

**返回值**：json格式的protobuf message的字符串

```
google.protobuf.json_format.MessageToJson(message, including_default_value_fields=False, preserving_proto_field_name=False, indent=2, sort_keys=False, use_integers_for_enums=False, descriptor_pool=None, float_precision=None)
```

###### 参数列表

message

including_default_value_fields=False	如果为TRUE，则单个原始字段、重复字段和映射字段将始终被序列化。如果为false，则仅序列化非空字段。单个消息字段和oneof字段不受此选项影响

preserving_proto_field_name=False	如果为TRUE，则使用.proto文件中定义的原始proto字段名称。如果为False，则字段名称转换为小驼峰命名

indent=2	缩进级别，打印json对象时用到。缩进级别0或者负数只会插入换行符

sort_keys=False	如果为True，则输出按字段名称排序

use_integers_for_enums=False	如果为真，则打印整数而不是枚举名称

descriptor_pool=None	用于解析Any类型的描述符池。如果None使用默认值

float_precision=None	如果设置，使用它来指定浮点字段有效数字

---

#### `Parse`

```
google.protobuf.json_format.Parse(text, message, ignore_unknown_fields=False, descriptor_pool=None)
```

将一个json形式的protocol message解析成message

---

#### `ParseDict`

```
google.protobuf.json_format.ParseDict(js_dict, message, ignore_unknown_fields=False, descriptor_pool=None)
```

将一个Json字典解析成message

### **text_format**

#### MessageToString

将protobuf消息转换为文本格式

返回值：string  文本格式的protocol buffer message的字符串

```
google.protobuf.text_format.MessageToString( message , as_utf8=False , as_one_line=False , use_short_repeated_primitives=False , pointy_brackets=False , use_index_order=False , float_format=None , double_format =None , use_field_number=False , descriptor_pool=None , indent=0 , message_formatter=None , print_unknown_fields=False , force_colon=False )
```

##### 参数列表

message

as_utf8=False 为非ASCII字符返回未转义的Unicode。在Python3中，实际的Unicode字符可能会以字符串形式出现

as_one_line=False 不要在字段之间引入换行符

use_short_repeated_primitives=False 对原语使用短重复格式

pointy_brackets=False 如果为True，使用尖括号而不是花括号进行嵌套

use_index_order=False	如果为TRUE，将使用源代码中定义的顺序而不是字段编号来打印proto消息的字段，扩展将在消息末尾打印，他们的相对顺序由扩展编号决定。默认下使用字段编号顺序

float_format=None	如果设置，使用它来指定浮点字段格式（根据“Format Specification Mini-Language"） 

double_format =None	同float，注意如果设置了float_format未设置double，会使用float的设置。默认使用str（）

use_field_number=False	如果为TRUE，则打印字段编号而不是名称

descriptor_pool=None	用于解析Any类型的描述符池

indent=0			初始缩进级别，用空格表示，用于漂亮的打印

message_formatter=None	选定子消息的自定义格式化程序（通常基于消息类型）。用于漂亮（特殊）的打印部分protobuf以便于区分

print_unknown_fields=False	如果为TRUE，打印未知字段 

force_colon=False			如果设置，即使字段是原始消息，也会在字段名称后添加冒号

#### Parse

将协议消息的文本解析为message

**返回值**  message

```
google.protobuf.text_format.Parse(text, message, allow_unknown_extension=False, allow_field_number=False, descriptor_pool=None, allow_unknown_field=False)
```

##### 参数列表

text(str)

message

allow_unknown_extension=False	如果为真，跳过缺少的扩展并继续解析

allow_field_number=False			如果为True，则允许字段编号和字段名称

descriptor_pool=None				用于解析Any类型的描述符池

allow_unknown_field=False	如果为真，跳过未知字段并继续解析。如果可能，请避免使用此选项，它可能会隐藏一些错误（例如字段名称的拼写）

