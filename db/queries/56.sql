-- Query 56
SELECT
          c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment
        FROM customer, nation, region
        WHERE c_nationkey = n_nationkey AND n_regionkey = r_regionkey
          AND r_name = 'ASIA' AND c_acctbal > 2685
          AND c_mktsegment = 'AUTOMOBILE'
        ORDER BY c_acctbal DESC LIMIT 20;