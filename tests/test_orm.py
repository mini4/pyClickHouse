import pytest

from clickhouse import ClickHouse, Column, Database, F, Index, Table, View, engines, types
from clickhouse.utils import unset


@pytest.fixture(autouse=True)
def clickhouse():
    yield ClickHouse
    ClickHouse._databases = {}


def test_clickhouse_declaration():
    ClickHouse2 = type('ClickHouse2', (ClickHouse,), {})
    assert ClickHouse != ClickHouse2


def test_database_declaration():
    City = type(
        'City',
        (Database,),
        {'__engine__': engines.MaterializedPostgreSQL('localhost', 'city')},
    )
    assert City.__clickhouse__ == ClickHouse
    assert City.__database_name__ == 'city'
    assert ClickHouse.database('city') == City


def test_abstract_database_declaration():
    City = type('City', (Database,), {'__abstract__': True})
    assert City.__clickhouse__ == ClickHouse
    assert not ClickHouse.database('city')


def test_database_declaration_in_different_clickhouses():
    ClickHouse2 = type('ClickHouse2', (ClickHouse,), {})
    assert ClickHouse != ClickHouse2
    assert not ClickHouse.database('shop')
    assert not ClickHouse2.database('shop')

    city_db = type('City', (Database,), {})
    assert ClickHouse.database('city') == city_db
    assert not ClickHouse2.database('city')

    shop_db = type('Shop', (Database,), {'__clickhouse__': ClickHouse2})
    assert not ClickHouse.database('shop')
    assert ClickHouse2.database('shop') == shop_db


def test_duplicated_database_declaration():
    type('City', (Database,), {})
    with pytest.raises(AssertionError):
        type('City', (Database,), {})


def test_table_declaration():
    Shop = type('Shop', (Database,), {})
    Product = type('Product', (Table,), {'__database__': Shop})
    assert Product.__table_name__ == 'product'
    assert Shop.table('product')


def test_abstract_table_declaration():
    Shop = type('Shop', (Database,), {})
    Product = type('Product', (Table,), {'__database__': Shop, '__abstract__': True})
    assert Product.__table_name__ == 'product'
    assert not Shop.table('product')


def test_table_declaration_in_abstract_database():
    with pytest.raises(AssertionError):
        type('Product', (Table,), {})


def test_view_declaration():
    Shop = type('Shop', (Database,), {})
    Product = type('Product', (View,), {'__database__': Shop})
    assert Product.__view_name__ == 'product'
    assert Shop.view('product')


def test_abstract_view_declaration():
    Shop = type('Shop', (Database,), {})
    Product = type('Product', (View,), {'__database__': Shop, '__abstract__': True})
    assert Product.__view_name__ == 'product'
    assert not Shop.view('product')


def test_view_declaration_in_abstract_database():
    with pytest.raises(AssertionError):
        type('Product', (View,), {})


@pytest.mark.parametrize('name', (unset, '', 'first_name'))
@pytest.mark.parametrize('default', (unset, '', 'Jon'))
@pytest.mark.parametrize('materialized', (unset, '', 'Jon'))
def test_column(name, default, materialized):
    try:
        col = Column(types.FixedString(6), default, materialized, name)
    except AssertionError:
        assert default != unset and materialized != unset
    else:
        assert col.type == types.FixedString(6)
        assert col.name == name
        assert col.default == default
        assert col.materialized == materialized


def test_index():
    col = Column(types.String, name='first_name')
    idx = Index(col, F.set(), 64, 'idx')
    assert idx.expr.name == 'first_name'
    assert idx.type.name == 'set'
    assert idx.granularity == 64
    assert idx.name == 'idx'


def test_table_items():
    Shop = type('Shop', (Database,), {})
    name_col = Column(types.String)
    Product = type(
        'Product',
        (Table,),
        {
            '__database__': Shop,
            'first_name': name_col,
            'idx': Index(name_col, F.set(), granularity=64),
        },
    )
    view_query = 'SELECT * FROM shop.product'
    ProductView = type(
        'ProductView',
        (View,),
        {
            '__database__': Shop,
            'first_name': Column(types.String),
            '__query__': view_query,
        },
    )

    assert Shop.table('product') == Product
    assert not Shop.view('product')
    assert Shop.table('product').column('first_name').type.name == 'String'
    assert Shop.table('product').index('idx').expr.name == 'first_name'
    assert Shop.view('product_view') == ProductView
    assert Shop.view('product_view').column('first_name').type.name == 'String'
    assert not Shop.table('product_view')
