import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath('..data/usage.db'))
db_path = os.path.join(BASE_DIR, '..', 'data', 'usage.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS cost_data (
    service TEXT,
    usage_date TEXT,
    amount REAL
)
''')

conn.commit()
conn.close()

conn.close()
