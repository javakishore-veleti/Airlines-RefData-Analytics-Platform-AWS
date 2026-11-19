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
    updated_at DATETIME(6),
    KEY idx_market_rule_status (status),
    KEY idx_market_rule_markets (market_from, market_to)
);
