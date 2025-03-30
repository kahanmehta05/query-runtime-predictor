-- Query 40
SELECT 
          l_returnflag, l_linestatus, 
          sum(l_quantity) AS sum_qty, 
          avg(l_extendedprice) AS avg_price, 
          avg(l_discount) AS avg_disc, 
          count(*) AS count_order
        FROM lineitem
        WHERE l_shipdate <= DATE '1998-10-13'
        GROUP BY l_returnflag, l_linestatus
        ORDER BY l_returnflag, l_linestatus;