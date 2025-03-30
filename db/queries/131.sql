-- Query 131
SELECT o_orderpriority, count(*) AS order_count
        FROM orders
        WHERE o_orderdate >= DATE '1998-08-24'
          AND o_orderdate < DATE '1998-11-22'
          AND EXISTS (SELECT * FROM lineitem WHERE l_orderkey = o_orderkey AND l_commitdate < l_receiptdate)
        GROUP BY o_orderpriority
        ORDER BY o_orderpriority;