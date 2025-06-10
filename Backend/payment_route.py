from flask import Blueprint, request, jsonify
from database import db,users_collection
from bson import ObjectId
from bson.json_util import dumps
import datetime


payment_bp = Blueprint("payment", __name__)
payments_collection = db["Payments"]

@payment_bp.route("/submit", methods=["POST"])
def submit_payment():
    data = request.json
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    screenshot_url = data.get("screenshot_url")
    timestamp = datetime.datetime.utcnow()

    if not name or not email or not screenshot_url:
        return jsonify({"message": "Missing required fields"}), 400

    payment_data = {
        "name": name,
        "email": email,
        "screenshot_url": screenshot_url,
        "status": "pending",
        "timestamp": timestamp
    }

    print(" Attempting to insert payment:", payment_data)
    result = payments_collection.insert_one(payment_data)
    print(" Inserted with ID:", result.inserted_id)

    return jsonify({"message": "Payment submitted successfully"}), 201

# Admin updates status
from bson import ObjectId

@payment_bp.route("/update_status/<payment_id>", methods=["POST"])
def update_payment_status(payment_id):
    data = request.json
    new_status = data.get("status")  # "confirmed" or "rejected"

    if new_status not in ["confirmed", "rejected"]:
        return jsonify({"message": "Invalid status"}), 400

    try:
        # Convert payment_id to ObjectId
        payment_id = ObjectId(payment_id)
    except Exception as e:
        return jsonify({"message": "Invalid payment ID"}), 400

    result = payments_collection.update_one(
        {"_id": payment_id},
        {"$set": {"status": new_status}}
    )

    if result.matched_count == 0:
        return jsonify({"message": "Payment not found"}), 404

    return jsonify({"message": f"Payment {new_status}"}), 200

@payment_bp.route("/status", methods=["GET"])
def get_payment_status():
    email = request.args.get("email")

    if not email:
        return jsonify({"error": "Email query parameter is required"}), 400

    payment = payments_collection.find_one({"email": email}, sort=[("timestamp", -1)])

    if not payment:
        return jsonify({"status": "not found"}), 404

    # Ensure the _id field is returned as a string for frontend compatibility
    payment["_id"] = str(payment["_id"])

    return jsonify(payment), 200  # Return the full payment dat


@payment_bp.route("/confirm_payment/<payment_id>", methods=["POST"])
def confirm_payment(payment_id):
    try:
        # Get the payment from the payments collection using the provided payment_id
        payment = payments_collection.find_one({"_id": ObjectId(payment_id)})

        if not payment:
            return jsonify({"message": "Payment not found"}), 404

        # Get the email of the user from the payment document
        email = payment["email"]
        if not email:
            return jsonify({"message": "Email not found in payment details"}), 400

        # Now update the user's is_premium status to True
        user = users_collection.find_one({"email": email})

        if not user:
            return jsonify({"message": "User not found"}), 404

        # Update the is_premium field in the users collection
        users_collection.update_one(
            {"email": email},
            {"$set": {"is_premium": True}}
        )

        # Update the payment status to 'confirmed'
        payments_collection.update_one(
            {"_id": ObjectId(payment_id)},
            {"$set": {"status": "confirmed"}}
        )

        return jsonify({"message": "Payment confirmed and user upgraded to premium"}), 200

    except Exception as e:
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500
