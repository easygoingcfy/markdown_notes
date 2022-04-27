# SQLite基础

### 创建数据库

```
$ sqlite3 DatabaseName.db
```

```
sqlite>.open test.db
```

上面的命令创建了数据库文件 test.db，位于 sqlite3 命令同一目录下。

打开已存在数据库也是用 **.open** 命令，以上命令如果 **test.db** 存在则直接会打开，不存在就创建它。

### 查看数据库列表

```
sqlite>.databases
```

### .dump 命令

您可以在命令提示符中使用 SQLite **.dump** 点命令来导出完整的数据库在一个文本文件中，如下所示：

```
$sqlite3 testDB.db .dump > testDB.sql
```

上面的命令将转换整个 **testDB.db** 数据库的内容到 SQLite 的语句中，并将其转储到 ASCII 文本文件 **testDB.sql** 中。您可以通过简单的方式从生成的 testDB.sql 恢复，如下所示：

```
$sqlite3 testDB.db < testDB.sql
```

此时的数据库是空的，一旦数据库中有表和数据，您可以尝试上述两个程序。现在，让我们继续学习下一章。

### SQLite 附加数据库

假设这样一种情况，当在同一时间有多个数据库可用，您想使用其中的任何一个。SQLite 的 **ATTACH DATABASE** 语句是用来选择一个特定的数据库，使用该命令后，所有的 SQLite 语句将在附加的数据库下执行。

#### 语法

SQLite 的 ATTACH DATABASE 语句的基本语法如下：

```
ATTACH DATABASE file_name AS database_name;
```

如果数据库尚未被创建，上面的命令将创建一个数据库，如果数据库已存在，则把数据库文件名称与逻辑数据库 'Alias-Name' 绑定在一起。

打开的数据库和使用 ATTACH附加进来的数据库的必须位于同一文件夹下。

#### 实例

如果想附加一个现有的数据库 **testDB.db**，则 ATTACH DATABASE 语句将如下所示：

```
sqlite> ATTACH DATABASE 'testDB.db' as 'TEST';
```

使用 SQLite **.database** 命令来显示附加的数据库。

### SQLite 分离数据库

SQLite 的 **DETACH DATABASE** 语句是用来把命名数据库从一个数据库连接分离和游离出来，连接是之前使用 ATTACH 语句附加的。如果同一个数据库文件已经被附加上多个别名，DETACH 命令将只断开给定名称的连接，而其余的仍然有效。您无法分离 **main** 或 **temp** 数据库。

> 如果数据库是在内存中或者是临时数据库，则该数据库将被摧毁，且内容将会丢失。

#### 语法

SQLite 的 DETACH DATABASE 'Alias-Name' 语句的基本语法如下：

```
DETACH DATABASE 'Alias-Name';
```

在这里，'Alias-Name' 与您之前使用 ATTACH 语句附加数据库时所用到的别名相同。

#### 实例

假设在前面的章节中您已经创建了一个数据库，并给它附加了 'test' 和 'currentDB'，使用 .database 命令，我们可以看到：

```
sqlite>.databases
seq  name             file
---  ---------------  ----------------------
0    main             /home/sqlite/testDB.db
2    test             /home/sqlite/testDB.db
3    currentDB        /home/sqlite/testDB.db
```

现在，让我们尝试把 'currentDB' 从 testDB.db 中分离出来，如下所示：

```
sqlite> DETACH DATABASE 'currentDB';
```

### SQLite 创建表

SQLite 的 **CREATE TABLE** 语句用于在任何给定的数据库创建一个新表。创建基本表，涉及到命名表、定义列及每一列的数据类型。

#### 语法

CREATE TABLE 语句的基本语法如下：

```
CREATE TABLE database_name.table_name(
   column1 datatype  PRIMARY KEY(one or more columns),
   column2 datatype,
   column3 datatype,
   .....
   columnN datatype,
);
```

CREATE TABLE 是告诉数据库系统创建一个新表的关键字。CREATE TABLE 语句后跟着表的唯一的名称或标识。您也可以选择指定带有 *table_name* 的 *database_name*。

#### 实例

下面是一个实例，它创建了一个 COMPANY 表，ID 作为主键，NOT NULL 的约束表示在表中创建纪录时这些字段不能为 NULL：

```
sqlite> CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);
```

