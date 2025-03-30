-- Query 208
SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment
        FROM part, supplier, partsupp, nation, region
        WHERE p_partkey = ps_partkey AND s_suppkey = ps_suppkey AND p_size IN (8,2,14,12,5)
          AND p_type LIKE '%BRASS' AND s_nationkey = n_nationkey
          AND n_regionkey = r_regionkey AND r_name = 'EUROPE'
        ORDER BY s_acctbal DESC, n_name, s_name, p_partkey LIMIT 100;