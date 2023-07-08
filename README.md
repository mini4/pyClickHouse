# pyClickHouse

## Usage

```
from clickhouse import Column, Database, F, Index, Table, View, engines, types


class Shop(Database):
    __engine__ = engines.Atomic


class Order(Table):
    __database__ = Shop

    id = Column(types.Int32)
    product_id = Column(types.Int32)
    delivery_date = Column(types.Date, default=F.today())
    quantity = Column(types.Int32)
    feedback = Column(types.Nullable(types.String))

    idx = Index(id, type=F.bloom_filter(0.01), granularity=64)


class Feedback(View):
    __database__ = Shop
    message = Column(types.String)
    __query__ = "SELECT feedback AS messsage FROM shop.order WHERE feedback IS NOT NULL"
```