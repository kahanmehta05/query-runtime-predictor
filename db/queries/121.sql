-- Query 121
SELECT
          c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment
        FROM customer, nation, region
        WHERE c_nationkey = n_nationkey AND n_regionkey = r_regionkey
          AND r_name = 'ASIA' AND c_acctbal > 3400
          AND c_mktsegment = 'FURNITURE'
        ORDER BY c_acctbal DESC LIMIT 20;