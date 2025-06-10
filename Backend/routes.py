import os
from flask import Blueprint, request, jsonify
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,JWTManager
from database import users_collection, admin_collection, trainer_collection,nutritionist_collection
from bson import ObjectId
from dotenv import load_dotenv
import datetime
from flask_jwt_extended import decode_token
from flask_mail import Mail, Message
load_dotenv()
from datetime import datetime
import datetime


mail = Mail()
auth_bp = Blueprint("auth", __name__)
def setup_jwt(app):
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    JWTManager(app)

@auth_bp.route("/register", methods=["POST"])
def register():
    print("Receive request.json" , request.json)
    data = request.json

    if not data:
        return jsonify({"message": "No JSON data received!"}), 400
    
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    print(f"name: {name}, email: {email}, password: {password}")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required!"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "Email already registered!"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "is_premium":False,
            "last_active":datetime.today().strftime("%Y-%m-%d"),
            "streak":0,
            "workout_count":0
        })
        print("Flask: User inserted successfully!")
        response = jsonify({"message": "User registered successfully!"}) 
        print("Flask: Response to send:", response.get_json()) 
        return response
    except Exception as e:
        print(f"Flask: Database error: {e}")
        return jsonify({"message": f"Database error: {e}"}), 500

# User Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and Password are required!"}), 400

    user = users_collection.find_one({"email": email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        access_token = create_access_token(identity=str(user["_id"]))
        return jsonify({"access_token":access_token }), 200
    else:
        return jsonify({"message": "Invalid email or password!"}), 401

# Admin Registration
@auth_bp.route("/admin/register", methods=["POST"])
def admin_register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required!"}), 400

    if admin_collection.find_one({"email": email}):
        return jsonify({"message": "Admin already registered!"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    admin_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "Admin registered successfully!"}), 201

# Admin Login
@auth_bp.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email , and Password are required!"}), 400

    admin = admin_collection.find_one({"email": email})
    if admin and bcrypt.checkpw(password.encode('utf-8'), admin["password"]):
        access_token = create_access_token(identity=str(admin["_id"]))
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid username , email or password!"}), 401

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(current_user_id)})
    if user:
        return jsonify({"message": f"Hello, {user['name']}!"}), 200
    else:
        return jsonify({"message": "User not found"}), 404
    

@auth_bp.route("/admin/details", methods=["GET"])
@jwt_required()
def get_admin_details():
    current_admin_id = get_jwt_identity()
    admin = admin_collection.find_one({"_id": ObjectId(current_admin_id)})

    if not admin:
        return jsonify({"message": "Admin not found"}), 404

    admin_data = {
        "id": str(admin["_id"]),
        "name": admin["name"],
        "email": admin["email"]
    }

    return jsonify(admin_data), 200

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required!"}), 400

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"message": "No user found with this email"}), 404

    reset_token = create_access_token(identity=str(user["_id"]), expires_delta=datetime.timedelta(minutes=15))

    try:
        msg = Message("Password Reset Token",
                      recipients=[email])
        msg.body = f"""
Hello {user.get('name', '')},

You requested a password reset. Use the following token in the app:

{reset_token}

This token is valid for 15 minutes. If you didn’t request a reset, please ignore this email.

Regards,
Your Team
"""
        mail.send(msg)
        return jsonify({"message": "Reset token sent to your email!"}), 200

    except Exception as e:
        print("Email send error:", e)
        return jsonify({"message": "Failed to send email"}), 500


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"message": "Token and new password are required"}), 400

    try:
        decoded_token = decode_token(token)
        user_id = decoded_token["sub"]

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hashed_password}}
        )

        if result.modified_count == 1:
            return jsonify({"message": "Password reset successful"}), 200
        else:
            return jsonify({"message": "Failed to reset password"}), 500

    except Exception as e:
        print(f"Token decoding error: {e}")
        return jsonify({"message": "Invalid or expired token"}), 400


