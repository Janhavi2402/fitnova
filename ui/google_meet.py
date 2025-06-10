import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTextBrowser, QMessageBox
)
from PyQt5.QtCore import Qt

class GoogleMeetPageU(QWidget):
    def __init__(self, dashboard, member_details=None):
        super().__init__(dashboard.content_widget) 
        self.dashboard = dashboard
        self.member_details = member_details if member_details else {}
        self.setWindowTitle("My Google Meet Appointments")
        self.setGeometry(200, 200, 600, 400)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        # Title
        self.title_label = QLabel("📅 My Google Meet Appointments")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Text browser to show meetings
        self.meetings_browser = QTextBrowser()
        self.meetings_browser.setOpenExternalLinks(True)
        self.meetings_browser.setStyleSheet("color: white; background-color: #2c2c2c; padding: 10px;")
        self.layout.addWidget(self.meetings_browser)

        # Back button
        self.back_button = QPushButton("⬅ Back to Dashboard")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        # Fetch meetings data (only if member details are available)
        self.fetch_user_meetings()

    def fetch_user_meetings(self):
            print(self.member_details)
        
            user_id = self.member_details.get("id")
            user_name = self.member_details.get("name", "User")

            if not user_id:
                QMessageBox.critical(self, "Error", "User ID not found in profile.")
                return

            # Prepare headers for the API call
            headers = {"Authorization": f"Bearer {self.dashboard.access_token}"}

            # Fetch meetings data from the API
            self.get_meetings_data(user_id, user_name, headers)


    def get_meetings_data(self, user_id, user_name, headers):
        try:
            meetings_url = f"http://127.0.0.1:5000/meetingu/meetings?user_id={user_id}"
            meetings_response = requests.get(meetings_url, headers=headers)
            meetings_response.raise_for_status()
            meetings_data = meetings_response.json()

            trainer_meetings = meetings_data.get("trainer_meetings", [])
            nutritionist_meetings = meetings_data.get("nutritionist_meetings", [])

            self.display_meetings(user_name, trainer_meetings, nutritionist_meetings)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Could not fetch meetings: {e}")

    def display_meetings(self, user_name, trainer_meetings, nutritionist_meetings):
        # Format the meetings data into HTML
        meetings_html = f"<h3>Hi {user_name}, here are your upcoming meetings:</h3>"

        if trainer_meetings:
            meetings_html += "<h4>💪 Trainer Sessions:</h4><ul>"
            for meet in trainer_meetings:
                date = meet.get('date', 'Unknown Date')
                time = meet.get('time', 'Unknown Time')
                link = meet.get('meet_link', '#')
                trainer = meet.get('trainer_name', 'Trainer')
                meetings_html += (
                    f"<li><strong>{date} at {time}</strong> with <b>{trainer}</b>: "
                    f"<a href='{link}' style='color:#64b5f6;'>Join Meet</a></li>"
                )
            meetings_html += "</ul>"

        if nutritionist_meetings:
            meetings_html += "<h4>🥗 Nutritionist Sessions:</h4><ul>"
            for meet in nutritionist_meetings:
                date = meet.get('date', 'Unknown Date')
                time = meet.get('time', 'Unknown Time')
                link = meet.get('meet_link', '#')
                nutritionist = meet.get('nutritionist_name', 'Nutritionist')
                meetings_html += (
                    f"<li><strong>{date} at {time}</strong> with <b>{nutritionist}</b>: "
                    f"<a href='{link}' style='color:#64b5f6;'>Join Meet</a></li>"
                )
            meetings_html += "</ul>"

        if not trainer_meetings and not nutritionist_meetings:
            meetings_html += "<p>No meetings scheduled yet.</p>"

        self.meetings_browser.setHtml(meetings_html)

    def go_back(self):
        # Navigate back to the dashboard (ensure it's set correctly)
        self.dashboard.stacked_widget.setCurrentWidget(self.dashboard)
