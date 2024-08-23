from kafka import KafkaConsumer, KafkaProducer
import json
import sqlite3
import os

# Kafka consumer setup
consumer = KafkaConsumer(
    'vulnerabilities',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Connect to SQLite database for saving preprocessed data
conn = sqlite3.connect('processed_data.db')
cursor = conn.cursor()

# Ensure the table exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS preprocessed_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT
    )
''')
conn.commit()

def preprocess(data):
    # Example preprocessing logic: Convert all text to lowercase
    if 'text' in data:
        data['text'] = data['text'].lower()
    return data

def save_to_db(data):
    cursor.execute('''
        INSERT INTO preprocessed_data (data)
        VALUES (?)
    ''', (json.dumps(data),))
    conn.commit()

# Print data from SQLite database (for verification)
def print_data_from_db():
    cursor.execute('SELECT * FROM preprocessed_data')
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Data: {json.loads(row[1])}")

# Consume, preprocess, and save preprocessed data
for message in consumer:
    raw_data = message.value
    preprocessed_data = preprocess(raw_data)
    save_to_db(preprocessed_data)
    print(f"Saved preprocessed message: {preprocessed_data}")

# Close the connection
conn.close()

# Call this function separately to view data if needed
print_data_from_db()
