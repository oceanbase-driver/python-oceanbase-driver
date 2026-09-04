# Changelog

## v1.0.0

* 首版。基线：上游 `PyMySQL 1.2.0`。
* 默认置上握手包 capability bit27（`QUERY_ATTRIBUTES`），
  OceanBase Oracle 租户可直接用 MySQL 协议登录；否则服务端报
  `Error 1235: Oracle tenant for current client driver is not supported`。
* 与上游互斥安装（同为 `pymysql` 包），二选一。
* 已在 OceanBase 4.2.1.11 Oracle 租户验证：连接、查询、绑定变量、
  建表写入、事务提交回滚。
