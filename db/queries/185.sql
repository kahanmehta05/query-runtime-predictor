-- Query 185
SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority
        FROM customer, orders, lineitem
        WHERE c_mktsegment = 'MACHINERY' AND c_custkey = o_custkey AND l_orderkey = o_orderkey
          AND o_orderdate < DATE '1998-09-22'
          AND l_shipdate > DATE '1998-09-22'
        GROUP BY l_orderkey, o_orderdate, o_shippriority
        ORDER BY revenue DESC, o_orderdate LIMIT 10;