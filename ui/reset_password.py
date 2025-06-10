import sys
import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QApplication
)

class ResetPasswordPage(QWidget):
    def __init__(self, main_window, role):
        super().__init__()
        self.main_window = main_window
        self.role = role.lower()  
        self.setWindowTitle("Reset Password")

        layout = QVBoxLayout()

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Enter reset token")
        layout.addWidget(self.token_input)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_password_input)

        reset_button = QPushButton("Reset Password")
        reset_button.clicked.connect(self.reset_password)
        layout.addWidget(reset_button)

        self.setLayout(layout)

    def reset_password(self):
        token = self.token_input.text()
        new_password = self.new_password_input.text()

        if not token or not new_password:
            QMessageBox.warning(self, "Error", "Please enter token and new password!")
            return

     
        if self.role == "admin":
            api_url = "http://127.0.0.1:5000/auth/admin/reset-password"
        elif self.role == "trainer":
            api_url = "http://127.0.0.1:5000/auth/trainer/reset-password"
        elif self.role == "nutritionist":
            api_url = "http://127.0.0.1:5000/auth/nutritionist/reset-password"
        else:
            api_url = "http://127.0.0.1:5000/auth/reset-password"



        try:
            response = requests.post(
                api_url,
                json={"token": token, "new_password": new_password}
            )
            result = response.json()

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Password reset successful!")
                from ui.login_admin_user import Login1Page
                self.main_window.setCentralWidget(Login1Page(self.main_window))
            else:
                QMessageBox.critical(self, "Error", result.get("message", "Error resetting password"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Request failed: {e}")