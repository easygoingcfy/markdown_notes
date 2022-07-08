

# 基础&理论





## 字典dict

哈希表

### 字典的构造

格式：` d = {key1 : value1, key2:value2.....}`

``` 
items = [('name','Gumby'),('age',42)]
d = dict(items)
d = dict(name='Gumby',age=42,height=1.76)
```

### 合并字典

```
dict2.update(dict1)
```



### 遍历

#### 遍历key

```
for key in dict:
for key in dict.keys():
```

#### 遍历value

```
for value in d.values():
```

#### 遍历项

```
for key,values in d.items():
```

### 删除元素

```
del tinydict['Name']  # 删除键是'Name'的条目
tinydict.clear()      # 清空字典所有条目
del tinydict          # 删除字典
```

### setdefault

```
d.setdefault(key, value)
```

如果key存在，会返回key对应的value，如果不存在，会设置key值为value。

## 字符串

### strip()

Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。

当rm为空时，默认删除空白符（包括'\n', '\r',  '\t',  ' ')

```
strip(rm)
lstrip(rm)
rstrip(rm)
```

## json

```
json.dumps()  将python对象编码成Json字符串
json.loads()  将Json字符串解码成python对象
json.dump()   将python中的对象转化成json储存到文件中
json.load()   将文件中的json的格式转化成python对象提取
```

注意，此处python对象不包括自定义的数据结构（类，消息）

使用json处理Protobuf消息时，仍然需要使用PythonApi ( json_format.Parse()  json_format.MessageToJson() ) 来完成消息与json字符串的转换。

```
json_format.MessageToJson(message, parameters)
json_format.Parse(text,message, parameters)
```



## 函数

```
def func(paras):
	balabala
	return xx	#如果有
```

### eval()

执行一个字符串表达式，并返回表达式的值

### exec()

exec 执行储存在字符串或文件中的Python语句，相比于 eval，exec可以执行更复杂的 Python 代码

### \_\_name\_\_:预定义全局变量

模块内部用来标识模块名称。如果模块被导入，则\_\_name\_\_的值为模块名称，如果主动执行，则为字符串“\_\_main\_\_”

因此就可以理解

if \_\_name\_\_ == '\_\_mian\_\_' : 

​		func()

### repr()

返回一个对象的string格式

### replace()

把字符串中的old替换成new，返回替换后的新字符串，如果指定max，则替换不超过max次

`str.replace(old, new[, max])`

### decode（）

以encoding指定的编码格式解码字符串。默认编码为字符串编码。

**返回值** 返回解码后的字符串

`str.decode(encoding='UTF-8',errors='strict')`

##### 参数

- encoding -- 要使用的编码，如"UTF-8"。
- errors -- 设置不同错误的处理方案。默认为 'strict',意为编码错误引起一个UnicodeError。 其他可能得值有 'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace' 以及通过 codecs.register_error() 注册的任何值。



## 列表

### 列表生成式

```
[exp for iter_var in iterable]
```

### 删除元素

#### del 

```
del listname[index]
del listname[start : end]
```

#### pop

如果不写 index 参数，默认会删除列表中的最后一个元素

```
listname.pop(index)
```

#### remove

除了 del 关键字，Python 还提供了 remove() 方法，该方法会根据元素本身的值来进行删除操作。

需要注意的是，remove() 方法只会删除第一个和指定值相同的元素，而且必须保证该元素是存在的，否则会引发 ValueError 错误。

```
list.remove(value)
```

#### clear()

Python clear() 用来删除列表的所有元素，也即清空列表

## ZIP

**zip()** 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。

如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用 * 号操作符，可以将元组解压为列表。

```
zip([iterable, ...])
```

## 注解 typing

用 : 类型 的形式指定函数的参数类型，用 -> 类型 的形式指定函数的返回值类型。

### 类型别名

适用于简化复杂的类型签名

```
Vector = list[floar]
```

### NewType

