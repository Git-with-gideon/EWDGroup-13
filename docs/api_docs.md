# MoMo SMS Data Processing API Documentation

## Introduction

The MoMo SMS API provides a simple and direct access to MoMo (Mobile Money) transaction data. The API is built with Flask and uses **HTTP Basic Authentication**.

| Property | Value |
|----------|-------|
| **Base URL** | `http://localhost:5000` |
| **Content-Type** | `application/json` |
| **Authentication** | HTTP Basic Auth |

### Getting Started

1. Ensure MySQL is running with the `momo_sms_db` database configured (see [database/database_setup_sql.sql](../database/database_setup_sql.sql)).
2. Install dependencies: `flask`, `flask-httpauth`, `mysql-connector-python`, `werkzeug`
3. Run the API: `python api/myapi.py` (runs on port 5000 by default)
4. Default credentials: `admin` / `admin@123`

---

## Authentication

All endpoints require HTTP Basic Authentication. Include credentials in the `Authorization` header:

```
Authorization: Basic YWRtaW46YWRtaW5AMTIz
```

(Above is Base64 encoding of `admin:admin@123`)

---

## Endpoints

### 1. List All Transactions

**Endpoint & Method:** `GET /transactions`

**Description:** Returns all active (non-deleted) transactions.

**Parameters:** None

**Request Example:**

```bash
curl -X GET "http://localhost:5000/transactions" \
  -u admin:admin@123
```

**Response Example (200 OK):**

```json
[
  {
    "transaction_id": 1,
    "transaction_ref": "12345678901",
    "category_id": 4,
    "amount": 5000.0,
    "fee": 0.0,
    "currency": "RWF",
    "transaction_date": "2025-01-15 10:30:00",
    "raw_sms": "TxId:12345678901*Payment of 5,000 RWF to SHOP123*Balance:52,000 RWF",
    "status": "completed",
    "is_deleted": false,
    "created_at": "2025-01-15 10:30:00",
    "updated_at": "2025-01-15 10:30:00",
    "deleted_at": null
  }
]
```

**Error Codes:**

| Code | Condition | Response |
|------|-----------|----------|
| 401 | Missing or invalid credentials | `{"error": "401 Unauthorized", "message": "Invalid or missing credentials. Access denied."}` |

---

### 2. Get Single Transaction

**Endpoint & Method:** `GET /transactions/{id}`

**Description:** Returns a single transaction by ID. Only returns non-deleted transactions.

**Parameters:**

| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| id | integer | path | Yes | Transaction ID |

**Request Example:**

```bash
curl -X GET "http://localhost:5000/transactions/1" \
  -u admin:admin@123
```

**Response Example (200 OK):**

```json
{
  "transaction_id": 1,
  "transaction_ref": "12345678901",
  "category_id": 4,
  "amount": 5000.0,
  "fee": 0.0,
  "currency": "RWF",
  "transaction_date": "2025-01-15 10:30:00",
  "raw_sms": "TxId:12345678901*Payment of 5,000 RWF to SHOP123*Balance:52,000 RWF",
  "status": "completed",
  "is_deleted": false,
  "created_at": "2025-01-15 10:30:00",
  "updated_at": "2025-01-15 10:30:00",
  "deleted_at": null
}
```

**Error Codes:**

| Code | Condition | Response |
|------|-----------|----------|
| 401 | Missing or invalid credentials | `{"error": "401 Unauthorized", "message": "Invalid or missing credentials. Access denied."}` |
| 404 | Transaction not found or deleted | `{"error": "Transaction not found"}` |

---

### 3. Create Transaction

**Endpoint & Method:** `POST /transactions`

**Description:** Adds a new transaction.

**Parameters (JSON body):**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| transaction_ref | string | Yes | Unique transaction reference (e.g., SMS TxId) |
| category_id | integer | Yes | FK to `transaction_categories.category_id` |
| amount | number | Yes | Transaction amount (must be positive) |
| fee | number | No | Fee (default: 0.0) |
| transaction_date | string | No | Datetime in `YYYY-MM-DD HH:MM:SS` (default: current timestamp) |
| raw_sms | string | Yes | Raw SMS text content |

**Request Example:**

