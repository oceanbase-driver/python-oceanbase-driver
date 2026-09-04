"""SQLAlchemy dialect for OceanBase MySQL tenant via pyoceanbase.

URL:
    oceanbase+pyoceanbase://USER:PASSWORD@HOST:PORT/DBNAME

Oracle 租户请用 oceanbase_oracle+pyoceanbase（见 pyoceanbase.sqlalchemy_oracle）。
"""

from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql

__all__ = ["OceanBaseDialect_pyoceanbase"]


class OceanBaseDialect_pyoceanbase(MySQLDialect_pymysql):
    name = "oceanbase"
    driver = "pyoceanbase"
    supports_statement_cache = True

    @classmethod
    def import_dbapi(cls):
        import pyoceanbase

        return pyoceanbase

    @classmethod
    def dbapi(cls):
        # SQLAlchemy < 2.0 compat
        return cls.import_dbapi()


# SQLAlchemy external dialect entry-point alias:
#   oceanbase.pyoceanbase -> this class
#   oceanbase (default driver) -> this class
dialect = OceanBaseDialect_pyoceanbase