使用 [`NewType`](https://docs.python.org/zh-cn/3/library/typing.html#typing.NewType) 助手来创建不同的类型

```
from typing import NewType

UserId = NewType('UserId', int)
some_id = UserId(524313)
```

### 可调对象（Callable）

预期特定签名回调函数的框架可以用 `Callable[[Arg1Type, Arg2Type], ReturnType]` 实现类型提示。

```
from collections.abc import Callable

def feeder(get_next_item: Callable[[], str]) -> None:
    # Body

def async_query(on_success: Callable[[int], None],
                on_error: Callable[[int, Exception], None]) -> None:
    # Body

async def on_update(value: str) -> None:
    # Body
callback: Callable[[str], Awaitable[None]] = on_update
```



## [`inspect`](https://docs.python.org/3/library/inspect.html#module-inspect) — Inspect live objects



## yield

简单地讲，yield 的作用就是把一个函数变成一个 generator，带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator，调用 fab(5) 不会执行 fab 函数，而是返回一个 iterable 对象！在 for 循环执行时，每次循环都会执行 fab 函数内部的代码，执行到 yield b 时，fab 函数就返回一个迭代值，下次迭代时，代码从 yield b 的下一条语句继续执行，而函数的本地变量看起来和上次中断执行前是完全一样的，于是函数继续执行，直到再次遇到 yield。

一个带有 yield 的函数就是一个 generator，它和普通函数不同，生成一个 generator 看起来像函数调用，但不会执行任何函数代码，直到对其调用 next()（在 for 循环中会自动调用 next()）才开始执行。虽然执行流程仍按函数的流程执行，但每执行到一个 yield 语句就会中断，并返回一个迭代值，下次执行时从 yield 的下一个语句继续执行。看起来就好像一个函数在正常执行的过程中被 yield 中断了数次，每次中断都会通过 yield 返回当前的迭代值。

yield 的好处是显而易见的，把一个函数改写为一个 generator 就获得了迭代能力，比起用类的实例保存状态来计算下一个 next() 的值，不仅代码简洁，而且执行流程异常清晰。

## lru_cache

```
import functools

@functools.lru_cache()
def xxx():
```

## 时间

timestamp 转np.datetime64

```
t.to_datetime64()
```



# 面向对象

## super

**super()** 函数是用于调用父类(超类)的一个方法。

**super()** 是用来解决多重继承问题的，直接用类名调用父类方法在使用单继承的时候没问题，但是如果使用多继承，会涉及到查找顺序（MRO）、重复调用（钻石继承）等种种问题。

MRO 就是类的方法解析顺序表, 其实也就是继承父类方法时的顺序表。

```
super(B, self).add(x)
super().add()
super(LocalizationMsg, self).__init__()
```

## lru_cache

```
from functools import lru_cache
```

def lru_cache(maxsize=128, typed=False):

maxsize:被装饰的方法最大可缓存结果数量,为None时表示可以缓存无限个结果

typed:如果 *typed* 设置为true，不同类型的函数参数将被分别缓存

清理缓存：

cache_info 具名元组，包含命中次数 hits，未命中次数 misses ，最大缓存数量 maxsize 和 当前缓存大小 currsize

```
func为被修饰的函数
cache_info = func.cache_info()
if cache_info[3] > 0:
    func.cache_clear()
```



## 执行系统命令

os.system()

# 库

## import reportlib 生成pdf 

https://zhuanlan.zhihu.com/p/318390273

### PLATYPUS

Platypus是“Page Layout and Typography Using Scripts”，是使用脚本的页面布局和印刷术的缩写，这是一个高层次页面布局库，它可以让你通过编程创造复杂的文档，并且毫不费力。

Platypus设计的目的是**尽可能地将高层布局设计与文档内容分离**，比如，段落使用段落格式构造，页面使用页面模板，这样做是有好处的，在仅仅修改几行代码的情况下，包含数百个页面的数百个文档就能够被构造成不同的风格。

Platypus从上到下，可以被看成具备多个层次。

DocTemplates：文档最外层的容器

PageTemplates：各种页面布局的规格

Frames：包含流动的文本和图形的文档区域规范

Flowables：能够被“流入文档”的文本、图形和段落等。

![img](https://pic2.zhimg.com/80/v2-825211073a9973053d0ae81be7daf291_720w.jpg)

### 元素间距&换页

```
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

story.append(Spacer(1, 0.2*inch))

from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
story.append(PageBreak())
```



### 段落

段落是一种重要的Flowables，它可以格式化任意的文本。

**段落中主要包括两种信息：文本和格式。**

下面的语句可以用来创建一个段落的实例。

```
Paragraph(text, style)
```

text参数提供了段落的文本，末尾和换行处的空白都会被删除。

style参数用于设置段落的格式，这里段落的格式是指参数的集合，包括字体大小、行间距、首行缩进等参数。我们可以调用如下语句来获得默认段落格式。

```
from reportlab.lib.styles import ParagraphStyle
```

```
class ParagraphStyle(PropertySet):
    defaults = {
        'fontName':_baseFontName,
        'fontSize':10,
        'leading':12,
        'leftIndent':0,
        'rightIndent':0,
        'firstLineIndent':0,
        'alignment':TA_LEFT,
        'spaceBefore':0,
        'spaceAfter':0,
        'bulletFontName':_baseFontName,
        'bulletFontSize':10,
        'bulletIndent':0,
        #'bulletColor':black,
        'textColor': black,
        'backColor':None,
        'wordWrap':None,        #None means do nothing special
                                #CJK use Chinese Line breaking
                                #LTR RTL use left to right / right to left
                                #with support from pyfribi2 if available
        'borderWidth': 0,
        'borderPadding': 0,
        'borderColor': None,
        'borderRadius': None,
        'allowWidows': 1,
        'allowOrphans': 0,
        'textTransform':None,   #uppercase lowercase (captitalize not yet) or None or absent
        'endDots':None,         #dots on the last line of left/right justified paras
                                #string or object with text and optional fontName, fontSize, textColor & backColor
                                #dy
        'splitLongWords':1,     #make best efforts to split long words
        'underlineWidth': _baseUnderlineWidth,  #underline width
        'bulletAnchor': 'start',    #where the bullet is anchored ie start, middle, end or numeric
        'justifyLastLine': 0,   #n allow justification on the last line for more than n words 0 means don't bother
        'justifyBreaks': 0,     #justify lines broken with <br/>
        'spaceShrinkage': _spaceShrinkage,  #allow shrinkage of percentage of space to fit on line
        'strikeWidth': _baseStrikeWidth,    #stroke width
        'underlineOffset': _baseUnderlineOffset,    #fraction of fontsize to offset underlines
        'underlineGap': _baseUnderlineGap,      #gap for double/triple underline
        'strikeOffset': _baseStrikeOffset,  #fraction of fontsize to offset strikethrough
        'strikeGap': _baseStrikeGap,        #gap for double/triple strike
        'linkUnderline': _platypus_link_underline,
        #'underlineColor':  None,
        #'strikeColor': None,
        'hyphenationLang': _hyphenationLang,
        #'hyphenationMinWordLength': _hyphenationMinWordLength,
        'embeddedHyphenation': _embeddedHyphenation,
        'uriWasteReduce': _uriWasteReduce,
        }
```

参数说明：

- fontName：字体名称
- fontSize：字体大小
- leading：行间距
- leftIndent：左缩进
- rightIndent：右缩进
- firstLineIndent：首行缩进
- alignment：对齐方式
- spaceBefore：段前间隙
- spaceAfter：段后间隙
- bulletFontName：列表名称
- bulletFontSize：列表字体大小
- bulletIndent：列表缩进
- textColor：字体颜色
- backColor：背景色
- borderWidth：边框粗细
- borderPadding：边框间距
- borderColor：边框颜色

获得简单的预定义格式：

```
from reportlab.lib.styles import getSampleStyleSheet
stylesheet=getSampleStyleSheet()
normalStyle = stylesheet['Normal']
```

可用格式：

- Normal
- BodyText
- Italic
- Heading1
- Title
- Heading2
- Heading3
- Heading4
- Heading5
- Heading6
- Bullet
- Definition
- Code
- UnorderedList
- OrderedList

### 表格

表格是Flowable的派生类，是一种简单文本表格机制。表格可以保存所有能被转换为字符串或Flowerable是所有事物。

如果我们不提供行高，它们可以根据数据自动计算出行高。

如果需要，它们可以跨页分割，你可以指定跨页分割后，需要重复的行数。

表格风格和表格数据是分离的，因此你可以声明一系列的风格，然后将它们用于一大堆报告。

表格使用如下代码进行创建：

```
Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1,
repeatRows=0, repeatCols=0, rowSplitRange=None, spaceBefore=None,
spaceAfter=None)
```

#### 参数：

- data：数据参数是一系列的表格值，每个表格值能够被转换为字符串或者Flowable实例。data值的第一行是data[0]，第i行j列表格值是data[i] [j]。
- colWidths：是一系列值，这些值代表每列的宽度。如果传递的是None，则对应列宽需要被自动计算。
- rowHeights：是一系列值，这些值代表每行的高度。如果传递的是None，则对应的行高需要被自动计算。
- style：表格被创建时的初始样式值。
- splitByRow：布尔值，当指定值为1时，允许跨页分割表格，当指定指为0时，不允许跨页分割表格。
- repeatRows：指定跨页分行时，需要重复的行数。
- repeatCols：暂时没用。
- spaceBefore：指定表格前的行数。
- spaceAfter：指定表格后的行数。

ex：

```
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet

# 调用模板，创建指定名称的PDF文档
doc = SimpleDocTemplate("Hello.pdf")
# 获得模板表格
styles = getSampleStyleSheet()
# 指定模板
style = styles['Normal']
# 初始化内容
story =[]

# 初始化表格内容
data= [['00', '01', '02', '03', '04'],
       ['10', '11', '12', '13', '14'],
       ['20', '21', '22', '23', '24'],
       ['30', '31', '32', '33', '34']]

# 根据内容创建表格
t = Table(data)
# 将表格添加到内容中
story.append(t)
# 将内容输出到PDF中
doc.build(story)
```

#### 表格格式：

指定表格格式有两种方式，一种是在调用创建表格接口时，传入style参数，一种是在创建完表格后，调用如下接口：

```
Table.setStyle(tblStyle)
```

##### **直接传入style参数**

```
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("Hello.pdf")
styles = getSampleStyleSheet()
style = styles['Normal']
story =[]

data= [['00', '01', '02', '03', '04'],
['10', '11', '12', '13', '14'],
['20', '21', '22', '23', '24'],
['30', '31', '32', '33', '34']]

t=Table(data,style=[
('GRID',(0,0),(-1,-1),1,colors.grey),
('GRID',(1,1),(-2,-2),1,colors.green),
('BOX',(0,0),(1,-1),2,colors.red),
('BACKGROUND', (0, 0), (0, 1), colors.pink),
('BACKGROUND', (1, 1), (1, 2), colors.lavender),
('BACKGROUND', (2, 2), (2, 3), colors.orange),
])

story.append(t)
doc.build(story)
```

##### **调用setStyle**	

```
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("Hello.pdf")
styles = getSampleStyleSheet()
style = styles['Normal']
story =[]

data= [['00', '01', '02', '03', '04'],
['10', '11', '12', '13', '14'],
['20', '21', '22', '23', '24'],
['30', '31', '32', '33', '34']]

t=Table(data)

t.setStyle(TableStyle(
    [('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
     ('BOX', (0,0), (-1,-1), 2, colors.black),
     ('LINEBELOW', (0,0), (-1,0), 2, colors.yellow),
     ('LINEAFTER', (0,0), (0,-1), 2, colors.blue),
     ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
    ))

story.append(t)
doc.build(story)

```

#### 格式化命令

- FONTNAME：字体名称
- FONTSIZE：字体大小
- LEADING：行间距
- TEXTCOLOR：字体颜色
- ALIGNMENT：水平对齐方式（可选值："LEFT"，”RIGHT“，”CENTER“）
- LEFTPADDING：左边填充
- RIGHTPADDING：右边填充
- BOTTOMPADDING：底部填充
- TOPPADDING：顶部填充
- BACKGROUND：背景色
- VALIGN：垂直对齐方式（可选值："TOP"，“MIDDLE”，“BOTTOM”）
- GRID：表格颜色，被指定的行列中的所有子行和子列都被设置成相应颜色
- INNERGRID：表格颜色，仅仅修改指定的子行和子列的相应颜色（不包括边框）
- BOX：边框颜色，被指定的边框的颜色
- LINEBELOW：指定块底部的行颜色
- LINEAFTER：指定块右边的行颜色。

### 图片

图片的调用接口比较简单，在调用该接口时，支持默认的jpeg格式。接口如下：

```
Image(filename, width=None, height=None)
```

#### 参数

- filename：指定文件名
- width：指定图片的宽度
- height：指定图片的高度

ex：

```
from reportlab.platypus import SimpleDocTemplate, Image

from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("Hello.pdf")
styles = getSampleStyleSheet()
style = styles['Normal']
story =[]

t = Image("C:\\Users\\Administrator\\Desktop\\timg.jpg")
story.append(t)

doc.build(story)
```

## import docx生成word

conda :

```
conda install -c conda-forge python-docx
```

pip

```
pip install python-docx
```

### 常用函数

```
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
```

#### 添加标题

```
doc.add_heading(title, level)
设置居中：
paragraph = doc.add_heading(title, level)
paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

#### 添加段落

```
paragraph = doc.add_paragraph(text, style)
设置字体：
run = paragraph.add_run()
run.font.size = Pt(9)
```

#### 添加表格

```
table = doc.add_table(rows, cols)
设置
table.style = "Table Grid"
table.alignment= WD_TABLE_ALIGNMENT.CENTER
访问单元格：
table.cell(x,y).text = ""
table.rows[0].cells
table.columns[0].cells
```



#### 保存doc

```
doc.save(filepath)
```



## import tqdm

tqdm模块是python进度条库, 主要分为两种运行模式

1. 基于迭代对象运行: tqdm(iterator)

2. 手动进行更新

```
class tqdm(object):
  """
  Decorate an iterable object, returning an iterator which acts exactly
  like the original iterable, but prints a dynamically updating
  progressbar every time a value is requested.
  """

  def __init__(self, iterable=None, desc=None, total=None, leave=False,
               file=sys.stderr, ncols=None, mininterval=0.1,
               maxinterval=10.0, miniters=None, ascii=None,
               disable=False, unit='it', unit_scale=False,
               dynamic_ncols=False, smoothing=0.3, nested=False,
               bar_format=None, initial=0, gui=False):
```

- iterable: 可迭代的对象, 在手动更新时不需要进行设置
- desc: 字符串, 左边进度条描述文字
- total: 总的项目数
- leave: bool值, 迭代完成后是否保留进度条
- file: 输出指向位置, 默认是终端, 一般不需要设置
- ncols: 调整进度条宽度, 默认是根据环境自动调节长度, 如果设置为0, 就没有进度条, 只有输出的信息
- unit: 描述处理项目的文字, 默认是'it', 例如: 100 it/s, 处理照片的话设置为'img' ,则为 100 img/s
- unit_scale: 自动根据国际标准进行项目处理速度单位的换算, 例如 100000 it/s >> 100k it/s

## import logging

### 基础设置

```
logging.basicConfig()
参数：
filename
filemode 使用filemode='w',每次执行将会覆盖之前的log
encoding
level
```

### 设置显示日期和时间

```
import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is when this event was logged.')
```

## 进阶

Logger类

```python
logger = logging.getLogger(__name__)
```



## import pyplot

### 基础

#### 绘图函数

plot 折线图

```
参数：颜色与线形（同matlab）
plt.plot(x_data,y_data,'ro')
```

scatter 散点图

```
matplotlib.pyplot.scatter(x, y, s=None, c=None, marker=None, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, *, edgecolors=None, plotnonfinite=False, data=None, **kwargs)
```

参数说明

x，y：长度相同的数组，也就是我们即将绘制散点图的数据点，输入数据。

s：点的大小，默认 20，也可以是个数组，数组每个参数为对应点的大小。

c：点的颜色，默认蓝色 'b'，也可以是个 RGB 或 RGBA 二维行数组。

marker：点的样式，默认小圆圈 'o'。

cmap：Colormap，默认 None，标量或者是一个 colormap 的名字，只有 c 是一个浮点数数组的时才使用。如果没有申明就是 image.cmap。

norm：Normalize，默认 None，数据亮度在 0-1 之间，只有 c 是一个浮点数的数组的时才使用。

vmin，vmax：：亮度设置，在 norm 参数存在时会忽略。

alpha：：透明度设置，0-1 之间，默认 None，即不透明。

linewidths：：标记点的长度。

edgecolors：：颜色或颜色序列，默认为 'face'，可选值有 'face', 'none', None。

plotnonfinite：：布尔值，设置是否使用非限定的 c ( inf, -inf 或 nan) 绘制点。

**kwargs：：其他参数。

data:  **可索引对象，可选** 如果给定，以下参数也接受一个字符串`s`，它被解释为`data[s]`（除非这引发异常）：

*x* , *y* , *s* ,*线宽*, *edgecolors* , *c* , *facecolor* , *facecolors* , *color*

### 绘制时间数据

需要使用np库，将时间首先转换为datetime,然后使用np.datetime64()转换为datetime64类型即可。

坐标轴范围使用plt.xticks()设置，可使用pd.date_range设置时间范围：

```
plt.xticks(pd.date_range(f"{self.date} 8:00", f"{self.date} 23:00", freq="1h"))
```

### 让图像分布均匀

使用自定义比例

*class* **matplotlib.scale.****FuncScale****(***axis***,** *functions***)**



## import ipdb 

设置断点：

```
ipdb.set_trace()
```

启动命令式：

```
python -m ipdb code.py
```



```
ENTER(重复上次命令)
c(继续)
l(查找当前位于哪里)
s(进入子程序)
r(运行直到子程序结束)
!<python 命令>
h(帮助)
a(rgs) 打印当前函数的参数
j(ump) 让程序跳转到指定的行数
l(ist) 可以列出当前将要运行的代码块
n(ext) 让程序运行下一行，如果当前语句有一个函数调用，用 n 是不会进入被调用的函数体中的
p(rint) 最有用的命令之一，打印某个变量
q(uit) 退出调试
r(eturn) 继续执行，直到函数体返回
s(tep) 跟 n 相似，但是如果当前有一个函数调用，那么 s 会进入被调用的函数体中
```



## threading 线程锁

lock = threading.Lock()

```
lock.acquie(True)
lock.release()
```



## import json

```
json.dumps()    将 Python 对象编码成 JSON 字符串
json.dumps().encode("utf-8")    将 Python 对象编码成 JSON 字符串,以utf-8格式编码。
json.loads()    将已编码的 JSON 字符串解码为 Python 对象
```



## import argparse

https://docs.python.org/zh-cn/3/library/argparse.html#the-add-argument-method

https://docs.python.org/zh-cn/3/howto/argparse.html

对命令行参数进行操作

```
parser = argparse.ArgumentParser()

parser.add_argument(
	'-i','--in',action='store',type=str,required=True,
	help="help instruction")
	
args = parser.parse_args()
```



## import struck

用来处理C结构数据，使用`struck.pack`将数据转化成C结构数据，使用`struck.unpack`将C结构数据解析成元组

## import zlib

用来对字符串进行压缩

```
zlib.compress(string)
zlib.decompress(string)
```

## import sys

命令行参数存在 sys.argv[]

## import time

### time.mktime()

```
time.mktime(t)
t -- 结构化的时间或者完整的9位元组元素。
返回用秒数来表示时间的浮点数
```

### time.time()

返回当前时间的时间戳

### time.strptime()

根据指定的格式把一个时间字符串解析为时间元组

```
time.strptime(string[, format])
```

- string -- 时间字符串。
- format -- 格式化字符串。

返回struct_time对象。

### time.strftime()

格式化时间，返回以可读字符串表示的当地时间，格式由参数 format 决定

```
time.strftime(format[, t])
```

- format -- 格式字符串。
- t -- 可选的参数 t 是一个 struct_time 对象。

返回以可读字符串表示的当地时间

### time.gmtime()

gmtime() 函数将一个时间戳转换为UTC时区（0时区）的struct_time，可选的参数sec表示从1970-1-1以来的秒数。其默认值为time.time()，函数返回time.struct_time类型的对象。

## import numpy

### 随机数

#### rand

numpy.random.rand(d0, d1, …, dn)，产生[0,1)之间均匀分布的随机浮点数，其中d0，d1....表示传入的数组形状。

```
生成含有2个元素的一维数组
np.random.rand(2)
生成2*4的二维数组
np.random.rand(2,4)
```

#### randn

numpy.random.randn(d0, d1, …, dn)从标准正态分布中返回一个或多个样本值。 参数表示样本的形状。所谓标准正态分布就是指这个函数产生的随机数，服从均值为0，方差为1的分布，使用方法和rand()类似。

#### random

numpy.random.random()方法返回随机生成的一个实数（浮点数），它在[0,1)范围内。

```
生成一个2*4的随机数组
numpy.random.random((2,4))
```

这边需要注意的是这个函数的参数，只有一个参数“size”，有三种取值，None，int型整数，或者int型元组。

#### randint

用于生成指定范围内的整数。

```
np.random.randint(0,50,50)
```

具体函数：randint(low, high=None, size=None, dtype='l')

其中low是整型元素，表示范围的下限，可以取到。high表示范围的上限，不能取到。也就是左闭右开区间。

high没有填写时，默认生成随机数的范围是[0，low)

size可以是int整数，或者int型的元组，表示产生随机数的个数，或者随机数组的形状。

dtype表示具体随机数的类型，默认是int，可以指定成int64。

#### uniform

从指定范围内产生均匀分布的随机浮点数

```
#默认产生一个[0,1)之间随机浮点数
temp=np.random.uniform()
```

函数：uniform(low=0.0, high=1.0, size=None)

low表示范围的下限，float型，或float型数组，默认为0.0.

high表示范围的上限，float型，或float型数组，默认为1.0.

size表示“形状”或“个数”，int型，或int型元组，默认为None。

* 如果范围只有一个参数num，

如果num小于1，那么随机数的范围是[0,num)

如果num大于1，那么随机数的范围是[1,num)

如果num等于1，那么产生的随机数全是1。

#### seed

np.random.seed()

## import pandas

Pandas 的主要数据结构是 Series （一维数据）与 DataFrame（二维数据），这两种数据结构足以处理金融、统计、社会科学、工程等领域里的大多数典型用例。

### Series

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html

Pandas Series 类似表格中的一个列（column），类似于一维数组，可以保存任何数据类型。

Series 由索引（index）和列组成，函数如下：

```
pandas.Series( data, index, dtype, name, copy)
```

- **data**：一组数据(ndarray 类型)。
- **index**：数据索引标签，如果不指定，默认从 0 开始。
- **dtype**：数据类型，默认会自己判断。
- **name**：设置名称。
- **copy**：拷贝数据，默认为 False。

#### 判断元素是否为空

```
pandas.isna()
pandas.notna()
```

### DataFrame

DataFrame 是一个表格型的数据结构，它含有一组有序的列，每列可以是不同的值类型（数值、字符串、布尔型值）。DataFrame 既有行索引也有列索引，它可以被看做由 Series 组成的字典（共同用一个索引）。

DataFrame 构造方法如下：

```
pandas.DataFrame( data, index, columns, dtype, copy)
```

参数说明：

- **data**：一组数据(ndarray、series, map, lists, dict 等类型)。
- **index**：索引值，或者可以称为行标签。
- **columns**：列标签，默认为 RangeIndex (0, 1, 2, …, n) 。
- **dtype**：数据类型。
- **copy**：拷贝数据，默认为 False。

Pandas DataFrame 是一个二维的数组结构，类似二维数组。

#### 转换Excel

https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.DataFrame.to_excel.html

```
DataFrame.to_excel()
DataFrame.to_excel(excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None)
```

参数：

**excel_writer** : 字符串或 ExcelWriter 对象

> 文件路径或现有 ExcelWriter

**sheet_name** : 字符串，默认为 'Sheet1'

> 将包含 DataFrame 的工作表名称

**na_rep** : 字符串，默认 ''

> 缺少数据表示

**float_format** : 字符串，默认无

> 浮点数的格式字符串

**列**：序列，可选

> 要写的列

**header** : 布尔值或字符串列表，默认为 True

> 写出列名。如果给出字符串列表，则假定它是列名的别名

**index** : 布尔值，默认为 True

> 写行名（索引）

**index_label** : 字符串或序列，默认无

> 如果需要，索引列的列标签。如果给出 None，并且 header和index为 True，则使用索引名称。如果 DataFrame 使用 MultiIndex，则应给出一个序列。

**开始行：**

> 左上角单元格行转储数据帧

**起始点：**

> 左上角单元格列转储数据框

**引擎**：字符串，默认无

> 编写要使用的引擎 - 您也可以通过选项 `io.excel.xlsx.writer`、`io.excel.xls.writer`和 `io.excel.xlsm.writer`.

**merge_cells**：布尔值，默认为 True

> 将 MultiIndex 和 Hierarchical Rows 写入合并单元格。

**编码：字符串，默认无**

> 生成的excel文件的编码。只有 xlwt 需要，其他编写器原生支持 unicode。

**inf_rep** : 字符串，默认 'inf'

> 无穷大的表示（Excel 中没有无穷大的本地表示）

**freeze_panes**：整数元组（长度为 2），默认无

> 指定要冻结的从 1 开始的最底行和最右列
>
> *0.20.0 版中的新功能。*

### pandas.data_range

https://pandas.pydata.org/docs/reference/api/pandas.date_range.html

按照指定的时间区间与时间间隔生成序列

```
pandas.date_range(start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=NoDefault.no_default, inclusive=None, **kwargs)
```



## import psutil



## import os

查看文件权限：

返回bool值

```
os.access()
```

os.F_OK: 检查文件或文件夹是否存在;

os.R_OK: 检查文件或文件夹是否可读;

os.W_OK: 检查文件或文件夹是否可以写入;

os.X_OK: 检查文件或文件夹是否可以执行

## os.system()

运行系统命令

## file 文件IO

### with

Python 中的 **with** 语句用于异常处理，封装了 **try…except…finally** 编码范式，提高了易用性。

**with** 语句使代码更清晰、更具可读性， 它简化了文件流等公共资源的管理。

在处理文件对象时使用 with 关键字是一种很好的做法

使用 **with** 关键字系统会自动调用 f.close() 方法， with 的作用等效于 try/finally 语句是一样的。

```
with open(file_name,'rb') as f:

```

#### 原理

with 语句实现原理建立在上下文管理器之上。

上下文管理器是一个实现 **__enter__** 和 **__exit__** 方法的类。

使用 with 语句确保在嵌套块的末尾调用 __exit__ 方法。

这个概念类似于 try...finally 块的使用。

### 创建新文件

```
os.mknod(filename)
os.open()
```

### file.open()

```
open(file, mode='r')
```

| r    | 以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。 |
| ---- | :----------------------------------------------------------- |
| rb   | 以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。一般用于非文本文件如图片等。 |
| r+   | 打开一个文件用于读写。文件指针将会放在文件的开头。           |
| w    | 打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。 |
| wb   | 以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。 |
| w+   | 打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。 |
| a    | 打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
| ab   | 以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
| a+   | 打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。 |
|      |                                                              |

### file.read ()

read（）方法从一个打开的文件中读取一个字符串。需要重点注意的是，Python字符串可以是二进制数据，而不是仅仅是文字。

`f.read([count])` count : 读取字节数

read()默认会读取整个文件，将文件内容存放到一个字符变量中

### f.readlines()

按列读取文件，返回由列组成的列表（list）

### f.readline()

每次读取一列，没怎么用过，效率较低。

### file.write([str])

str : 要写入文件的字符串

返回写入的字符长度

### file.tell()

定位文件读写指针

### file.seek(offset)

设置文件读写指针位置

## shell

### 退出

ctrl d 或者输入`exit()`

## urllib

### `urllib.request` 打开和读取URL

`urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)`

- **url**：url 地址。
- **data**：发送到服务器的其他数据对象，默认为 None。
- **timeout**：设置访问超时时间。
- **cafile 和 capath**：cafile 为 CA 证书， capath 为 CA 证书的路径，使用 HTTPS 需要用到。
- **cadefault**：已经被弃用。
- **context**：ssl.SSLContext类型，用来指定 SSL 设置。  

---

#### urllib.request.Request类：模拟头部信息

`class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)`

- **url**：url 地址。
- **data**：发送到服务器的其他数据对象，默认为 None。
- **headers**：HTTP 请求的头部信息，字典格式。
- **origin_req_host**：请求的主机地址，IP 或域名。
- **unverifiable**：很少用这个参数，用于设置网页是否需要验证，默认是False。
- **method**：请求方法， 如 GET、POST、DELETE、PUT等。







### `urlib.error`异常信息

包含两个方法

URLError:

OSError的一个子类，处理程序出错时引发，包含的属性reason异常原因

HTTPError:

URLError的一个子类，处理特殊HTTP错误

属性： code -状态码    reason异常原因	headers -http响应头

### `urllib.parse`解析URL

`urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)`

- **urlstring** : url地址
- **scheme**   :  协议类型
- **allow_fragment**   :  参数为 false，则无法识别片段标识符。相反，它们被解析为路径，参数或查询组件的一部分，并 fragment 在返回值中设置为空字符串。

`urllib.parse.encode` 对参数进行编码

`urllib.prase.decode` 对参数进行解码

###  `urllib.robotparser`解析robots.txt文件



## dir

**dir()** 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；

带参数时，返回参数的属性、方法列表。如果参数包含方法\_\_dir\_\_()，该方法将被调用。如果参数不包含\_\_dir\_\_()，该方法将最大限度地收集参数信息。

`dir([object])`

## 正则表达式 RE

匹配数字

```
\d
```



```
re.match(pattern,string)
match要求完全匹配

