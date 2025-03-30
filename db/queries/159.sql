-- Query 159
SELECT
          c_custkey, c_name, c_acctbal, n_name, c_address, c_phone, c_comment
        FROM customer, nation, region
        WHERE c_nationkey = n_nationkey AND n_regionkey = r_regionkey
          AND r_name = 'AMERICA' AND c_acctbal > 2031
          AND c_mktsegment = 'HOUSEHOLD'
        ORDER BY c_acctbal DESC LIMIT 20;