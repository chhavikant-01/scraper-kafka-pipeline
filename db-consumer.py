from kafka import KafkaConsumer
from pymongo import MongoClient
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Kafka consumer setup
consumer = KafkaConsumer(
    'vulnerabilities',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# MongoDB Atlas setup
mongo_uri = os.getenv('MONGO_URI')
try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # 5 seconds timeout
    # Test the connection by getting server information
    client.admin.command('ping')
    print("Database connected successfully.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

db = client['scraper_database']
collection = db['nciipc_vulnerabilities']
collection.insert_one({'test': 'test'})  # Create collection if not exists

# Consume messages from Kafka and store in MongoDB
for message in consumer:
    collection.insert_one(message.value)
    print(f"Saved message: {message.value}")