re.search(pattern,string)
rearch只需要存在即可，类似 in

re.sub(pattern,repl,string)
将string中匹配的部分用repl替换

re.findall(pattern,string,flags=0)
查找字符串中所有和模式匹配的子串放入列表
```









## 格式化输出

### 缩进:\t

### 换行:\n

### 设置字符串的颜色

\033[3;

字体颜色

\033[4;

背景颜色



## 运算符

/ : 除法，结果是小数。即便能整除也是小数

% : 取模

// : 求商，结果是整数（往小取整）

** 求幂



## 字符串

单引号，双引号，三引号都可以，分行写时用\连接

# global

在函数内部对函数外的变量进行操作时，需要在函数内部声明为global

# OpenCv

## 图像

```
cv.imread(path, flag)
```

path:图像路径
flag:
**cv.IMREAD_COLOR**：加载彩色图像，任何图像的透明度都会被忽略，它是默认标志
**cv.IMREAD_GRAYSCALE**：以灰度模式加载图像
**cv.IMREAD_UNCHANGED**：加载图像，包括 alpha 通道

```
cv.imshow(name, image)
```

第一个参数是窗口名，它是一个字符串，第二个参数就是我们的图像。你可以根据需要创建任意数量的窗口，但是窗口名字要不同。

```
cv.waitkey()
```

一个键盘绑定函数，它的参数是以毫秒为单位的时间。该函数为任意键盘事件等待指定毫秒。如果你在这段时间内按下任意键，程序将继续。如果传的是 0，它会一直等待键盘按下

```
cv.destroyAllWindows()
```

简单的销毁我们创建的所有窗口。如果你想销毁任意指定窗口，应该使用函数 **[cv.destroyWindow()](https://docs.opencv.org/4.0.0/d7/dfc/group__highgui.html#ga851ccdd6961022d1d5b4c4f255dbab34)** 参数是确切的窗口名

```
cv.namedWindow(name, flag)
```

默认情况下，flag 是 **[cv.WINDOW_AUTOSIZE](https://docs.opencv.org/4.0.0/d7/dfc/group__highgui.html#ggabf7d2c5625bc59ac130287f925557ac3acf621ace7a54954cbac01df27e47228f)**。但如果你指定了 flag 为 **[cv.WINDOW_NORMAL](https://docs.opencv.org/4.0.0/d7/dfc/group__highgui.html#ggabf7d2c5625bc59ac130287f925557ac3a29e45c5af696f73ce5e153601e5ca0f1)**，你能调整窗口大小。当图像尺寸太大，在窗口中添加跟踪条是很有用的。

```
cv.imwrite(name, img)
```

第一个参数是文件名，第二个参数是你要保存的图像。

### 关于Matplotlib

Matplotlib 是一个 Python 的绘图库，提供了丰富多样的绘图函数。

彩色图像 OpenCV 用的 BGR 模式，但是 Matplotlib 显示用的 RGB 模式,使用Matplotlib显示opencv读取的彩色图像时需要进行转换：

```
1. img2 = img[:, :, ::-1]
2. img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

