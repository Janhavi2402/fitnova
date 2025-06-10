import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes import auth_bp ,setup_jwt
from dotenv import load_dotenv
from route1 import auth_ca
from memberroute import member_bp
from meeting_routes import meeting_bp
from review_routes import review_bp
from report_route import report_bp
from routeprofile import trainerprofile_bp
from meeting_routes import meeting_bp
from admin_Dashboard import admin_dashboard_bp
from routenutriprofile import nutriprofile_bp
from meeting_trainer_routes import meetingt_bp
from flask_mail import Mail, Message
from payment_route import payment_bp
from meeting_nutritionist_routes import meetingn_bp
from meeting_user_route import meetingu_bp

load_dotenv()

app = Flask(__name__)
CORS(app) 

# Set secret keys from environment variables
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default-jwt-secret")
JWTManager(app)
# Initialize JWT
setup_jwt(app)




mail = Mail()

def configure_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")  # your Gmail
    app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")  # app-specific password
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME")
    mail.init_app(app)

configure_mail(app)
# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(auth_ca, url_prefix="/create")
app.register_blueprint(member_bp,url_prefix="/member")
app.register_blueprint(review_bp, url_prefix="/review")
app.register_blueprint(report_bp, url_prefix="/report")
app.register_blueprint(trainerprofile_bp, url_prefix="/trainerprofile")
app.register_blueprint(meetingt_bp, url_prefix="/meeting")
app.register_blueprint(admin_dashboard_bp,url_prefix='/admin')
app.register_blueprint(nutriprofile_bp , url_prefix = "/nutriprofile")
app.register_blueprint(payment_bp, url_prefix="/payment")
app.register_blueprint(meetingn_bp, url_prefix="/meetingn")
app.register_blueprint(meetingu_bp , url_prefix = "/meetingu")

if __name__ == "__main__":
    app.run(debug=True)
