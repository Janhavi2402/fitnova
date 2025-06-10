import os

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton,
    QHBoxLayout, QLineEdit, QFrame, QMessageBox, QPlainTextEdit
)
from PyQt5.QtGui import QIcon, QClipboard
from PyQt5.QtCore import Qt
import requests

from ui.workout_page import WorkoutPage
from ui.trainer_Dashboard import TrainerDashboard
from ui.nutritionist_dashboard import NutritionistDashboard
from ui.MemberDashboard import MemberDashboardPage
from ui.admin_dashboard import AdminPage


class Login2Page(QWidget):
    def __init__(self, main_window, role):
        super().__init__()
        self.main_window = main_window
        self.role = role
        self.access_token = None

        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle(f"Login - {self.role}")

        main_layout = QVBoxLayout()

        # Back Button
        back_layout = QHBoxLayout()
        back_button = QPushButton("←")
        back_button.setFixedSize(40, 40)
        back_button.clicked.connect(self.go_back)
        back_layout.addWidget(back_button)
        back_layout.addStretch()
        main_layout.addLayout(back_layout)

        self.login_box = QFrame()
        self.login_box.setObjectName("formFrame")
        self.login_box.setFixedSize(500, 500)

        login_layout = QVBoxLayout(self.login_box)
        login_layout.setAlignment(Qt.AlignCenter)
        login_layout.setSpacing(12)

        self.role_label = QLabel(f"Login as {self.role}")
        self.role_label.setAlignment(Qt.AlignCenter)
        self.role_label.setObjectName("title")
        login_layout.addWidget(self.role_label)
        login_layout.addSpacing(10)

        # Email Input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Your Email....")
        self.email_input.setObjectName("emailField")
        login_layout.addWidget(self.email_input)
        login_layout.addSpacing(10)

        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password.....")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("passwordField")
        login_layout.addWidget(self.password_input)
        login_layout.addSpacing(15)

        # Forgot Password Button
        self.forgot_password_button = QPushButton("Forgot Password?")
        self.forgot_password_button.setObjectName("forgotPasswordButton")
        self.forgot_password_button.setFlat(True)
        self.forgot_password_button.setCursor(Qt.PointingHandCursor)
        self.forgot_password_button.clicked.connect(self.forgot_password)
        login_layout.addWidget(self.forgot_password_button, alignment=Qt.AlignRight)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.login)
        login_layout.addWidget(self.login_button)
        login_layout.addSpacing(15)

        # Create Account Section
        create_account_layout = QHBoxLayout()
        self.create_account_label = QLabel("New to FitNova? ")
        self.create_account_label.setObjectName("create_account_label")
        self.create_account_button = QPushButton("Create Account")
        self.create_account_button.setObjectName("switchButton")
        self.create_account_button.clicked.connect(self.create_account)
        create_account_layout.addWidget(self.create_account_label)
        create_account_layout.addWidget(self.create_account_button)
        create_account_layout.addStretch()
        login_layout.addLayout(create_account_layout)

        self.login_box.setLayout(login_layout)
        main_layout.addWidget(self.login_box, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

        self.apply_styles()

    def apply_styles(self):
        style_file = os.path.join(os.path.dirname(__file__), "login2page.qss")
        if os.path.exists(style_file):
            with open(style_file, "r") as file:
                self.setStyleSheet(file.read())

    def go_back(self):
        from ui.login_admin_user import Login1Page
        self.main_window.setCentralWidget(Login1Page(self.main_window))

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        if self.role == "Admin" or self.role == "Member":
            self.login_admin_member(email, password)
        elif self.role.lower() == "trainer":
            self.login_trainer(email, password)
        elif self.role.lower() == "nutritionist":
            self.login_nutritionist(email, password)
        else:
            QMessageBox.critical(self, "Error", f"Unknown role: {self.role}")

    def login_admin_member(self, email, password):
        url = "http://127.0.0.1:5000/auth/login" if self.role == "Member" else "http://127.0.0.1:5000/auth/admin/login"
        data = {"email": email, "password": password}

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            self.access_token = result.get("access_token")

            if self.access_token:
                QMessageBox.information(self, "Success", "Login successful!")
        

                if self.role == "Admin":
                    admin_details = self.fetch_admin_details()
                    if admin_details:
                        admin_page = AdminPage(self.main_window, admin_details)
                        self.main_window.setCentralWidget(admin_page)
                    else:
                        QMessageBox.critical(self, "Error", "Failed to fetch admin data")
                else:
                    self.navigate_to_workout()
            else:
                QMessageBox.critical(self, "Error", "Login failed: Access token not found")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Login failed: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {e}")

    def fetch_admin_details(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get("http://127.0.0.1:5000/auth/admin/details", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to fetch admin details: {e}")
            return None

    def login_trainer(self, email, password):
        url = "http://127.0.0.1:5000/create/trainerlogin"
        data = {"email": email, "password": password}

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()

            if "error" in result:
                QMessageBox.critical(self, "Error", f"Login failed: {result['error']}")
                return

            self.access_token = result.get("access-token")
            if self.access_token:
                QMessageBox.information(self, "Success", "Login successful!")
            
                user_data = result.get("user_data", {})
                self.main_window.access_token = self.access_token
                self.navigate_to_dashboard(user_data)
            else:
                QMessageBox.critical(self, "Error", "Login failed: Access token not found")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Login failed: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {e}")

    def login_nutritionist(self, email, password):
        url = "http://127.0.0.1:5000/create/nutritionistlogin"
        data = {"email": email, "password": password}

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()

            if "error" in result:
                QMessageBox.critical(self, "Error", f"Login failed: {result['error']}")
                return

            self.access_token = result.get("access-token")
            if self.access_token:
                QMessageBox.information(self, "Success", "Login successful!")
         
                user_data = result.get("user_data", {})
                self.main_window.access_token = self.access_token
                self.navigate_to_nutritionist_dashboard(user_data)
            else:
                QMessageBox.critical(self, "Error", "Login failed: Access token not found")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Login failed: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {e}")



    def create_account(self):
        if self.role in ["Member", "Admin"]:
            from ui.create_account_t_n import CreateAccount1Page
            self.main_window.setCentralWidget(CreateAccount1Page(self.main_window))
        else:
            from ui.create_Account_u_a import CreateAccount2Page
            create_account_page = CreateAccount2Page(self.main_window, role=self.role)
            if self.role.lower() == "trainer":
                create_account_page.trainer_data_ready.connect(
                    lambda data: self.navigate_to_dashboard(data)
                )
            elif self.role.lower() == "nutritionist":
                create_account_page.nutritionist_data_ready.connect(
                    lambda data: self.navigate_to_nutritionist_dashboard(data)
                )
            self.main_window.setCentralWidget(create_account_page)

    def navigate_to_workout(self):
        workout_page = WorkoutPage(self.main_window)
        workout_page.set_access_token(self.access_token)
        self.main_window.setCentralWidget(workout_page)

    def forgot_password(self):
        email = self.email_input.text()

        if not email:
            QMessageBox.warning(self, "Missing Email", "Please enter your email to reset password.")
            return

        url_map = {
            "member": "http://127.0.0.1:5000/auth/forgot-password",
            "admin": "http://127.0.0.1:5000/auth/admin/forgot-password",
            "trainer": "http://127.0.0.1:5000/auth/trainer/forgot-password",
            "nutritionist": "http://127.0.0.1:5000/auth/nutritionist/forgot-password"
        }

        role_key = self.role.lower()
        url = url_map.get(role_key)

        if not url:
            QMessageBox.critical(self, "Error", "Forgot password not supported for this role.")
            return

        try:
            response = requests.post(url, json={"email": email})
            response.raise_for_status()
            result = response.json()

            if result.get("message"):
                token = result.get("reset_token")
                QMessageBox.information(self, "Reset Token", f"Token: {token}\n\nUse this token on the next screen.")
                from ui.reset_password import ResetPasswordPage
                self.main_window.setCentralWidget(ResetPasswordPage(self.main_window,role_key))
            else:
                QMessageBox.warning(self, "Info", "If the email exists, a reset link has been sent.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request failed: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def navigate_to_dashboard(self, trainer_data):
        dashboard_page = TrainerDashboard(trainer_data, self.main_window)
        self.main_window.setCentralWidget(dashboard_page)
        self.main_window.access_token = self.access_token

    def navigate_to_nutritionist_dashboard(self , nutritionist_data ):
        dashboard_page = NutritionistDashboard(nutritionist_data , self.main_window)
        self.main_window.setCentralWidget(dashboard_page)
        dashboard_page.main_window.access_token = self.access_token