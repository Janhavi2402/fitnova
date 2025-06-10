from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit)
from PyQt5.QtCore import Qt
import requests

class reportDisplay(QWidget):
    def __init__(self, main_window, username=None):
        super().__init__()
        self.main_window = main_window
        self.username = username

        self.setWindowTitle("FitNova - Health Report")
        self.setGeometry(100, 100, 500, 600)

        self.setStyleSheet("""
            QWidget { background-color: black; color: white; font-size: 16px; }
            QLabel { font-size: 20px; font-weight: bold; text-align: center; color: #0ff; }
            QTextEdit {
                background-color: rgba(50, 50, 50, 0.8);
                border: 2px solid #0ff;
                padding: 8px;
                border-radius: 5px;
                color: white;
            }
            QPushButton {
                background-color: #0ff;
                border: none;
                padding: 12px;
                border-radius: 5px;
                font-weight: bold;
                color: black;
            }
            QPushButton:hover { background-color: #00ffff; }
        """)

        layout = QVBoxLayout(self)

        self.title_label = QLabel("Your Personalized Health Report")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.report_area = QTextEdit()
        self.report_area.setReadOnly(True)
        layout.addWidget(self.report_area)

    def get_report(self):
        try:
            response = requests.post(
                "http://127.0.0.1:5000/report/generate_report",
                json={"name": self.username}
            )

            if response.status_code == 201:
                data = response.json().get("report", {})
                if not data:
                    self.report_area.setText("No report data found for this user.")
                    return

                report_text = f"""
Name: {data.get("name", "N/A")}
Email: {data.get("email", "N/A")}
Age: {data.get("age", "N/A")}
Weight: {data.get("weight", "N/A")} kg
Height: {data.get("height", "N/A")} cm
BMI: {data.get("bmi", "N/A")}
Fitness Level: {data.get("fitness_level", "N/A")}
Recommended Exercises: {data.get("recommended_exercises", "N/A")}
"""
                self.report_area.setText(report_text)
            else:
                self.report_area.setText("Error fetching report. Please try again.")
        except Exception as e:
            self.report_area.setText(f"Exception: {str(e)}")

    def go_to_login2_page(self):
        self.main_window.setCurrentIndex(0)

    def set_username(self, username):
        self.username = username
        print(f"Username updated to: {self.username}")

    def set_report_data(self, report_data):
        if not report_data:
            self.report_area.setText("No report data found.")
            return

        report_text = f"""
Name: {report_data.get("name", "N/A")}
Email: {report_data.get("email", "N/A")}
Age: {report_data.get("age", "N/A")}
Weight: {report_data.get("weight", "N/A")} kg
Height: {report_data.get("height", "N/A")} cm
BMI: {report_data.get("bmi", "N/A")}
Fitness Level: {report_data.get("fitness_level", "N/A")}
Recommended Exercises: {report_data.get("recommended_exercises", "N/A")}
"""
        self.report_area.setText(report_text)
