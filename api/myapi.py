from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

# Basic Authentication
USER_DATA = {
    "admin": generate_password_hash("admin@123")
}

@auth.verify_password
def verify_password(username, password):
    if username in USER_DATA and \
       check_password_hash(USER_DATA.get(username), password):
        return username
    return None

# Custom error handler for 401 Unauthorized
@auth.error_handler
def auth_error(status):
    return jsonify({
        "error": "401 Unauthorized",
        "message": "Invalid or missing credentials. Access denied."
    }), 401

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Philosophy@360',
    'database': 'momo_sms_db'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# 1. GET /transactions -> List all active transactions
@app.route('/transactions', methods=['GET'])
@auth.login_required
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # We only fetch records where is_deleted is FALSE
    cursor.execute("SELECT * FROM transactions WHERE is_deleted = FALSE")
    transactions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(transactions), 200

# 2. GET /transactions/{id} -> View one transaction
@app.route('/transactions/<int:t_id>', methods=['GET'])
@auth.login_required
def get_transaction(t_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM transactions WHERE transaction_id = %s AND is_deleted = FALSE", (t_id,))
    transaction = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if transaction:
        return jsonify(transaction), 200
    return jsonify({"error": "Transaction not found"}), 404
