from flask import Flask
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import traceback 
from flask_cors import CORS
import base64
from database import db, trainer_collection, nutritionist_collection  # Import Database

# Create a Blueprint
auth_bp = Blueprint("auth", __name__)
auth_ca = Blueprint("create", __name__)
bcrypt = Bcrypt()

   
@auth_ca.route("/createaccount", methods=["POST"])
def register():
    try:

        if not request.is_json:
            return jsonify({"error": "Invalid request. JSON format expected."}), 400

        data = request.get_json()

        if not data:
            return jsonify({"error": "Empty request body."}), 400

        print("📩 Received Data:", data)  # Debugging

        # Fetch and Validate Role
        role = data.get("role", "").strip().lower()
        if role not in ["trainer", "nutritionist"]:
            return jsonify({"error": "Invalid role. Choose 'trainer' or 'nutritionist'."}), 400

        # Validate Required Fields
        required_fields = ["username", "email", "phone", "password", "age", "experience", "gender", "specialization", "degree", "location"]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Select Collection Based on Role
        collection = trainer_collection if role == "trainer" else nutritionist_collection

        # Check if Email Already Exists in Both Collections
        if trainer_collection.find_one({"email": data["email"]}) or nutritionist_collection.find_one({"email": data["email"]}):
            return jsonify({"error": "Email is already registered"}), 400

        #  Hash Password
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

        # Store Base64-encoded PDF (Ensure Valid Encoding)
        certification = data.get("certification", None)

        if certification:
            try:
                base64.b64decode(certification)  # Validate if it's a correct base64 string
            except Exception:
                return jsonify({"error": "Invalid PDF encoding"}), 400

        # Create User Data Object
        user = {
            "username": data["username"].strip(),
            "email": data["email"].strip(),
            "phone": data["phone"].strip(),
            "password": hashed_password,
            "age": int(data["age"]),
            "experience": int(data["experience"]),
            "gender": data["gender"].strip(),
            "specialization": data["specialization"].strip(),
            "degree": data["degree"].strip(),
            "location": data["location"].strip(),
            "role": role,
            "certification": certification,  #  Store PDF as Base64
            "created_at": datetime.datetime.utcnow()
        }

        # Insert into MongoDB
        user_id = collection.insert_one(user).inserted_id

        #  Generate JWT Token
        access_token = create_access_token(identity={"id": str(user_id), "role": role})

        print("Account Created Successfully:", user)  #  Debugging
        return jsonify({"message": f"{role.capitalize()} registered successfully", "token": access_token}), 201

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

@auth_ca.route("/trainerlogin" , methods = ["POST"])
def login_trainer():
    try:
        print("Flask: /trainerlogin called") 
        if not request.is_json:
            print("Flask: Invalid request - Not JSON")
            return jsonify({"error" : "Invalid request here JSON format expected "}) ,400

        data = request.get_json()
        email = data.get("email")
        password = data.get("password")


        print(f"Flask: Email received: {email}")
        print(f"Flask: Password received: {password}")


        if not email or not password:
            print("Flask: Missing email or password")
            return jsonify({"error" : "Email and password are required"}) , 400

        trainer = trainer_collection.find_one({"email" : email})

        
        if not trainer:
            print(f"Flask: User not found for email: {email}")
            return jsonify({"error" : "Invalid email or password"}) , 401
        
        print(f"Flask: Trainer from DB: {trainer}")
    
        if not bcrypt.check_password_hash(trainer["password"] , password) :
            print(f"password failed")
            return jsonify({"error" : "Invalid email or password"}) , 401
    
        role = trainer["role"]
        print(f"User role: {role}")

        print(f"Flask: User data: {trainer}")


        access_token = create_access_token(identity=str(trainer["_id"]))
        print(f"Generated access token: {access_token}")

        return jsonify({"access-token" : access_token , "role" : role}) , 200
    
    except Exception as e:
        print(f"Flask: !!!!! ERROR !!!!!: {e}")
        traceback.print_exc()  
        return jsonify({"error": "Internal Server Error"}), 500


@auth_ca.route("/nutritionistlogin", methods=["POST"])
def login_nutritionist():
    try:
        print("Flask: /nutritionistlogin called")
        if not request.is_json:
            print("Flask: Invalid request - Not JSON")
            return jsonify({"error": "Invalid request here JSON format expected"}), 400

        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        print(f"Flask: Email received: {email}")
        print(f"Flask: Password received: {password}")

        if not email or not password:
            print("Flask: Missing email or password")
            return jsonify({"error": "Email and password are required"}), 400

        nutritionist = nutritionist_collection.find_one({"email": email})

        if not nutritionist:
            print(f"Flask: Nutritionist not found for email: {email}")
            return jsonify({"error": "Invalid email or password"}), 401

        if not bcrypt.check_password_hash(nutritionist["password"], password):
            print(f"password failed")
            return jsonify({"error": "Invalid email or password"}), 401

        role = nutritionist["role"]  
        print(f"User role: {role}")

        print(f"Flask: User data: {nutritionist}")
        
        access_token = create_access_token(identity=str(nutritionist["_id"]))

        print(f"Generated access token: {access_token}")

        return jsonify({"access-token": access_token, "role": role}), 200

    except Exception as e:
        print(f"Flask: !!!!! ERROR !!!!!: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    