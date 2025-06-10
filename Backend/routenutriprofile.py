from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity , get_jwt , decode_token
from database import trainer_collection, nutritionist_collection
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
import traceback

nutriprofile_bp = Blueprint("nutritionistprofile", __name__)
bcrypt = Bcrypt()

@nutriprofile_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_nutritionist_profile():
    try:
        current_user = get_jwt_identity()
        print(f"Current user: {current_user}")
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
            user_role = "nutritionist"

        print(f"fetch profile for user ID: {user_id}, Role: {user_role}")

        collection = (
            nutritionist_collection if user_role == "nutritionist" else trainer_collection
        )

        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            user.pop("password", None)

            return jsonify(user), 200
        else:
            return jsonify({"error": "Nutritionist not found"}), 404

    except Exception as e:
        print(f"Error in get_nutritionist_profile: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@nutriprofile_bp.route("/editprofile", methods=["PUT"])
@jwt_required()
def update_nutritionist_profile():
    try:
        current_user = get_jwt_identity()

        if isinstance(current_user, dict):
            user_id = current_user.get("id")
            user_role = current_user.get("role")
        else:
            user_id = current_user
            user_role = "nutritionist"

        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid data format. Expected JSON object."}), 400

        collection = (
            nutritionist_collection if user_role == "nutritionist" else trainer_collection
        )

        if "password" in data:
            data["password"] = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

        update_data = {k: v for k, v in data.items() if k != "_id"}

        result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

        if result.modified_count > 0:
            return jsonify({"message": "Nutritionist profile updated successfully"}), 200
        else:
            return jsonify({"error": "Nutritionist profile update failed or no changes made"}), 400

    except Exception as e:
        print(f"Error in update_nutritionist_profile: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500