\COPY region FROM '/Users/darshmehta/tpch-dbgen/region.tbl' WITH (FORMAT text, DELIMITER '|');
\COPY nation FROM '/Users/darshmehta/tpch-dbgen/nation.tbl' WITH (FORMAT text, DELIMITER '|');
\COPY customer FROM '/Users/darshmehta/tpch-dbgen/customer.tbl' WITH (FORMAT text, DELIMITER '|');
\COPY orders FROM '/Users/darshmehta/tpch-dbgen/orders.tbl' WITH (FORMAT text, DELIMITER '|');
\COPY lineitem FROM '/Users/darshmehta/tpch-dbgen/lineitem.tbl' WITH (FORMAT text, DELIMITER '|');
\COPY part FROM '/Users/darshmehta/tpch-dbgen/part.tbl' WITH (FORMAT text, DELIMITER '|');
\COPY supplier FROM '/Users/darshmehta/tpch-dbgen/supplier.tbl' WITH (FORMAT text, DELIMITER '|');
\COPY partsupp FROM '/Users/darshmehta/tpch-dbgen/partsupp.tbl' WITH (FORMAT text, DELIMITER '|');
