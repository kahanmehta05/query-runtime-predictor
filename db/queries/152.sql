-- Query 152
SELECT o_orderpriority, count(*) AS order_count
        FROM orders
        WHERE o_orderdate >= DATE '1998-06-19'
          AND o_orderdate < DATE '1998-09-17'
          AND EXISTS (SELECT * FROM lineitem WHERE l_orderkey = o_orderkey AND l_commitdate < l_receiptdate)
        GROUP BY o_orderpriority
        ORDER BY o_orderpriority;