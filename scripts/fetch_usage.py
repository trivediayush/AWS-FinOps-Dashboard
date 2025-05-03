import boto3
import sqlite3
import configparser
import os

# Get base directory dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, '..', 'data', 'usage.db')
config_path = os.path.join(BASE_DIR, 'config.ini')

# Load config
config = configparser.ConfigParser()
config.read(config_path)

region = config['AWS']['region']
start = config['AWS']['start_date']
end = config['AWS']['end_date']

# Initialize AWS client
client = boto3.client('ce', region_name=region)

# Get cost usage data
response = client.get_cost_and_usage(
    TimePeriod={'Start': start, 'End': end},
    Granularity='DAILY',
    Metrics=['UnblendedCost'],
    GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
)

# Store in SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

for day in response['ResultsByTime']:
    date = day['TimePeriod']['Start']
    for group in day['Groups']:
        service = group['Keys'][0]
        amount = float(group['Metrics']['UnblendedCost']['Amount'])
        cursor.execute(
            "INSERT INTO cost_data (service, usage_date, amount) VALUES (?, ?, ?)",
            (service, date, amount)
        )

conn.commit()
conn.close()

print("Data fetched and stored successfully.")
