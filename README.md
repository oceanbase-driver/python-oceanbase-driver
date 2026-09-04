# python-oceanbase-driver

Python 的 OceanBase 驱动，基于 `PyMySQL 1.2.0`，纯 Python，用法与 PyMySQL 完全一致，
区别是默认置上握手包 capability bit27，可直连 OceanBase **Oracle 租户**。
未打补丁的 MySQL 协议驱动连 Oracle 租户会被服务端拒绝：

```text
pyoceanbase.err.NotSupportedError: (1235, 'Oracle tenant for current client driver is not supported')
```

原理：OceanBase 登录时检查该位（`OB_CLIENT_SUPPORT_ORACLE_MODE`，
与 MySQL 8.0 的 `CLIENT_QUERY_ATTRIBUTES` 同一位），mysql 8.0 客户端默认置位，
PyMySQL 默认没置。本驱动默认置上，对 MySQL / MariaDB / OB MySQL 租户无副作用。

## 安装

```shell
pip install pyoceanbase
```

注意：顶层包名为 `pyoceanbase`，可与上游 PyMySQL 共存于同一环境，按需选用。

## 用法

```python
import pyoceanbase

conn = pyoceanbase.connect(
    host="HOST",
    port=9090,
    user="USER@TENANT#CLUSTER",
    password="PASSWORD",
    database="DBNAME",
)
with conn.cursor() as cur:
    cur.execute("SELECT USER FROM DUAL")
    print(cur.fetchone())
conn.close()
```

## SQLAlchemy

```shell
pip install "pyoceanbase[sqlalchemy]"
```

MySQL 租户（`oceanbase+pyoceanbase`，ORM 全功能）：

```python
from sqlalchemy import create_engine

engine = create_engine("oceanbase+pyoceanbase://USER:PASSWORD@HOST:3306/DBNAME")
```

Oracle 租户（`oceanbase_oracle+pyoceanbase`，主键用 Sequence，不支持 identity/RETURNING）：

```python
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Sequence

# 用户名里的 @/# 必须百分号编码：@ -> %40，# -> %23
engine = create_engine("oceanbase_oracle+pyoceanbase://USER%40TENANT%23CLUSTER:PASSWORD@HOST:9090/DBNAME")

md = MetaData()
seq = Sequence("T_SEQ")
t = Table("T", md, Column("id", Integer, seq, primary_key=True), Column("name", String(50)))
md.create_all(engine)
```

注意：Oracle 租户须用 Oracle 方言写原生 SQL 时照常 `text("SELECT ... FROM DUAL")`，
表名建议大写；数字类型默认返回 `Decimal`。

## 注意事项

1. 业务 SQL 须用 Oracle 方言（如 `FROM DUAL`、`SYSDATE`）。
2. 默认 `autocommit=False`，写入后记得 `conn.commit()`（标准 PyMySQL 行为）。
3. 数字类型默认返回 `Decimal`（标准 PyMySQL 行为），可用 `conv` 覆盖。
4. DSN 参数等细节见上游文档：https://github.com/PyMySQL/PyMySQL

## 协议

MIT，与上游一致。
