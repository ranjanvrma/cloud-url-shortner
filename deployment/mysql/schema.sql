-- Run once on VM3 as an admin user (e.g. mysql -u root -p < schema.sql)
-- Creates the database, an application user scoped to it, and the initial schema.
-- Flask-Migrate (backend/migrations) is the source of truth going forward;
-- this file documents the schema and can bootstrap a fresh VM3 quickly.

CREATE DATABASE IF NOT EXISTS url_shortener
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Replace 'change-this-password' and match backend/.env DB_PASSWORD.
-- '%' allows connections from VM2's private IP; restrict further via
-- security group / firewall rules rather than relaxing this grant.
CREATE USER IF NOT EXISTS 'url_shortener_app'@'%' IDENTIFIED BY 'change-this-password';
GRANT SELECT, INSERT, UPDATE, DELETE ON url_shortener.* TO 'url_shortener_app'@'%';
FLUSH PRIVILEGES;

USE url_shortener;

CREATE TABLE IF NOT EXISTS urls (
  id INT AUTO_INCREMENT PRIMARY KEY,
  short_code VARCHAR(16) NOT NULL,
  original_url VARCHAR(2048) NOT NULL,
  original_url_hash CHAR(64) NOT NULL,
  total_clicks INT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL,
  last_accessed_at DATETIME NULL,
  UNIQUE KEY ix_urls_short_code (short_code),
  UNIQUE KEY ix_urls_original_url_hash (original_url_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS clicks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  url_id INT NOT NULL,
  ip_address VARCHAR(45) NULL,
  user_agent VARCHAR(256) NULL,
  accessed_at DATETIME NOT NULL,
  INDEX ix_clicks_url_id (url_id),
  INDEX ix_clicks_accessed_at (accessed_at),
  CONSTRAINT fk_clicks_url_id FOREIGN KEY (url_id) REFERENCES urls(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
