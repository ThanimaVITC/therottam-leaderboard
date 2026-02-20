from pymongo import MongoClient
import os
import bcrypt

MONGO_URI = os.environ.get('MONGO_DB_URI', 'mongodb://localhost:27017/leaderboard')
client = MongoClient(MONGO_URI)
db = client.get_database()

admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')

hashed = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

existing_admin = db.admins.find_one({'username': admin_username})
if existing_admin:
    db.admins.update_one(
        {'username': admin_username},
        {'$set': {'password': hashed}}
    )
    print(f"Admin '{admin_username}' password updated.")
else:
    db.admins.insert_one({
        'username': admin_username,
        'password': hashed
    })
    print(f"Admin '{admin_username}' created successfully.")

print(f"\nLogin credentials:")
print(f"  Username: {admin_username}")
print(f"  Password: {admin_password}")