让我们再创建一个表，我们将在随后章节的练习中使用：

```
sqlite> CREATE TABLE DEPARTMENT(
   ID INT PRIMARY KEY      NOT NULL,
   DEPT           CHAR(50) NOT NULL,
   EMP_ID         INT      NOT NULL
);
```

您可以使用 SQLIte 命令中的 **.tables** 命令来验证表是否已成功创建，该命令用于列出附加数据库中的所有表。

```
sqlite>.tables
COMPANY     DEPARTMENT
```

在这里，可以看到我们刚创建的两张表 COMPANY、 DEPARTMENT。

您可以使用 SQLite **.schema** 命令得到表的完整信息，如下所示：

```
sqlite>.schema COMPANY
CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);
```

### SQLite 删除表

SQLite 的 **DROP TABLE** 语句用来删除表定义及其所有相关数据、索引、触发器、约束和该表的权限规范。

> 使用此命令时要特别注意，因为一旦一个表被删除，表中所有信息也将永远丢失。

#### 语法

DROP TABLE 语句的基本语法如下。您可以选择指定带有表名的数据库名称，如下所示：

```
DROP TABLE database_name.table_name;
```

#### 实例

让我们先确认 COMPANY 表已经存在，然后我们将其从数据库中删除。

```
sqlite>.tables
COMPANY       test.COMPANY
```

这意味着 COMPANY 表已存在数据库中，接下来让我们把它从数据库中删除，如下：

```
sqlite>DROP TABLE COMPANY;
sqlite>
```

现在，如果尝试 .TABLES 命令，那么将无法找到 COMPANY 表了：

```
sqlite>.tables
sqlite>
```

显示结果为空，意味着已经成功从数据库删除表。

### SQLite Insert 语句

SQLite 的 **INSERT INTO** 语句用于向数据库的某个表中添加新的数据行。

#### 语法

INSERT INTO 语句有两种基本语法，如下所示：

```
INSERT INTO TABLE_NAME [(column1, column2, column3,...columnN)]  
VALUES (value1, value2, value3,...valueN);
```

在这里，column1, column2,...columnN 是要插入数据的表中的列的名称。

如果要为表中的所有列添加值，您也可以不需要在 SQLite 查询中指定列名称。但要确保值的顺序与列在表中的顺序一致。SQLite 的 INSERT INTO 语法如下：

```
INSERT INTO TABLE_NAME VALUES (value1,value2,value3,...valueN);
```

#### 实例

假设您已经在 testDB.db 中创建了 COMPANY表，如下所示：

```
sqlite> CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);
```

现在，下面的语句将在 COMPANY 表中创建六个记录：

```
INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (1, 'Paul', 32, 'California', 20000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (2, 'Allen', 25, 'Texas', 15000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (3, 'Teddy', 23, 'Norway', 20000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (5, 'David', 27, 'Texas', 85000.00 );

INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (6, 'Kim', 22, 'South-Hall', 45000.00 );
```

您也可以使用第二种语法在 COMPANY 表中创建一个记录，如下所示：

```
INSERT INTO COMPANY VALUES (7, 'James', 24, 'Houston', 10000.00 );
```

上面的所有语句将在 COMPANY 表中创建下列记录。下一章会教您如何从一个表中显示所有这些记录。

```
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          South-Hall  45000.0
7           James       24          Houston     10000.0
```

#### 使用一个表来填充另一个表

您可以通过在一个有一组字段的表上使用 select 语句，填充数据到另一个表中。下面是语法：

```
INSERT INTO first_table_name [(column1, column2, ... columnN)] 
   SELECT column1, column2, ...columnN 
   FROM second_table_name
   [WHERE condition];
```

您暂时可以先跳过上面的语句，可以先学习后面章节中介绍的 SELECT 和 WHERE 子句。

### SQLite Select 语句

SQLite 的 **SELECT** 语句用于从 SQLite 数据库表中获取数据，以结果表的形式返回数据。这些结果表也被称为结果集。

#### 语法

SQLite 的 SELECT 语句的基本语法如下：

```
SELECT column1, column2, columnN FROM table_name;
```

在这里，column1, column2...是表的字段，他们的值即是您要获取的。如果您想获取所有可用的字段，那么可以使用下面的语法：

```
SELECT * FROM table_name;
```

#### 实例