### cv.get()

```
enum cv::VideoCaptureProperties {
  cv::CAP_PROP_POS_MSEC =0,
  cv::CAP_PROP_POS_FRAMES =1,
  cv::CAP_PROP_POS_AVI_RATIO =2,
  cv::CAP_PROP_FRAME_WIDTH =3,
  cv::CAP_PROP_FRAME_HEIGHT =4,
  cv::CAP_PROP_FPS =5,
  cv::CAP_PROP_FOURCC =6,
  cv::CAP_PROP_FRAME_COUNT =7,
  cv::CAP_PROP_FORMAT =8,
  cv::CAP_PROP_MODE =9,
  cv::CAP_PROP_BRIGHTNESS =10,
  cv::CAP_PROP_CONTRAST =11,
  cv::CAP_PROP_SATURATION =12,
  cv::CAP_PROP_HUE =13,
  cv::CAP_PROP_GAIN =14,
  cv::CAP_PROP_EXPOSURE =15,
  cv::CAP_PROP_CONVERT_RGB =16,
  cv::CAP_PROP_WHITE_BALANCE_BLUE_U =17,
  cv::CAP_PROP_RECTIFICATION =18,
  cv::CAP_PROP_MONOCHROME =19,
  cv::CAP_PROP_SHARPNESS =20,
  cv::CAP_PROP_AUTO_EXPOSURE =21,
  cv::CAP_PROP_GAMMA =22,
  cv::CAP_PROP_TEMPERATURE =23,
  cv::CAP_PROP_TRIGGER =24,
  cv::CAP_PROP_TRIGGER_DELAY =25,
  cv::CAP_PROP_WHITE_BALANCE_RED_V =26,
  cv::CAP_PROP_ZOOM =27,
  cv::CAP_PROP_FOCUS =28,
  cv::CAP_PROP_GUID =29,
  cv::CAP_PROP_ISO_SPEED =30,
  cv::CAP_PROP_BACKLIGHT =32,
  cv::CAP_PROP_PAN =33,
  cv::CAP_PROP_TILT =34,
  cv::CAP_PROP_ROLL =35,
  cv::CAP_PROP_IRIS =36,
  cv::CAP_PROP_SETTINGS =37,
  cv::CAP_PROP_BUFFERSIZE =38,
  cv::CAP_PROP_AUTOFOCUS =39,
  cv::CAP_PROP_SAR_NUM =40,
  cv::CAP_PROP_SAR_DEN =41,
  cv::CAP_PROP_BACKEND =42,
  cv::CAP_PROP_CHANNEL =43,
  cv::CAP_PROP_AUTO_WB =44,
  cv::CAP_PROP_WB_TEMPERATURE =45
}
```



