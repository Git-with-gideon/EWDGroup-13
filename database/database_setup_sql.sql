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


-- ============================================
-- TABLE: transactions
-- Main table for all MoMo transactions
-- ============================================

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_ref VARCHAR(50) NOT NULL UNIQUE,
    category_id INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    fee DECIMAL(15,2) DEFAULT 0.00,
    transaction_date DATETIME NOT NULL,
    raw_sms TEXT NULL,
    status ENUM('pending', 'completed', 'failed', 'reversed') NOT NULL DEFAULT 'completed',
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,

    CONSTRAINT chk_amount_positive CHECK (amount > 0),
    CONSTRAINT chk_fee_valid CHECK (fee >= 0),

    FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id)
);

CREATE INDEX idx_trans_date ON transactions(transaction_date);
CREATE INDEX idx_trans_category ON transactions(category_id);
CREATE INDEX idx_trans_status ON transactions(status);

-- ============================================
-- TABLE: user_transactions (Junction Table)
-- Links users to transactions with their role
-- ============================================

CREATE TABLE user_transactions (
    user_transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    transaction_id INT NOT NULL,
    role ENUM('sender', 'receiver') NOT NULL,
    balance_snapshot DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY unique_user_transaction (user_id, transaction_id),

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE
);

CREATE INDEX idx_user_trans_user ON user_transactions(user_id);
CREATE INDEX idx_user_trans_trans ON user_transactions(transaction_id);

-- ============================================
-- TABLE: tags
-- Labels for transactions
-
