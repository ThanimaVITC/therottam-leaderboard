from pymongo import MongoClient
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_DB_URI')
if not MONGO_URI:
    print("Error: MONGO_DB_URI environment variable is not set")
    print("Please set it in .env file or export MONGO_DB_URI=your_mongodb_connection_string")
    exit(1)

DB_NAME = os.environ.get('DB_NAME', 'leaderboard')
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

hashed = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt())

existing_admin = db.admins.find_one({'username': ADMIN_USERNAME})
if existing_admin:
    db.admins.update_one(
        {'username': ADMIN_USERNAME},
        {'$set': {'password': hashed}}
    )
    print(f"Admin '{ADMIN_USERNAME}' password updated.")
else:
    db.admins.insert_one({
        'username': ADMIN_USERNAME,
        'password': hashed
    })
    print(f"Admin '{ADMIN_USERNAME}' created successfully.")

print(f"\nDatabase: {DB_NAME}")
print(f"Login credentials:")
print(f"  Username: {ADMIN_USERNAME}")
print(f"  Password: {ADMIN_PASSWORD}")
