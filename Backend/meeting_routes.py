from flask import Blueprint, jsonify, request
from database import users_collection, meeting_collection
from bson import ObjectId

meeting_bp = Blueprint("meeting", __name__)

# Fetch premium users
@meeting_bp.route("/get_premium_users", methods=["GET"])
def get_premium_users():
    """Fetch all premium users with names."""
    premium_users = users_collection.find({"is_premium": True}, {"_id": 1, "name": 1})
    
    return jsonify([{"user_id": str(user["_id"]), "name": user["name"]} for user in premium_users])


@meeting_bp.route("/schedule_meeting", methods=["POST"])
def schedule_meeting():
    """Save meeting schedules for multiple users with date, linked to a nutritionist."""
    data = request.json  
    if not data:
        return jsonify({"error": "No data provided"}), 400

    print("DEBUG: Received data:", data)  

    if isinstance(data, list):
        schedule_list = []
        
        for entry in data:
            if isinstance(entry, dict):  
                user_id = entry.get("user_id")
                user_name = entry.get("user_name")  
                meet_link = entry.get("meet_link")
                time = entry.get("time")
                date = entry.get("date")  
                nutritionist_id = entry.get("nutritionist_id") 
                nutritionist_name = entry.get("nutritionist_name")  

                if not all([user_id, meet_link, time, user_name, date, nutritionist_id, nutritionist_name]):
                    return jsonify({"error": "Missing fields in request"}), 400

                # Check if the user already has a scheduled meeting on the same date
                existing_meeting = meeting_collection.find_one({
                    "user_id": ObjectId(user_id),
                    "date": date
                })

                if existing_meeting:
                    return jsonify({"error": f"User {user_name} already has a scheduled meeting on {date}"}), 400

                # Append meeting to schedule list
                schedule_list.append({
                    "user_id": ObjectId(user_id),
                    "user_name": user_name,
                    "meet_link": meet_link,
                    "time": time,
                    "date": date,
                    "nutritionist_id": ObjectId(nutritionist_id),  # Store nutritionist ID
                    "nutritionist_name": nutritionist_name  # Store nutritionist name
                })
            else:
                return jsonify({"error": "Invalid data structure. Each entry must be a dictionary."}), 400

        # Insert all valid schedules
        if schedule_list:
            meeting_collection.insert_many(schedule_list)

        return jsonify({"message": "Meetings scheduled successfully!"}), 201
    else:
        return jsonify({"error": "Expected a list of meetings, but got something else."}), 400

@meeting_bp.route("/get_previous_meetings/<nutritionist_id>", methods=["GET"])
def get_previous_meetings(nutritionist_id):
    """Fetch all scheduled meetings for a specific nutritionist."""
    try:
        nutritionist_object_id = ObjectId(nutritionist_id)
    except Exception:
        return jsonify({"error": "Invalid nutritionist ID"}), 400

    # Fetch meetings only for the logged-in nutritionist
    meetings = meeting_collection.find(
        {"nutritionist_id": nutritionist_object_id},
        {"_id": 1, "user_name": 1, "meet_link": 1, "time": 1, "date": 1}
    )

    meeting_list = [
        {
            "_id": str(meeting["_id"]),
            "user_name": meeting["user_name"],  
            "meet_link": meeting["meet_link"],
            "time": meeting["time"],
            "date": meeting["date"]
        }
        for meeting in meetings
    ]

    return jsonify(meeting_list)
