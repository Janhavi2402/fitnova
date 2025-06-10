from pymongo import MongoClient


MONGO_URI = ""


client = MongoClient(MONGO_URI)
db = client["Fitnova"]  
users_collection = db["User"] 
trainer_collection = db["Trainer"]
nutritionist_collection = db["Nutritionist"]
admin_collection = db["Admin"]
member_Dashboard = db["MemberDashboard"]
meeting_collection = db["meeting"]
meeting_nutritionist_collection = db["meeting_nutritionist"]
user_Report = db["userReport"]

print("Connected to MongoDB Atlas successfully!")
