from flask import Blueprint, request, jsonify
from bson import ObjectId
from database import meeting_collection, meeting_nutritionist_collection,users_collection



meetingu_bp = Blueprint('meetingu', __name__)

@meetingu_bp.route('/meetings', methods=['GET'])
def get_user_meetings():
    try:
        # Get user ID from query param or auth token
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400

        object_user_id = ObjectId(user_id)

        # Fetch trainer meetings
        trainer_meetings = list(meeting_collection.find({"user_id": object_user_id}))


        for meeting in trainer_meetings:
            meeting["_id"] = str(meeting["_id"])
            meeting["user_id"] = str(meeting["user_id"])
            meeting["trainer_id"] = str(meeting["trainer_id"])

        #  Fetch nutritionist meetings
        nutritionist_meetings = list(meeting_nutritionist_collection.find({"user_id": object_user_id}))
        for meeting in nutritionist_meetings:
            meeting["_id"] = str(meeting["_id"])
            meeting["user_id"] = str(meeting["user_id"])
            meeting["nutritionist_id"] = str(meeting["nutritionist_id"])

        return jsonify({
            "trainer_meetings": trainer_meetings,
            "nutritionist_meetings": nutritionist_meetings
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
