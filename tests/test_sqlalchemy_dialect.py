"""无真库测试：oceanbase / oceanbase_oracle dialect 注册、解析与 SQL 生成。"""

import pyoceanbase
from pyoceanbase.sqlalchemy import OceanBaseDialect_pyoceanbase
from pyoceanbase.sqlalchemy_oracle import OceanBaseOracleDialect_pyoceanbase


def test_mysql_dialect_identity():
    d = OceanBaseDialect_pyoceanbase()
    assert d.name == "oceanbase"
    assert d.driver == "pyoceanbase"
    assert d.import_dbapi() is pyoceanbase


def test_oracle_dialect_identity():
    d = OceanBaseOracleDialect_pyoceanbase()
    assert d.name == "oceanbase_oracle"
    assert d.driver == "pyoceanbase"
    assert d.import_dbapi() is pyoceanbase
    # RETURNING/identity 在 MySQL 协议上跑不了，v1 必须关掉走 Sequence
    assert d.insert_returning is False
    assert d.supports_identity_columns is False


def test_engine_url_no_connection():
    sqlalchemy = __import__("pytest").importorskip("sqlalchemy")
    from sqlalchemy.dialects import registry

    registry.register(
        "oceanbase.pyoceanbase",
        "pyoceanbase.sqlalchemy",
        "OceanBaseDialect_pyoceanbase",
    )
    registry.register(
        "oceanbase", "pyoceanbase.sqlalchemy", "OceanBaseDialect_pyoceanbase"
    )
    registry.register(
        "oceanbase_oracle.pyoceanbase",
        "pyoceanbase.sqlalchemy_oracle",
        "OceanBaseOracleDialect_pyoceanbase",
    )
    registry.register(
        "oceanbase_oracle",
        "pyoceanbase.sqlalchemy_oracle",
        "OceanBaseOracleDialect_pyoceanbase",
    )

    from sqlalchemy import create_engine

    e = create_engine("oceanbase+pyoceanbase://u:p@127.0.0.1:2881/db")
    assert e.dialect.name == "oceanbase"
    assert e.dialect.driver == "pyoceanbase"

    e2 = create_engine("oceanbase://u:p@127.0.0.1:2881/db")
    assert e2.dialect.name == "oceanbase"

    # 用户名里的 @/# 必须百分号编码
    e3 = create_engine(
        "oceanbase_oracle+pyoceanbase://BSSP%40arcdbcs%23C:p@127.0.0.1:9090/DB"
    )
    assert e3.dialect.name == "oceanbase_oracle"
    assert e3.url.username == "BSSP@arcdbcs#C"
    assert e3.url.database == "DB"


def test_sql_generation_split():
    sqlalchemy = __import__("pytest").importorskip("sqlalchemy")
    from sqlalchemy import MetaData, Table, Column, Integer, String, Sequence
    from sqlalchemy.schema import CreateTable

    mysql_d = OceanBaseDialect_pyoceanbase()
    m = MetaData()
    t1 = Table(
        "t1",
        m,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    mysql_ddl = str(CreateTable(t1).compile(dialect=mysql_d))
    assert "AUTO_INCREMENT" in mysql_ddl

    ora_d = OceanBaseOracleDialect_pyoceanbase()
    m2 = MetaData()
    seq = Sequence("t2_seq")
    t2 = Table(
        "T2",
        m2,
        Column("id", Integer, seq, primary_key=True),
        Column("name", String(50)),
    )
    oracle_ddl = str(CreateTable(t2).compile(dialect=ora_d))
    assert "VARCHAR2" in oracle_ddl
    assert "AUTO_INCREMENT" not in oracle_ddl

    # 分页语法分家：MySQL 用 LIMIT，Oracle 用 FETCH FIRST
    assert "LIMIT" in str(t1.select().limit(1).compile(dialect=mysql_d))
    assert "FETCH FIRST" in str(t2.select().limit(1).compile(dialect=ora_d))
