-- Query 180
SELECT o_orderpriority, count(*) AS order_count
        FROM orders
        WHERE o_orderdate >= DATE '1998-10-02'
          AND o_orderdate < DATE '1998-12-31'
          AND EXISTS (SELECT * FROM lineitem WHERE l_orderkey = o_orderkey AND l_commitdate < l_receiptdate)
        GROUP BY o_orderpriority
        ORDER BY o_orderpriority;