@auth_bp.route("/admin/forgot-password", methods=["POST"])
def admin_forgot_password():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required!"}), 400

    admin = admin_collection.find_one({"email": email})
    if not admin:
        return jsonify({"message": "No admin found with this email"}), 404

    reset_token = create_access_token(identity=str(admin["_id"]), expires_delta=datetime.timedelta(minutes=15))

    try:
        msg = Message("Admin Password Reset Token", recipients=[email])
        msg.body = f"""
Hello {admin.get('name', '')},

You requested a password reset. Use the following token in the app:

{reset_token}

This token is valid for 15 minutes. If you didn’t request a reset, please ignore this email.

Regards,
Your Admin Team
"""
        mail.send(msg)
        return jsonify({"message": "Reset token sent to your email!"}), 200

    except Exception as e:
        print("Email send error:", e)
        return jsonify({"message": "Failed to send email"}), 500


@auth_bp.route("/admin/reset-password", methods=["POST"])
def reset_admin_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"message": "Token and new password are required"}), 400

    try:
        decoded_token = decode_token(token)
        admin_id = decoded_token["sub"]

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        result = admin_collection.update_one(
            {"_id": ObjectId(admin_id)},
            {"$set": {"password": hashed_password}}
        )

        if result.modified_count == 1:
            return jsonify({"message": "Password reset successful"}), 200
        else:
            return jsonify({"message": "Failed to reset password"}), 500

    except Exception as e:
        print(f"Token decoding error: {e}")
        return jsonify({"message": "Invalid or expired token"}), 400
    

@auth_bp.route("/trainer/forgot-password", methods=["POST"])
def trainer_forgot_password():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required!"}), 400

    trainer = trainer_collection.find_one({"email": email})
    if not trainer:
        return jsonify({"message": "No trainer found with this email"}), 404

    reset_token = create_access_token(identity=str(trainer["_id"]), expires_delta=datetime.timedelta(minutes=15))

    try:
        msg = Message("Trainer Password Reset Token", recipients=[email])
        msg.body = f"""
Hello {trainer.get('name', '')},

You requested a password reset. Use the following token in the app:

{reset_token}

This token is valid for 15 minutes. If you didn’t request a reset, please ignore this email.

Regards,
Your Admin Team
"""
        mail.send(msg)
        return jsonify({"message": "Reset token sent to your email!"}), 200

    except Exception as e:
        print("Email send error:", e)
        return jsonify({"message": "Failed to send email"}), 500


@auth_bp.route("/trainer/reset-password", methods=["POST"])
def reset_trainer_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"message": "Token and new password are required"}), 400

    try:
        decoded_token = decode_token(token)
        trainer_id = decoded_token["sub"]

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        result = trainer_collection.update_one(
            {"_id": ObjectId(trainer_id)},
            {"$set": {"password": hashed_password}}
        )

        if result.modified_count == 1:
            return jsonify({"message": "Password reset successful"}), 200
        else:
            return jsonify({"message": "Failed to reset password"}), 500

    except Exception as e:
        print(f"Token decoding error: {e}")
        return jsonify({"message": "Invalid or expired token"}), 400
    
@auth_bp.route("/nutritionist/forgot-password", methods=["POST"])
def nutritionist_forgot_password():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required!"}), 400

    nutritionist = nutritionist_collection.find_one({"email": email})
    if not nutritionist:
        return jsonify({"message": "No Nutritionist found with this email"}), 404

    reset_token = create_access_token(identity=str(nutritionist["_id"]), expires_delta=datetime.timedelta(minutes=15))

    try:
        msg = Message("Nutritionist Password Reset Token", recipients=[email])
        msg.body = f"""
Hello {nutritionist.get('name', '')},

You requested a password reset. Use the following token in the app:

{reset_token}

This token is valid for 15 minutes. If you didn’t request a reset, please ignore this email.

Regards,
Your Admin Team
"""
        mail.send(msg)
        return jsonify({"message": "Reset token sent to your email!"}), 200

    except Exception as e:
        print("Email send error:", e)
        return jsonify({"message": "Failed to send email"}), 500


@auth_bp.route("/nutritionist/reset-password", methods=["POST"])
def reset_nutritionist_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"message": "Token and new password are required"}), 400

    try:
        decoded_token = decode_token(token)
        nutritionist_id = decoded_token["sub"]

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        result = nutritionist_collection.update_one(
            {"_id": ObjectId(nutritionist_id)},
            {"$set": {"password": hashed_password}}
        )

        if result.modified_count == 1:
            return jsonify({"message": "Password reset successful"}), 200
        else:
            return jsonify({"message": "Failed to reset password"}), 500

    except Exception as e:
        print(f"Token decoding error: {e}")
        return jsonify({"message": "Invalid or expired token"}), 400