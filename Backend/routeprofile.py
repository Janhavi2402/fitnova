from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, decode_token
from database import trainer_collection, nutritionist_collection
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
import traceback

trainerprofile_bp = Blueprint("trainerprofile", __name__)
bcrypt = Bcrypt()

@trainerprofile_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    try:
        current_user = get_jwt_identity()
        print(f"Current user : {current_user}")
        token = get_jwt()
        print(f"JWT Token: {token}")

        raw_token = request.headers.get("Authorization").split("Bearer ")[1]
        print(f"Raw Token: {raw_token}")

        decoded_token = decode_token(encoded_token=raw_token)
        print(f"Decoded Token: {decoded_token}")
        
        if isinstance(current_user, dict):
            user_id = current_user.get("id")
            user_role = current_user.get("role")
        else:
            user_id = current_user
            user_role = "trainer"

        print(f"fetch profile for user ID : {user_id} , Role: {user_role}")

        collection = (
            trainer_collection if user_role == "trainer" else nutritionist_collection
        )

        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            user.pop("password", None)

            # Corrected: Return JSON instead of HTML
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        print(f"Error in get_profile: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
    
@trainerprofile_bp.route("/editprofile", methods=["PUT"])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()

    if isinstance(current_user, dict):
        user_id = current_user.get("id")
        user_role = current_user.get("role")
    else:
        user_id = current_user
        user_role = "trainer"

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format. Expected JSON object."}), 400

    collection = (
        trainer_collection if user_role == "trainer" else nutritionist_collection
    )

    if "password" in data:
        data["password"] = bcrypt.generate_password_hash(
            data["password"]
        ).decode("utf-8")

    update_data = {k: v for k, v in data.items() if k != "_id"}

    result = collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": update_data}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Profile updated successfully"}), 200
    else:
        return jsonify(
            {"error": "Profile update failed or no changes made"}
        ), 400