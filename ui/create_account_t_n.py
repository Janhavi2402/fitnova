import os
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout , QPushButton , QHBoxLayout , QLineEdit , QFrame , QMessageBox
from PyQt5.QtGui import QIcon , QFont
from PyQt5.QtCore import Qt
import requests
from ui.ReportSummary import reportSummary

class CreateAccount1Page(QWidget):
    def __init__(self , main_window):
        super().__init__()
        self.main_window = main_window 
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(20, 20, 20, 20) 

        back_layout = QHBoxLayout()
        back_button = QPushButton("←")                              
        back_button.setFixedSize(40, 40)
        back_button.setObjectName("backButton")
        back_button.clicked.connect(self.main_window.go_back_to_main) 
        back_layout.addWidget(back_button)
        back_layout.addStretch()  
        main_layout.addLayout(back_layout)

        self.form_frame = QFrame()
        self.form_frame.setObjectName("formFrame")
        self.form_frame.setFixedSize(500, 500)

        layout = QVBoxLayout(self.form_frame)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12) 


        title_label = QLabel("Create Account")
        title_label.setFont(QFont("Arial" , 18 , QFont.Bold))
        title_label.setObjectName("title")
        layout.addWidget(title_label , alignment = Qt.AlignCenter)
        
 
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Your User Name.....")
        self.username_input.setObjectName("usernameField")
        layout.addWidget(self.username_input)

       

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Your Email....")
        self.email_input.setObjectName("emailField")
        layout.addWidget(self.email_input)

        #Password 
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password.....")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("passwordField")
        layout.addWidget(self.password_input)

        #createaccount button
        create_account_button = QPushButton("Create Account")
        create_account_button.setObjectName("createaccountbutton")
        create_account_button.clicked.connect(self.create_account)
        layout.addWidget(create_account_button)
    
        # back to login
        back_to_login_button = QPushButton("Already have an account? Login")
        back_to_login_button.setObjectName("switchButton")
        back_to_login_button.clicked.connect(self.go_to_login)
        layout.addWidget(back_to_login_button)

        
        main_layout.addWidget(self.form_frame , alignment = Qt.AlignCenter)
        
        self.setLayout(main_layout)

        self.apply_styles()

    def create_account(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        data = {
           "name": username,
           "email": email,
           "password": password
        }

        print("Data to send:", data)
        try:
            if self.main_window.role == "Admin":
              url = "http://127.0.0.1:5000/auth/admin/register"
            else:
              url = "http://127.0.0.1:5000/auth/register"

            response = requests.post(url, json=data)
            response.raise_for_status()

            result = response.json()
            QMessageBox.information(self, "Success", result.get("message", "Account created successfully!"))

        # Navigate conditionally based on role
            if self.main_window.role == "Admin":
               self.go_to_login()
            else:
               self.go_to_report_summary(username)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to register: {e}")
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Failed to parse json response: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

   
    def go_to_report_summary(self,username):
        self.main_window.setCentralWidget(reportSummary(self.main_window,username))

    def apply_styles(self):
        style_file = os.path.join(os.path.dirname(__file__), "createaccount.qss")
        if os.path.exists(style_file):
            with open(style_file, "r") as file:
                self.setStyleSheet(file.read()) 

    def go_to_login(self):
        from ui.login_t_n import Login2Page

        role = self.main_window.role
        self.main_window.setCentralWidget(Login2Page(self.main_window , role))