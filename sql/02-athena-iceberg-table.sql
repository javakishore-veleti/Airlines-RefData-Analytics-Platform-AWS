-- Destination Apache Iceberg table (Athena DDL — not MySQL).
-- Replace amzn-s3-demo-bucket with your globally unique S3 bucket name.
-- Create the Glue database first (CLI): aws glue create-database --database-input '{"Name":"market_db"}'
-- Create the S3 prefix first (CLI): aws s3api put-object --bucket <bucket> --key market_db/market_rule/

CREATE TABLE market_db.market_rule (
    rule_id int,
    name string,
    weight int,
    status string,
    effective_from timestamp,
    market_from string,
    market_to string,
    created_at timestamp,
    updated_at timestamp
)
LOCATION 's3://amzn-s3-demo-bucket/market_db/market_rule/'
TBLPROPERTIES (
    'table_type' = 'ICEBERG',
    'format' = 'parquet'
);

-- Validation queries (after full-load / CDC):
-- SELECT * FROM market_db.market_rule;
-- SELECT * FROM market_db.market_rule WHERE name = 'SYD-MEL Easter Peak';

-- Optional table maintenance (production):
-- OPTIMIZE market_db.market_rule REWRITE DATA USING BIN_PACK;
-- VACUUM market_db.market_rule;
