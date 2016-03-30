# django-query-execfile
**Django module for execute sql query in a file**

[![pypi-version]][pypi]

Full documentation for the project is available at []

---

**Note**:


---

# Overview

django-query-execfile is a simple library for execute .sql query file.
Espesialy


# Requirements

* Python (2.7.x )
* Django (1.5+ )

# Installation

Install using `pip`...

    pip install django-query-execfile


# Usage & Example

This is content of a .sql file

    #sum_customerPayment_amount_rate_exchanged_group_by_day
    SELECT
      DATE(customerPayment.created)                       AS created,
      SUM(transaction.amount * transaction.exchange_rate) AS amount_exchanged
    FROM shop_module_customerpayment customerPayment
      LEFT JOIN shop_module_transaction transaction ON transaction.id = customerPayment.transaction_id
    WHERE (customerPayment.created BETWEEN %(from_date)s AND %(to_date)s)
    GROUP BY DATE(customerPayment.created);


Usage example

    from query_execfile import sql_execfile

    sql_execfile(cursor,
        '../datagrip/payment_transaction_stats.sql'),
        {'from_date': .., 'to_date': ..},
        mapResultToDict=True,
        includeDescription=True
    )

**mapResultToDict=True** will map results to a dict with key = first comment above the query.
So you can write multiple query in a single file and execute these query at once.

**includeDescription=True** will add a extra row at first as column header using description from the query.
In this case is _AS created_ and _AS amount_exchanged_


**Result return of that example:**

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


# Documentation & Support


