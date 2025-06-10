import sys
import requests
import json
import base64
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFormLayout, QSpinBox, QComboBox, QFileDialog, QHBoxLayout, QWidget
)
from PyQt5.QtCore import pyqtSignal

class CreateAccount2Page(QWidget):

    trainer_data_ready = pyqtSignal(dict)
    nutritionist_data_ready = pyqtSignal(dict)

    def __init__(self, main_window, role=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.role = role
        self.initUI() 
        self.apply_styles()

        self.setWindowTitle("Create Account")
        self.setGeometry(100, 100, 600, 550)

    def initUI(self): 
        main_layout = QVBoxLayout()
        back_layout = QHBoxLayout()
        back_button = QPushButton("←")
        back_button.setFixedSize(40, 40)
        back_button.clicked.connect(self.go_back_to_login)
        back_layout.addWidget(back_button)
        back_layout.addStretch()
        main_layout.addLayout(back_layout)

        layout = QVBoxLayout()

        title = QLabel("Create Account")
        title.setObjectName("title")
        layout.addWidget(title)

        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        form_layout.addRow("Username:", self.username_input)

        self.email_input = QLineEdit()
        form_layout.addRow("Email:", self.email_input)

        self.phone_input = QLineEdit()
        form_layout.addRow("Phone:", self.phone_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_input)

        age_hbox = QHBoxLayout()
        self.age_input = QSpinBox()
        self.age_input.setRange(18, 100)
        age_hbox.addWidget(self.age_input)
        age_hbox.addStretch()
        form_layout.addRow("Age:", age_hbox)

        experience_hbox = QHBoxLayout()
        self.experience_input = QSpinBox()
        self.experience_input.setRange(0, 50)
        experience_hbox.addWidget(self.experience_input)
        experience_hbox.addStretch()
        form_layout.addRow("Experience (years):", experience_hbox)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        form_layout.addRow("Gender:", self.gender_input)

        self.specialization_input = QComboBox()
        self.specialization_input.addItems(["Weight Loss", "Muscle Gain", "General Fitness", "Strength Training"])
        form_layout.addRow("Specialization:", self.specialization_input)

        self.degree_input = QComboBox()
        self.degree_input.addItems(["BSc in Nutrition", "Certified Trainer", "Physiotherapy", "BSc in Sports Science"])
        form_layout.addRow("Degree:", self.degree_input)

        self.location_input = QLineEdit()
        form_layout.addRow("Location:", self.location_input)

        self.role_input = QComboBox()
        self.role_input.addItems(["Trainer", "Nutritionist"])
        form_layout.addRow("Role:", self.role_input)

        upload_hbox = QHBoxLayout() 
        self.upload_button = QPushButton("Upload Certification")
        self.upload_button.clicked.connect(self.upload_certification)
        upload_hbox.addWidget(self.upload_button)
        upload_hbox.addStretch() 

        upload_widget = QWidget()  
        upload_widget.setLayout(upload_hbox)

        form_layout.addRow("Certification:", upload_widget)  

        layout.addLayout(form_layout)

        self.submit_button = QPushButton("Create Account")
        self.submit_button.setObjectName("createaccountbutton")
        self.submit_button.clicked.connect(self.submit_form)
        layout.addWidget(self.submit_button)

        main_layout.addLayout(layout)
        self.setLayout(main_layout)

    def apply_styles(self):
        style_file = os.path.join(os.path.dirname(__file__), "createaccount_tn.qss")
        if os.path.exists(style_file):
            with open(style_file, "r") as file:
                self.setStyleSheet(file.read())
        else:
                print(f"Warning: Style file not found at {style_file}")

    def upload_certification(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Certification File", "", "PDF Files (*.pdf);;Image Files (*.jpg *.png)")
        if file_path:
            self.certification_path = file_path
            QMessageBox.information(self, "File Selected", f"Selected: {file_path}")

    def submit_form(self):
        if not self.certification_path:
            QMessageBox.warning(self, "Error", "Please upload a certification file.")
            return

        try:
            with open(self.certification_path, "rb") as file:
                encoded_certification = base64.b64encode(file.read()).decode()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read the certification file: {e}")
            return

        form_data = {
            "username": self.username_input.text().strip(),
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "password": self.password_input.text(),
            "age": self.age_input.value(),
            "experience": self.experience_input.value(),
            "gender": self.gender_input.currentText(),
            "specialization": self.specialization_input.currentText(),
            "degree": self.degree_input.currentText(),
            "location": self.location_input.text().strip(),
            "role": self.role_input.currentText().lower(),
            "certification": encoded_certification 
        }

        api_url = "http://127.0.0.1:5000/create/createaccount"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(api_url, data=json.dumps(form_data), headers=headers)

            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Account created successfully!")
                self.login_after_create(form_data["email"], form_data["password"])
                self.go_back_to_login()
            else:
                error_message = response.json().get('error', 'Unknown error')
                QMessageBox.warning(self, "Error", f"Failed to create account: {error_message}")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request failed: {e}")

    def login_after_create(self, email, password):
        api_url = "http://127.0.0.1:5000/create/tnlogin"
        data = {"email": email, "password": password}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(api_url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            access_token = result.get("access-token")

            if access_token:
                print(f"yeh! Login successful! Token : {access_token}")
                user_data = result.get("user_data", {})
                if user_data:
                    if user_data.get("role") == "trainer":
                        self.trainer_data_ready.emit(user_data)  
                    elif user_data.get("role") == "nutritionist":
                        self.nutritionist_data_ready.emit(
                            user_data) 
                    else:
                        print("Unknown user role!")
                        QMessageBox.warning(
                            self, "Error", "Unknown user role after login.")
                else:
                    print("No user data in login response!")
                    QMessageBox.warning(self, "Error", "No user data received after login.")
            else:
                print("Oh! Login Failed")
                QMessageBox.warning(self, "Login error", "Login failed after create account")

        except requests.exceptions.RequestException as e:
            print(f"login after create account : Request exception : {e}")
            QMessageBox.critical(self, "Login Error", f"Login request failed : {e}")
        except json.JSONDecodeError:
            print("login after create account : Invalid JSON response from server")
            QMessageBox.critical(self, "Login Error", "Invalid JSON response from server")

    def show_dashboard(self, trainer_data):
        
        pass

    def go_back_to_login(self):
        from ui.login_t_n import Login2Page
        login_page = Login2Page(self.main_window, self.role_input.currentText().lower())
        self.main_window.setCentralWidget(login_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreateAccount2Page(None) 
    window.show()
    sys.exit(app.exec_())