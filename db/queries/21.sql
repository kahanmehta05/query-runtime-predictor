-- Modified TPC-H Query 21
SELECT
  s_name,
  COUNT(*) AS numwait
FROM
  supplier
JOIN
  lineitem l1 ON s_suppkey = l1.l_suppkey
WHERE
  EXISTS (
    SELECT *
    FROM lineitem l2
    WHERE
      l2.l_orderkey = l1.l_orderkey
      AND l2.l_suppkey <> l1.l_suppkey
  )
  AND NOT EXISTS (
    SELECT *
    FROM lineitem l3
    WHERE
      l3.l_orderkey = l1.l_orderkey
      AND l3.l_suppkey <> l1.l_suppkey
      AND l3.l_receiptdate > l3.l_commitdate
  )
GROUP BY
  s_name
ORDER BY
  numwait DESC, s_name
LIMIT 100;
