# python-oceanbase-driver

Python 的 OceanBase 驱动，基于 `PyMySQL 1.2.0`，纯 Python，用法与 PyMySQL 完全一致，
区别是默认置上握手包 capability bit27，可直连 OceanBase **Oracle 租户**。
未打补丁的 MySQL 协议驱动连 Oracle 租户会被服务端拒绝：

```text
pymysql.err.NotSupportedError: (1235, 'Oracle tenant for current client driver is not supported')
```

原理：OceanBase 登录时检查该位（`OB_CLIENT_SUPPORT_ORACLE_MODE`，
与 MySQL 8.0 的 `CLIENT_QUERY_ATTRIBUTES` 同一位），mysql 8.0 客户端默认置位，
PyMySQL 默认没置。本驱动默认置上，对 MySQL / MariaDB / OB MySQL 租户无副作用。

## 安装

```shell
pip install "git+https://github.com/oceanbase-driver/python-oceanbase-driver.git@v1.0.0"
```

注意：本驱动与上游 PyMySQL 是同一个 `pymysql` 包，互斥安装，二选一。

## 用法

```python
import pymysql

conn = pymysql.connect(
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

## 注意事项

1. 业务 SQL 须用 Oracle 方言（如 `FROM DUAL`、`SYSDATE`）。
2. 默认 `autocommit=False`，写入后记得 `conn.commit()`（标准 PyMySQL 行为）。
3. 数字类型默认返回 `Decimal`（标准 PyMySQL 行为），可用 `conv` 覆盖。
4. DSN 参数等细节见上游文档：https://github.com/PyMySQL/PyMySQL

## 协议

MIT，与上游一致。
