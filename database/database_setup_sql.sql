-- ============================================
-- MoMo SMS Database Setup Script
-- Team: EWDGroup-13
-- ============================================

CREATE DATABASE IF NOT EXISTS momo_sms_db;
USE momo_sms_db;

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS system_logs;
DROP TABLE IF EXISTS transaction_tags;
DROP TABLE IF EXISTS user_transactions;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS transaction_categories;
DROP TABLE IF EXISTS users;

-- ============================================
-- TABLE: users
-- Stores people who send or receive money
-- ============================================

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    user_type ENUM('individual', 'business', 'agent') NOT NULL DEFAULT 'individual',
    current_balance DECIMAL(15,2) DEFAULT 0.00,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,

    CONSTRAINT chk_phone_format CHECK (phone_number REGEXP '^250[0-9]{9}$')
);

CREATE INDEX idx_users_phone ON users(phone_number);
CREATE INDEX idx_users_type ON users(user_type);

-- ============================================
-- TABLE: transaction_categories
-- The 9 types of MoMo transactions
-- ============================================

CREATE TABLE transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    category_code VARCHAR(20) NOT NULL UNIQUE,
    direction ENUM('inbound', 'outbound', 'internal') NOT NULL,
    description TEXT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);
