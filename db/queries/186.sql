-- Query 186
SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue
        FROM customer, orders, lineitem, supplier, nation, region
        WHERE c_custkey = o_custkey AND l_orderkey = o_orderkey AND l_suppkey = s_suppkey
          AND c_nationkey = s_nationkey AND s_nationkey = n_nationkey AND n_regionkey = r_regionkey
          AND r_name = 'AFRICA' AND o_orderdate >= DATE '1998-07-25'
          AND o_orderdate < DATE '1999-07-25'
        GROUP BY n_name ORDER BY revenue DESC;