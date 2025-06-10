from flask import Blueprint, request, jsonify
from database import db 

review_bp = Blueprint("review", __name__)


reviews_collection = db["Reviews"] 

# Submit a Review
@review_bp.route("/submit", methods=["POST"])
def submit_review():
    data = request.json
    print("Received Data:", data) 
    review_text = data.get("review", "").strip()
    rating = data.get("rating")  # Get the rating from request

    if not review_text:
        return jsonify({"message": "Review cannot be empty!"}), 400
    
    if rating is None or not isinstance(rating, int) or not (1 <= rating <= 5):  # Validate rating
        return jsonify({"message": "Invalid rating! Please select a rating between 1 and 5."}), 400

    review_data = {"review": review_text, "rating": rating}
    reviews_collection.insert_one(review_data)

    return jsonify({"message": "Review submitted successfully!"}), 201

@review_bp.route("/all", methods=["GET"])
def get_reviews():
    reviews = list(reviews_collection.find({}, {"_id": 0}))  # Fetch all reviews without _id

    #  Ensure each review has "rating" and "review"
    for r in reviews:
        if "rating" not in r:
            r["rating"] = "N/A"  # Default rating
        if "review" not in r:
            r["review"] = "No review provided"

    return jsonify(reviews), 200