## 视频

### VideoCapture

去获取一个视频，你需要创建一个**VideoCapture**对象。它的参数可以是设备索引或者一个视频文件名。

```
cap = cv.VideoCapture(0)
```

#### cap.read()

**[cap.read()](https://docs.opencv.org/4.0.0/d2/d75/namespacecv.html#a9afba2f5b9bf298c62da8cf66184e41f)** 返回一个 bool 值(`True`/`False`)。如果加载成功，它会返回`True`。因此，你可以通过这个返回值判断视频是否结束。

有时，cap 可能没有初始化 capture。在这种情况下，此代码显示错误。你可以通过该方法 **cap.isOpened()** 检查它是否初始化。如果它是 True，那么是好的，否则用 **[cap.open()](https://docs.opencv.org/4.0.0/d6/dee/group__hdf5.html#ga243d7e303690af3c5c3686ca5785205e)** 打开在使用。



#### cap.get(propId)

你也可以通过使用 **cap.get(propId)** 函数获取一些视频的特征，这里的 propld 是一个 0-18 的数字，每个数字代表视频的一个特征 (如果这个视频有)，或者使用cv:VideoCapture:get()获取全部细节。它们中有些值可以使用 **cap.set(propId, value)** 修改。Value 就是你想要的新值



### 播放视频

#### cv.waitkey()

如果它太小，视频将非常快，如果太大，视频将很慢 (嗯，这就是如何显示慢动作)。正常情况下，25 毫秒就可以了。

### 保存视频

建一个 **VideoWriter** 对象。我们应该指定输出文件的名字 (例如：output.avi)。然后我们应该指定 **FourCC** 码 (下一段有介绍)。然后应该传递每秒帧数和帧大小。最后一个是 **isColor** flag。如果是 True，编码器期望彩色帧，否则它适用于灰度帧。

```
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi',fourcc, 20.0, (640,480))
```

**[FourCC](http://en.wikipedia.org/wiki/FourCC)** 是用于指定视频解码器的 4 字节代码。这里 **[fourcc.org](http://www.fourcc.org/codecs.php)** 是可用编码的列表。它取决于平台，下面编码就很好。

- In Fedora: DIVX, XVID, MJPG, X264, WMV1, WMV2. (XVID 是最合适的. MJPG 结果比较大. X264 结果比较小)
- In Windows: DIVX (还需要测试和添加跟多内容)
- In OSX: MJPG (.mp4), DIVX (.avi), X264 (.mkv).

#### 编码大小

尝试过XVID, MJPG,MP4V

```
XVID(.avi) 大小和MP4V接近，略高
MJEP(.avi) 极大
MP4V(mp4)目前最小的
```



#### **保存视频失败的问题

保存视频时设置的视频尺寸，必须要与读到的每帧图片大小一致，两种解决办法

```
1. 修改cv.VideoWriter中视频尺寸参数，可以通过cap.get()函数获取图片的宽和高
2. 修改图片大小，使用cv.resize(frame, (width, height))
```



# conda

## conda 不可用（以zsh客户端为例，如bash则是~/.bashrc）

添加conda环境变量

```
vim ~/.zshrc
export PATH=/home/caofangyu/anaconda3/bin:$PATH   ****此处需要根据自己实际情况输入
source ~/.zshrc					 在终端中运行
```

之后在zsh中运行

```
conda init zsh
运行conda init后需要重启shell才生效
```



## 查看环境

```
conda env list	
```

## 创建环境

```
conda create -n ENV python=x.x
```



## 激活环境

```
conda activate ENV
conda deactivate ENV
```



# 使用C或C++扩展Python

