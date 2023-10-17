# tracker:
--------
CREATE TABLE `e3escoles.ordino.tracker_registry` (
    file_name STRING NOT NULL,
    num_lines_csv INT64 NOT NULL,
    num_lines_clean INT64 NOT NULL,
    tmstmp TIMESTAMP NOT NULL
)
PARTITION BY DATE(tmstmp)
--------

# nationals:
--------
CREATE TABLE `tourism-361611.final2.nationals` (
    imsi STRING NOT NULL,
    zone STRING NOT NULL,
    tmstmp TIMESTAMP NOT NULL
)
PARTITION BY DATE(tmstmp)
CLUSTER BY zone;
--------