```bash
curl -X POST "http://localhost:5000/transactions" \
  -u admin:admin@123 \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_ref": "98765432100",
    "category_id": 4,
    "amount": 2500.0,
    "fee": 0.0,
    "transaction_date": "2025-02-02 12:00:00",
    "raw_sms": "TxId:98765432100*Payment of 2,500 RWF to MERCHANT456*Balance:10,000 RWF"
  }'
```

**Response Example (201 Created):**

```json
{
  "message": "Transaction created",
  "id": 15
}
```

**Error Codes:**

| Code | Condition | Response |
|------|-----------|----------|
| 401 | Missing or invalid credentials | `{"error": "401 Unauthorized", "message": "Invalid or missing credentials. Access denied."}` |
| 400 | Validation error, DB constraint violation, or missing required fields | `{"error": "<error message>"}` |

---

### 4. Update Transaction

**Endpoint & Method:** `PUT /transactions/{id}`

**Description:** Updates an existing transaction. Pass only the fields you want to update.

**Parameters:**

| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| id | integer | path | Yes | Transaction ID |

**Body (JSON):** Any subset of transaction fields, e.g. `amount`, `fee`, `transaction_date`, `raw_sms`, `category_id`, `status`.

**Request Example:**

```bash
curl -X PUT "http://localhost:5000/transactions/1" \
  -u admin:admin@123 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 6000.0,
    "raw_sms": "TxId:12345678901*Updated payment of 6,000 RWF*Balance:51,000 RWF"
  }'
```

**Response Example (200 OK):**

```json
{
  "message": "Transaction updated"
}
```

**Error Codes:**

| Code | Condition | Response |
|------|-----------|----------|
| 401 | Missing or invalid credentials | `{"error": "401 Unauthorized", "message": "Invalid or missing credentials. Access denied."}` |
| 400 | Empty body provided | `{"error": "No data provided"}` |
| 404 | Transaction not found | `{"error": "Transaction not found"}` |

---

### 5. Delete Transaction (Soft Delete)

**Endpoint & Method:** `DELETE /transactions/{id}`

**Description:** Soft-deletes a transaction by setting `is_deleted = TRUE` and `deleted_at = CURRENT_TIMESTAMP`. The record remains in the database but is excluded from `GET /transactions` results.

**Parameters:**

| Name | Type | Location | Required | Description |
|------|------|----------|----------|-------------|
| id | integer | path | Yes | Transaction ID |

**Request Example:**

```bash
curl -X DELETE "http://localhost:5000/transactions/1" \
  -u admin:admin@123
```

**Response Example (200 OK):**

```json
{
  "message": "Transaction deleted (soft delete)"
}
```

**Error Codes:**

| Code | Condition | Response |
|------|-----------|----------|
| 401 | Missing or invalid credentials | `{"error": "401 Unauthorized", "message": "Invalid or missing credentials. Access denied."}` |
| 404 | Transaction not found | `{"error": "Transaction not found"}` |

---

## Error Codes Summary

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST (new resource) |
| 400 | Bad Request | Validation error, missing/invalid data, DB constraint violation |
| 401 | Unauthorized | Missing or invalid HTTP Basic credentials |
| 404 | Not Found | Transaction ID does not exist or is soft-deleted |
| 500 | Internal Server Error | Unhandled server error (e.g., DB connection failure) |

---

## Common Error Response Format

Most error responses follow this structure:

```json
{
  "error": "Error type or message"
}
```

For 401 responses, an additional `message` field is included:

```json
{
  "error": "401 Unauthorized",
  "message": "Invalid or missing credentials. Access denied."
}
```

---

## Database Schema Reference

The `transactions` table structure (relevant to API responses):

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | INT | Primary key (auto-increment) |
| transaction_ref | VARCHAR(50) | Unique transaction reference |
| category_id | INT | FK to transaction_categories |
| amount | DECIMAL(15,2) | Transaction amount (must be > 0) |
| fee | DECIMAL(15,2) | Fee (default 0.00) |
| currency | VARCHAR(10) | Default: RWF |
| transaction_date | DATETIME | Transaction timestamp |
| raw_sms | TEXT | Raw SMS content |
| status | ENUM | pending, completed, failed, reversed |
| is_deleted | BOOLEAN | Soft delete flag |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update time |
| deleted_at | TIMESTAMP | Set when soft-deleted |
