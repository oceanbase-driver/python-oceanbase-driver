# Changelog

## v1.1.0

* 新增 SQLAlchemy 方言（`pip install "pyoceanbase[sqlalchemy]"`）：
  `oceanbase+pyoceanbase`（MySQL 租户，ORM 全功能）、
  `oceanbase_oracle+pyoceanbase`（Oracle 租户，MySQL 协议执行 +
  Oracle 语法编译，主键用 Sequence，不支持 identity/RETURNING）。
* 双租户真库验证：建表、写入、查询、分页、事务。

## v1.0.1

* 分发包改名 `pyoceanbase`，顶层 import 包同步改为 `pyoceanbase`，
  可与上游 PyMySQL 共存。
* 客户端标识改为 `pyoceanbase`。

## v1.0.0

* 首版。基线：上游 `PyMySQL 1.2.0`。
* 默认置上握手包 capability bit27（`QUERY_ATTRIBUTES`），
  OceanBase Oracle 租户可直接用 MySQL 协议登录；否则服务端报
  `Error 1235: Oracle tenant for current client driver is not supported`。
* 已在 OceanBase 4.2.1.11 Oracle 租户验证：连接、查询、绑定变量、
  建表写入、事务提交回滚。
