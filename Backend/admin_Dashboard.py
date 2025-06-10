from flask import Blueprint, jsonify
from database import trainer_collection, nutritionist_collection, meeting_collection
from bson import ObjectId

admin_dashboard_bp = Blueprint("admin_dashboard", __name__)

@admin_dashboard_bp.route("/admin/dashboard", methods=["GET"])
def get_admin_dashboard():
    try:
        # 1. Fetch all trainers
        trainers = list(trainer_collection.find({}, {"_id": 1, "name": 1, "email": 1}))
        trainers_list = [
            {
                "_id": str(trainer["_id"]),
                "name": trainer["name"],
                "email": trainer["email"]
            }
            for trainer in trainers
        ]

        # 2. Fetch all nutritionists
        nutritionists = list(nutritionist_collection.find({}, {"_id": 1, "name": 1, "email": 1}))
        nutritionists_list = [
            {
                "_id": str(nutritionist["_id"]),
                "name": nutritionist["name"],
                "email": nutritionist["email"]
            }
            for nutritionist in nutritionists
        ]

        # 3. Fetch all meetings
        meetings = list(meeting_collection.find({}, {
            "_id": 1,
            "user_name": 1,
            "meet_link": 1,
            "time": 1,
            "date": 1,
            "nutritionist_name": 1
        }))
        meetings_list = [
            {
                "_id": str(meeting["_id"]),
                "user_name": meeting["user_name"],
                "meet_link": meeting["meet_link"],
                "time": meeting["time"],
                "date": meeting["date"],
                "nutritionist_name": meeting["nutritionist_name"]
            }
            for meeting in meetings
        ]

        return jsonify({
            "trainers": trainers_list,
            "nutritionists": nutritionists_list,
            "meetings": meetings_list
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
