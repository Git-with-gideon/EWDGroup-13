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
