-- ARFD operational database (CDC-ready). Applied on first MySQL container boot
-- and by docker-all-up against a reused MySQL instance.

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

CREATE USER IF NOT EXISTS 'arfd'@'%' IDENTIFIED BY 'arfd';
GRANT ALL PRIVILEGES ON market_db.* TO 'arfd'@'%';
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'arfd'@'%';
FLUSH PRIVILEGES;
