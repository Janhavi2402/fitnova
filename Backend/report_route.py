from unittest import result
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import user_Report
from bson import ObjectId

report_bp = Blueprint("report", __name__)
@report_bp.route("/generate_report", methods=["POST"])
def generate_report():
    try:
        data = request.get_json()
        print("Received Data:", data) 

        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400
        
        required_keys = ["name", "age", "weight", "height", "goal", "fitness_level","email"]
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return jsonify({"success": False, "message": f"Missing keys: {missing_keys}"}), 400
       
        weight = float(data["weight"])
        height = float(data["height"]) / 100 
        bmi = round(weight / (height ** 2), 2)

        goal = data.get("goal","N/A")
        fitness_level = data.get("fitness_level","N/A")

        recommended_exercises = ""
        if bmi < 18.5:
            recommended_exercises = "Strength training, resistance exercises, and a high-calorie diet."
        elif 18.5 <= bmi < 24.9:
            recommended_exercises = "Balanced mix of strength training, cardio, and flexibility exercises."
        elif 25 <= bmi < 29.9:
            recommended_exercises = "Cardio exercises like running, cycling, and strength training."
        else:
            recommended_exercises = "Low-impact workouts like swimming, yoga, and walking."

        if goal == "Gain Muscle":
            recommended_exercises += " Focus on weight training and protein-rich diet."
        elif goal == "Lose Weight":
            recommended_exercises += " Increase cardio sessions and maintain a calorie deficit."

        report = {
            "name": data["name"],
            "email": data["email"],
            "age": data["age"],
            "weight": weight,
            "height": height * 100,  
            "bmi": bmi,
            "goal": goal,
            "fitness_level": fitness_level,
            "recommended_exercises": recommended_exercises
        }

        # Save report to MongoDB
        result=user_Report.insert_one(report)
        
        inserted_id = str(result.inserted_id)  # Convert ObjectId to string
        print("Inserted ID:", result.inserted_id)  # Debugging print
        report["_id"] = inserted_id
        return jsonify({"success": True, "message": "Report generated", "report": report}), 201

    except Exception as e:
        print("Error:", str(e))  # Debugging print
        return jsonify({"success": False, "message": str(e)}), 400


@report_bp.route("/get_report", methods=["POST"])
def get_report():
    try:
        data = request.get_json()
        email = data.get("email")
        print("Received data for fetching report:", data)

        if not data or "email" not in data:
            return jsonify({"success": False, "message": "Missing 'email' in request"}), 400

      

        # Fetch the latest report for the given name (you can add sorting if needed)
        report = user_Report.find_one({"email":email}, sort=[('_id', -1)])

        if not report:
            return jsonify({"success": False, "message": "No report found for this user"}), 404

        # Convert ObjectId to string for JSON serialization
        report["_id"] = str(report["_id"])

        return jsonify({"success": True, "report": report}), 200

    except Exception as e:
        print("Error fetching report:", str(e))
        return jsonify({"success": False, "message": str(e)}), 500
