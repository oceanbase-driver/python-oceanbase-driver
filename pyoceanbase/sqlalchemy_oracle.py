"""SQLAlchemy dialect for OceanBase Oracle tenant via pyoceanbase.

URL:
    oceanbase_oracle+pyoceanbase://USER@TENANT#CLUSTER:PASSWORD@HOST:PORT/DBNAME

MySQL 协议走 pyoceanbase，SQL 编译走 Oracle 方言（FETCH FIRST、
sequence、双引号、VARCHAR2/NUMBER）。v1 要求主键用 Sequence 显式声明，
identity/RETURNING 暂不支持。
"""

from sqlalchemy.dialects.oracle.base import OracleDialect

__all__ = ["OceanBaseOracleDialect_pyoceanbase"]


class OceanBaseOracleDialect_pyoceanbase(OracleDialect):
    name = "oceanbase_oracle"
    driver = "pyoceanbase"

    # pyoceanbase 只懂 pyformat/format，不懂 Oracle 的 named(:name)
    default_paramstyle = "pyformat"

    # cx_oracle 的 OUT 参数式 RETURNING 在 MySQL 协议上跑不了，
    # v1 用 Sequence 预取 + 直接 INSERT，不走 RETURNING 取回。
    insert_returning = False
    update_returning = False
    delete_returning = False
    supports_identity_columns = False

    supports_statement_cache = True

    @classmethod
    def import_dbapi(cls):
        import pyoceanbase

        return pyoceanbase

    @classmethod
    def dbapi(cls):
        # SQLAlchemy < 2.0 compat
        return cls.import_dbapi()

    def create_connect_args(self, url):
        # OracleDialect 默认吐 username/dsn，pyoceanbase 要 user/host/port，
        # 按 MySQL 那套映射，URL 里 @ 写 %40、# 写 %23。
        opts = url.translate_connect_args(
            database="database",
            username="user",
            password="password",
            host="host",
            port="port",
        )
        opts.update(url.query)
        return [], opts

    def _get_server_version_info(self, connection):
        # OB 报的是 4.2.1.11，Oracle 方言按 >=12 开 OFFSET/FETCH/identity，
        # 直接按 Oracle 19 报，保证现代语法全开；连通性已在真库验证。
        try:
            connection.exec_driver_sql("SELECT version FROM v$instance").scalar()
        except Exception:
            pass
        return (19, 0)

    def _get_effective_compat_server_version_info(self, connection):
        return self.server_version_info

    def is_disconnect(self, e, connection, cursor):
        # pyoceanbase 是 PyMySQL 语系，按 MySQL 断连码判，别用 Oracle 那套。
        try:
            dbapi = self.dbapi()
        except Exception:
            return False
        if isinstance(
            e,
            (
                dbapi.OperationalError,
                dbapi.ProgrammingError,
                dbapi.InterfaceError,
            ),
        ):
            code = None
            try:
                code = e.args[0] if e.args else None
            except Exception:
                pass
            if code in (1927, 2006, 2013, 2014, 2045, 2055, 4031):
                return True
        if isinstance(e, (dbapi.InterfaceError, dbapi.InternalError)):
            return "(0, '')" in str(e)
        return False


dialect = OceanBaseOracleDialect_pyoceanbase
