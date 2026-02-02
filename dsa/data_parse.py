import xml.etree.ElementTree as ET
import json
import re
import mysql.connector
from datetime import datetime

# 1. Configuration & Constants
XML_FILE = 'modified_sms_v2.xml'
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Philosophy@360',
    'database': 'momo_sms_db'
}

def parse_sms_to_json(file_path):
    """Parses XML and returns a list of dictionaries (JSON objects)."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    transactions = []

    for sms in root.findall('sms'):
        body = sms.get('body', '')
        
        # Extract Transaction Reference
        ref_match = re.search(r'TxId:\s*(\d+)', body) or \
                    re.search(r'Financial Transaction Id:\s*(\d+)', body)
        ref = ref_match.group(1) if ref_match else "UNKNOWN"

        # Extract Amount (removing commas)
        amount_match = re.search(r'(\d{1,3}(?:,\d{3})|\d+)\sRWF', body)
        amount = float(amount_match.group(1).replace(',', '')) if amount_match else 0.0

        # Extract Fee
        fee_match = re.search(r'Fee was\s*(?::)?\s*(\d+)', body)
        fee = float(fee_match.group(1)) if fee_match else 0.0

        # Date formatting (converting XML date to SQL format)
        raw_date = sms.get('readable_date', '')
        try:
            # Format: "10 May 2024 4:30:58 PM" -> "2024-05-10 16:30:58"
            dt_obj = datetime.strptime(raw_date, '%d %b %y %I:%M:%S %p')
            formatted_date = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        except:
            formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Determine Category ID based on keywords
        category_id = 1  # Default to 'Incoming'
        if "payment of" in body.lower(): category_id = 4
        elif "transferred to" in body.lower(): category_id = 2
        elif "bank deposit" in body.lower(): category_id = 1
        elif "airtime" in body.lower(): category_id = 5

        transactions.append({
            "transaction_ref": ref,
            "category_id": category_id,
            "amount": amount,
            "fee": fee,
            "currency": "RWF",
            "transaction_date": formatted_date,
            "raw_sms": body
        })
    
    return transactions

def insert_into_db(transactions):
    """Connects to MySQL and inserts transaction data."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        sql = """
        INSERT INTO transactions 
        (transaction_ref, category_id, amount, fee, currency, transaction_date, raw_sms)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP
        """

        data_to_insert = [
            (t['transaction_ref'], t['category_id'], t['amount'], 
             t['fee'], t['currency'], t['transaction_date'], t['raw_sms'])
            for t in transactions if t['transaction_ref'] != "UNKNOWN"
        ]

        cursor.executemany(sql, data_to_insert)
        conn.commit()
        
        print(f"Successfully inserted/updated {cursor.rowcount} records.")
        
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
