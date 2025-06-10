from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import users_collection
from bson import ObjectId
from datetime import datetime, timedelta

member_bp = Blueprint("member", __name__)

@member_bp.route("/details", methods=["GET"])
@jwt_required()
def get_member_details():
    try:
        current_user_id = get_jwt_identity()
        print(f"DEBUG: Current user ID from JWT: {current_user_id}")
        user = users_collection.find_one({"_id": ObjectId(current_user_id)})

        if not user:
            return jsonify({"message": "User not found!"}), 404

        # Daily streak logic
        today = datetime.utcnow().date()
        last_active = user.get("last_active")
        streak = user.get("streak", 0)

        if last_active:
            last_active = datetime.strptime(last_active, "%Y-%m-%d").date()
            if last_active == today:
                pass  # Already updated today
            elif last_active == today - timedelta(days=1):
                streak += 1
            else:
                streak = 1
        else:
            streak = 1

        # Update if needed
        # users_collection.update_one(
        #     {"_id": ObjectId(current_user_id)},
        #     {"$set": {"streak": streak, "last_active": today.strftime("%Y-%m-%d")}}
        # )

        user_data = {
            "id": str(user["_id"]),
            "name": user.get("name"),
            "email": user.get("email"),
            "streak": user.get("streak"),
            "last_active":user.get("last_active"),
            "workout_count":user.get("workout_count")
        }
        return jsonify({"user": user_data}), 200

    except Exception as e:
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500

@member_bp.route("/complete_workout", methods=["POST"])
@jwt_required()
def complete_workout():
    try:
        current_user_id = get_jwt_identity()
        user = users_collection.find_one({"_id": ObjectId(current_user_id)})

        if not user:
            return jsonify({"message": "User not found!"}), 404

        # Get today's date
        today = datetime.utcnow().date()
        last_active = user.get("last_active")
        streak = user.get("streak", 0)

        # Handle streak logic
        if last_active:
            last_active = datetime.strptime(last_active, "%Y-%m-%d").date()
            if last_active == today:
                pass  # already updated
            elif last_active == today - timedelta(days=1):
                streak += 1
            else:
                streak = 1
        else:
            streak = 1

        # Increment workoutCount
        workout_count = user.get("workout_count", 0) + 1

        # Update user document
        users_collection.update_one(
            {"_id": ObjectId(current_user_id)},
            {
                "$set": {
                    "workout_count": workout_count,
                    "streak": streak,
                    "last_active": today.strftime("%Y-%m-%d")
                }
            }
        )

        return jsonify({
            "message": "Workout completed!",
            "workoutCount": workout_count,
            "streak": streak,
            "last_active": today.strftime("%Y-%m-%d")
        }), 200

    except Exception as e:
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500


