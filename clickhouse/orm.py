from .expr import ExprMixin
from .utils import convert_classname_to_tablename, unset


class ClickHouse:
    @classmethod
    def databases(cls):
        return cls.__dict__.get('_databases', {})

    @classmethod
    def _register(cls, database):
        assert database.__database_name__ not in cls.databases()
        cls._databases = cls.databases()
        cls._databases[database.__database_name__] = database

    @classmethod
    def database(cls, name):
        return cls.databases().get(name)


class _Name:
    '''
    The class is a descriptor for converting the class name to ClickHouse object name.

    '''

    def __get__(self, inst, cls=None):
        return convert_classname_to_tablename(cls.__name__)


class _Engine:
    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def __call__(self, *args):
        self.args = args
        return self


class _EnginesType(type):
    def __getattr__(cls, name):
        return _Engine(name)


class _Engines(metaclass=_EnginesType):
    ...


engines = _Engines
'''
The class for coding table and database engines.

Example:
    engines.MaterializedPostgreSQL('localhost', 'city')

'''


class _DatabaseType(type):
    def __init__(database, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not database.__dict__.get('__abstract__', False):
            database.__clickhouse__._register(database)


class Database(metaclass=_DatabaseType):
    '''
    The class for coding ClickHouse database.
    '''
    __abstract__ = True
    __clickhouse__ = ClickHouse
    __database_name__ = _Name()
    __engine__ = engines.Atomic

    @classmethod
    def _register(cls, obj):
        assert not cls.__dict__.get('__abstract__', False)
        if issubclass(obj, Table):
            assert obj.__table_name__ not in cls.tables()
            cls._tables = cls.tables()
            cls._tables[obj.__table_name__] = obj
        elif issubclass(obj, View):
            assert obj.__view_name__ not in cls.views()
            cls._views = cls.views()
            cls._views[obj.__view_name__] = obj

    @classmethod
    def tables(cls):
        return cls.__dict__.get('_tables', {})

    @classmethod
    def table(cls, table_name):
        return cls.tables().get(table_name)

    @classmethod
    def views(cls):
        return cls.__dict__.get('_views', {})

    @classmethod
    def view(cls, view_name):
        return cls.views().get(view_name)


class _DatabaseItemType(type):
    def __init__(item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not item.__dict__.get('__abstract__', False):
            item.__database__._register(item)


class _DatabaseItem(metaclass=_DatabaseItemType):
    __abstract__ = True
    __database__ = Database

    @classmethod
    def _register(cls, obj):
        if isinstance(obj, Column):
            assert not cls.column(obj.name)
            cls._columns = cls.columns()
            cls._columns.append(obj)
        elif isinstance(obj, Index):
            assert not issubclass(cls, View)
            assert not cls.index(obj.name)
            cls._indices = cls.indices()
            cls._indices.append(obj)

    @classmethod
    def columns(cls):
        return cls.__dict__.get('_columns', [])

    @classmethod
    def column(cls, name):
        for col in cls.columns():
            if col.name == name:
                return col

    @classmethod
    def indices(cls):
        return cls.__dict__.get('_indices', [])

    @classmethod
    def index(cls, name):
        for idx in cls.indices():
            if idx.name == name:
                return idx


class Table(_DatabaseItem):
    '''
    The class for coding ClickHouse table.
    '''
    __abstract__ = True
    __table_name__ = _Name()

    # TODO: rebuild to descriptor to use arbitrary name
    # TODO: save table metadata in specific structure
    __engine__ = engines.MergeTree
    __order_by__ = tuple()
    __partition_by__ = unset
    __ttl__ = unset
    __settings__ = unset

    __materialized_by__ = unset


class View(_DatabaseItem):
    '''
    The class for coding ClickHouse view.
    '''
    __abstract__ = True
    __view_name__ = _Name()

    __query__ = unset  # TODO: disallow view registration with unset query


class _TableItemMixin:
    def __set_name__(self, table, alias):
        self.table = table
        if self.name is unset:
            self.name = alias
        if alias not in ('__database__', '__engine__', '__partition_by__', '__order_by__'):
            table._register(self)


class Column(_TableItemMixin, ExprMixin):
    '''
    The class for coding table and view column.
    '''
    def __init__(self, type, default=unset, materialized=unset, name=unset):
        # TODO: add column option support: EPHEMERAL, ALIAS
        assert default is unset or materialized is unset
        self.type = type
        self.name = name
        self.default = default
        self.materialized = materialized


class Index(_TableItemMixin):
    '''
    The class for coding table index.
    '''
    def __init__(self, expr, type, granularity=64, name=unset):
        self.expr = expr
        self.name = name
        self.type = type
        self.granularity = granularity


class _ColumnType:
    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def __call__(self, *args):
        self.args = args
        return self

    def __eq__(self, other):
        return self.name == other.name and self.args == other.args


class _ColumnTypesType(type):
    def __getattr__(cls, name):
        return _ColumnType(name)


class _ColumnTypes(metaclass=_ColumnTypesType):
    ...


types = _ColumnTypes
