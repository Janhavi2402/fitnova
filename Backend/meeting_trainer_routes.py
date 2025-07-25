from flask import Blueprint, jsonify, request
from database import users_collection, meeting_collection
from bson import ObjectId

meetingt_bp = Blueprint("meeting", __name__)

# Fetch premium users for dropdown
@meetingt_bp.route("/get_premium_users", methods=["GET"])
def get_premium_users():
    """Fetch all premium users with names."""
    premium_users = users_collection.find({"is_premium": True}, {"_id": 1, "name": 1})
    
    return jsonify([{"user_id": str(user["_id"]), "name": user["name"]} for user in premium_users])

# Route to schedule a meeting for a single user
@meetingt_bp.route("/schedule_meeting", methods=["POST"])
def schedule_meeting():
    """Save a single meeting schedule for a user, linked to a nutritionist."""
    data = request.json  

    if not isinstance(data, dict): 
        return jsonify({"error": "Invalid data format. Expected a JSON object."}), 400

    user_id = data.get("user_id")
    user_name = data.get("user_name")
    meet_link = data.get("meet_link")
    time = data.get("time")
    date = data.get("date")
    trainer_id = data.get("trainer_id")
    trainer_name = data.get("trainer_name")

    if not all([user_id, meet_link, time, user_name, date, trainer_id, trainer_name]):
        return jsonify({"error": "Missing fields in request"}), 400

    # Check if the user already has a scheduled meeting on the same date
    existing_meeting = meeting_collection.find_one({
        "user_id": ObjectId(user_id),
        "date": date
    })

    if existing_meeting:
        return jsonify({"error": f"User {user_name} already has a scheduled meeting on {date}"}), 400

    # Insert the meeting into the collection
    meeting_data = {
        "user_id": ObjectId(user_id),
        "user_name": user_name,
        "meet_link": meet_link,
        "time": time,
        "date": date,
        "trainer_id": ObjectId(trainer_id),
        "trainer_name": trainer_name
    }
    
    meeting_collection.insert_one(meeting_data)

    return jsonify({"message": "Meeting scheduled successfully!"}), 201


@meetingt_bp.route("/get_previous_meetings/<trainer_id>", methods=["GET"])
def get_previous_meetings(trainer_id):
    """Fetch all scheduled meetings for a specific nutritionist."""
    try:
        trainer_object_id = ObjectId(trainer_id)
    except Exception:
        return jsonify({"error": "Invalid nutritionist ID"}), 400

    # Fetch meetings only for the logged-in nutritionist
    meetings = meeting_collection.find(
        {"trainer_id": trainer_object_id},
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