假设 COMPANY 表有以下记录：

```
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          South-Hall  45000.0
7           James       24          Houston     10000.0
```

下面是一个实例，使用 SELECT 语句获取并显示所有这些记录。在这里，前两个个命令被用来设置正确格式化的输出。

```
sqlite>.header on
sqlite>.mode column
sqlite> SELECT * FROM COMPANY;
```

最后，将得到以下的结果：

```
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          South-Hall  45000.0
7           James       24          Houston     10000.0
```

如果只想获取 COMPANY 表中指定的字段，则使用下面的查询：

```
sqlite> SELECT ID, NAME, SALARY FROM COMPANY;
```

上面的查询会产生以下结果：

```
ID          NAME        SALARY
----------  ----------  ----------
1           Paul        20000.0
2           Allen       15000.0
3           Teddy       20000.0
4           Mark        65000.0
5           David       85000.0
6           Kim         45000.0
7           James       10000.0
```

#### 设置输出列的宽度

有时，由于要显示的列的默认宽度导致 **.mode column**，这种情况下，输出被截断。此时，您可以使用 **.width num, num....** 命令设置显示列的宽度，如下所示：

```
sqlite>.width 10, 20, 10
sqlite>SELECT * FROM COMPANY;
```

上面的 **.width** 命令设置第一列的宽度为 10，第二列的宽度为 20，第三列的宽度为 10。因此上述 SELECT 语句将得到以下结果：

```
ID          NAME                  AGE         ADDRESS     SALARY
----------  --------------------  ----------  ----------  ----------
1           Paul                  32          California  20000.0
2           Allen                 25          Texas       15000.0
3           Teddy                 23          Norway      20000.0
4           Mark                  25          Rich-Mond   65000.0
5           David                 27          Texas       85000.0
6           Kim                   22          South-Hall  45000.0
7           James                 24          Houston     10000.0
```

#### Schema 信息

因为所有的**点命令**只在 SQLite 提示符中可用，所以当您进行带有 SQLite 的编程时，您要使用下面的带有 **sqlite_master** 表的 SELECT 语句来列出所有在数据库中创建的表：

```
sqlite> SELECT tbl_name FROM sqlite_master WHERE type = 'table';
```

假设在 testDB.db 中已经存在唯一的 COMPANY 表，则将产生以下结果：

```
tbl_name
----------
COMPANY
```

您可以列出关于 COMPANY 表的完整信息，如下所示：

```
sqlite> SELECT sql FROM sqlite_master WHERE type = 'table' AND tbl_name = 'COMPANY';
```

假设在 testDB.db 中已经存在唯一的 COMPANY 表，则将产生以下结果：

```
CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
)
```



# SQLAlchemy

## 建立与数据库的连接

### sqlite示例

**create_engine()** 函数创建 engine 对象，不同的数据库有不同的 database url。比如连接到 sqlite 的 testdb 数据库：

```
from sqlalchemy import create_engine
engine = create_engine("sqlite:///testdb.db")
```

典型的 database url 语法规则:

```
dialect+driver://username:password@host:port/database
```

### mysql 数据库连接示例

```
# 使用pymysql驱动连接到mysql
engine = create_engine('mysql+pymysql://user:pwd@localhost/testdb')
```

### sql server 数据库连接示例

```
# 使用pymssql驱动连接到sql server
engine = create_engine('mssql+pymssql://user:pwd@localhost:1433/testdb')
```

## 建立映射关系

数据库与 Python 对象的映射主要在体现三个方面：

