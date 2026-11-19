-- Source Aurora MySQL setup for airlines reference-data CDC.
-- Run against the Aurora MySQL writer as an admin (or least-privilege) user.
-- Blog walkthrough tested on Aurora MySQL 3.08.0 (MySQL 8.0 compatible).

-- After associating a custom cluster parameter group with:
--   binlog_format = ROW
--   binlog_row_image = FULL
--   binlog_checksum = NONE
-- reboot the writer, then set retention and verify:

CALL mysql.rds_set_configuration('binlog retention hours', 24);

SHOW VARIABLES WHERE Variable_name IN
('log_bin', 'binlog_format', 'binlog_row_image', 'binlog_checksum');
-- Expect: log_bin=ON, binlog_format=ROW, binlog_row_image=FULL, binlog_checksum=NONE

CREATE DATABASE IF NOT EXISTS market_db;
USE market_db;

CREATE TABLE IF NOT EXISTS market_rule (
    rule_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    weight INT NOT NULL DEFAULT 0,
    status VARCHAR(10) NOT NULL DEFAULT 'DRAFT',
    effective_from DATETIME(6) NOT NULL,
    market_from VARCHAR(30) NOT NULL,
    market_to VARCHAR(30) NOT NULL,
    created_at DATETIME(6),
    updated_at DATETIME(6)
);

-- Seed rows so full-load has data to replicate
INSERT INTO market_rule
(name, weight, status, effective_from, market_from, market_to, created_at, updated_at)
VALUES
('ORD-SFO Base', 10, 'ACTIVE', NOW(), 'ORD', 'SFO', NOW(), NOW()),
('LAX-JFK Peak', 50, 'ACTIVE', NOW(), 'LAX', 'JFK', NOW(), NOW());

-- Optional CDC smoke-test insert (run after the pipeline is Running):
-- INSERT INTO market_rule
-- (name, weight, status, effective_from, market_from, market_to, created_at, updated_at)
-- VALUES
-- ('SYD-MEL Easter Peak', 100, 'ACTIVE', NOW(), 'SYD', 'MEL', NOW(), NOW());

-- Optional UPDATE / DELETE validation:
-- UPDATE market_rule SET weight = 120 WHERE rule_id = 3;
-- DELETE FROM market_rule WHERE rule_id = 1;
