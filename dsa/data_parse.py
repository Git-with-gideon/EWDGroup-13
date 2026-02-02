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
