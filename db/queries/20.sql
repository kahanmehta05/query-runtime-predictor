WITH forest_parts AS (
  SELECT p_partkey
  FROM part
  WHERE p_name LIKE 'forest%'
),
lineitem_summary AS (
  SELECT
    l_partkey,
    l_suppkey,
    SUM(l_quantity) AS total_quantity
  FROM lineitem
  WHERE l_shipdate >= DATE '1994-01-01'
    AND l_shipdate < DATE '1995-01-01'
  GROUP BY l_partkey, l_suppkey
)
SELECT
  s_name,
  s_address
FROM
  supplier
JOIN nation ON s_nationkey = n_nationkey
JOIN partsupp ON s_suppkey = ps_suppkey
JOIN forest_parts ON ps_partkey = forest_parts.p_partkey
JOIN lineitem_summary ON
  lineitem_summary.l_partkey = ps_partkey AND
  lineitem_summary.l_suppkey = ps_suppkey
WHERE
  ps_availqty > 0.5 * lineitem_summary.total_quantity
  AND n_name = 'CANADA'
ORDER BY
  s_name;

