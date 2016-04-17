# django-query-execfile
**Django module for execute sql query in a file**

Full documentation for the project is available at []

---

**Note**:


---

# Overview

django-query-execfile is a simple library for execute .sql query file.
Especially


# Requirements

* Python (2.7.x )
* Django (1.5+ )

# Installation

Install using `pip`...

```shell
pip install django-query-execfile
```


# Usage & Example

This is content of a .sql file

```sql
#sum_customerPayment_amount_rate_exchanged_group_by_day
SELECT
  DATE(customerPayment.created)                       AS created,
  SUM(transaction.amount * transaction.exchange_rate) AS amount_exchanged
FROM shop_module_customerpayment customerPayment
  LEFT JOIN shop_module_transaction transaction ON transaction.id = customerPayment.transaction_id
WHERE (customerPayment.created BETWEEN %(from_date)s AND %(to_date)s)
GROUP BY DATE(customerPayment.created);
```


Usage example

```python
from models import Order
from query_execfile import sql_execfile, raw_queryfile

result = sql_execfile('../datagrip/payment_transaction_stats.sql'),
    params={'from_date': .., 'to_date': ..},
    mapResultToDict=True,
    includeDescription=True
)
print result

rawQuerySet = raw_queryfile(Order, '../datagrip/order_rawquery.sql')
for order in rawQuerySet:
    doSomeThingWith(order)
```

**mapResultToDict=True** will map results to a dict with key = first comment above the query.
So you can write multiple query in a single file and execute these query at once.

**includeDescription=True** will add a extra row at first as column header using description from the query.
In this case is _AS created_ and _AS amount_exchanged_


**Result return of that example:**

```json
{"sum_customerPayment_amount_rate_exchanged_group_by_day": [
[
    "created",
    "amount_exchanged"
],
[
    "2016-03-01",
    4933000.0
],
[
    "2016-03-02",
    7144000.0
],
...
...
...
[
    "2016-03-10",
    2110000.0
]
],}
```


# Documentation & Support