- 数据库表 (table）映射为 Python 的类 (class)，称为 model
- 表的字段 (field) 映射为 Column
- 表的记录 (record）以类的实例 (instance) 来表示

sqlalchemy 支持两种方式创建映射，最常见的是通过下面的方式，这种方式被称为**声明式映射** (Declarative Mapping)，声明式映射与命令式映射 (imperative mapping) 相对。

```
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    EMP_ID = Column(SmallInteger, primary_key=True)
    FIRST_NAME = Column(String(255))
    LAST_NAME = Column(String(255))
    GENDER = Column(String(255))
    AGE = Column(SmallInteger)
    EMAIL = Column(String(255))
    PHONE_NR = Column(String(255))
    EDUCATION = Column(String(255))
    MARITAL_STAT = Column(String(255))
    NR_OF_CHILDREN = Column(SmallInteger)  
```

以上代码的作用是：通过 declarative_base() 函数创建 Base 类，Base 类本质上是 一个 registry 对象，Base 作为所有 model 类的父类，将在子类中把声明式映射过程作用于其子类。

### 替代办法

在实际编码的时候，常见的方式是先在数据库中建表，然后再用代码操作数据库。上面这种声明式定义映射模型，对 Column 的声明是很枯燥的。如果表的字段很多，这种枯燥的代码编写也是很痛苦的事情。

#### sqlacodegen

解决办法有两个，方法一是安装 sqlacodegen 库 (pip 安装方式)，然后通过下面的命令，基于数据库中的表自动生成 model 映射的代码。sqlacodegen 用法如下：

```
# 将数据库中所有表导出为 model
sqlacodegen sqlite:///testdb.db --outfile=models.py
```

sqlacodegen 使用与 sqlalchemy 相同的 database url。如果只关心部分表的模型导出，使用 tables 参数：

```
# 指定导出的表导出model
sqlacodegen sqlite:///testdb.db --outfile=models.py -- tables users, addresses
```

为准备后面单表的 CRUD 操作，我用 sqlacodegen 命令创建 employees 表的 model 映射代码：

```
sqlacodegen sqlite:///testdb.db --outfile=employee_model.py --tables employees
```

生成的代码文件 employee_model.py 内容如下：

```
from sqlalchemy import Column, SmallInteger, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Employee(Base):
    __tablename__ = 'employees'

    EMP_ID = Column(SmallInteger, primary_key=True)
    FIRST_NAME = Column(Text(255))
    LAST_NAME = Column(Text(255))
    GENDER = Column(Text(255))
    AGE = Column(SmallInteger)
    EMAIL = Column(Text(255))
    PHONE_NR = Column(Text(255))
    EDUCATION = Column(Text(255))
    MARITAL_STAT = Column(Text(255))
    NR_OF_CHILDREN = Column(SmallInteger)

```

#### 设置autoload

第二种方法，在构建 model 的时候，使用 autoload = True，sqlalchemy 依据数据库表的字段结构，自动加载 model 的 Column。使用这种方法时，在构建 model 之前，Base 类要与 engine 进行绑定。下面的代码演示了 autoload 模式编写 model 映射的方法：

```
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table

engine = create_engine("sqlite:///testdb.db")
Base = declarative_base()
metadata = Base.metadata
metadata.bind = engine

class Employee(Base):
    __table__ = Table("employees", metadata, autoload=True)
```

## CRUD

### 单表CRUD

SQLAlchemy 操作数据库，需要引入另外一个对象 Session。Session 建立与数据库的会话 (conversation)，可以将其想象成对象的容器，包含的对象叫 identity map 的结构，identity map 的作用就是保证对象的唯一性。另外，Session 对 Python 对象进行状态管理，后面我会说明。

首先，需要构建一个 Session 对象，比较常用的方式是使用 sessionmaker() 函数来创建一个 global 的 Session Factory，进行调用后就生成 Session 对象：

```
engine = create_engine("sqlite:///testdb.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
```

#### 查询记录

第一种方式是将 model 类作为参数传递给 query() 方法

```
session.query(Employee)
```

#### 筛选记录

Query 对象提供了 filter() 方法和 filter_by() 方法用于数据筛选。filter_by() 适用于简单的基于关键字参数的筛选。 filter() 适用于复杂条件的表达。比如，我们要找出 EMP_ID 为 1001 的雇员信息，filter_by 和 filter 都是可以的：

```
def test_filtered_query(self):
    emp = session.query(Employee).filter_by(EMP_ID='1001').first()
    print(emp)

def test_filtered_query2(self):
    emp = session.query(Employee).filter(Employee.EMP_ID == '1001').first()
    print(emp)
```

filter可以接受条件表达式作为输入。

## 排序

### 直接使用order_by

```
results = session.query(User).order_by(User.create_time.desc()).all()　
print(results)
```

### 传入字段名

```
from sqlalchemy import desc

#order_by降序并取第一条数据，如果不取第一条，直接把first()方法去掉
query.order_by(desc(“create_time”)).first()

#order_by升序并取第一条数据，如果不取第一条，直接把first()方法去掉
query.order_by(“create_time”).first()
```

