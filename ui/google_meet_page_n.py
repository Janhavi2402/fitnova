import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QLineEdit, QDateEdit, QTimeEdit
)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtWidgets import QTextBrowser

class GoogleMeetPageN(QWidget):
    def __init__(self, dashboard, access_token):
        super().__init__(dashboard.content_area_widget)
        self.dashboard = dashboard
        self.access_token = access_token
        self.setWindowTitle("Google Meet Scheduler")
        self.setGeometry(200, 200, 600, 500)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.meet_label = QLabel("Google Meet Scheduler")
        self.meet_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.meet_label)

        self.nutritionist_name_label = QLabel("Fetching Nutritionist Name...")
        self.nutritionist_name_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.nutritionist_name_label)

        self.fetch_nutritionist_info()

        self.user_dropdown = QComboBox()
        self.layout.addWidget(self.user_dropdown)
        self.fetch_premium_users()

        self.meet_link_input = QLineEdit()
        self.meet_link_input.setPlaceholderText("Enter Google Meet Link")
        self.layout.addWidget(self.meet_link_input)

        self.date_picker = QDateEdit()
        self.date_picker.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_picker)

        self.time_picker = QTimeEdit()
        self.time_picker.setTime(QTime.currentTime())
        self.time_picker.setDisplayFormat("h:mm AP") 
        self.layout.addWidget(self.time_picker)

        self.schedule_button = QPushButton("Schedule Meeting")
        self.schedule_button.clicked.connect(self.schedule_meeting)
        self.layout.addWidget(self.schedule_button)

        self.previous_meetings_label = QTextBrowser()
        self.previous_meetings_label.setOpenExternalLinks(True)
        self.previous_meetings_label.setStyleSheet("color: white; background-color: #2c2c2c; padding: 10px;")
        self.layout.addWidget(self.previous_meetings_label)

        self.fetch_previous_meetings()

        self.back_button = QPushButton("Back to Dashboard")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

    def fetch_nutritionist_info(self):
        try:
            api_url = "http://127.0.0.1:5000/nutriprofile/profile"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            profile_data = response.json()
            nutritionist_name = profile_data.get("username", "nutritionist Name")
            self.nutritionist_name_label.setText(f"Nutritionist: {nutritionist_name}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Could not fetch nutritionist info: {e}")

    def fetch_premium_users(self):
        try:
            api_url = "http://127.0.0.1:5000/meetingn/get_premium_users"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            users = response.json()

            self.user_dropdown.clear()
            for user in users:
                self.user_dropdown.addItem(user["name"], user["user_id"])
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Could not fetch premium users: {e}")

    def schedule_meeting(self):
        user_id = self.user_dropdown.currentData()
        meet_link = self.meet_link_input.text()
        meeting_date = self.date_picker.date().toString("yyyy-MM-dd")
        meeting_time = self.time_picker.time().toString("hh:mm AP")


        if not meet_link:
            QMessageBox.warning(self, "Warning", "Please enter a valid Google Meet link.")
            return

        try:
            api_url_profile = "http://127.0.0.1:5000/nutriprofile/profile"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            profile_response = requests.get(api_url_profile, headers=headers)
            profile_response.raise_for_status()
            profile_data = profile_response.json()

            nutritionist_id = profile_data.get("_id", None)
            nutritionist_name = profile_data.get("username", "Nutritionist Name")

            if not nutritionist_id:
                QMessageBox.critical(self, "Error", "Could not retrieve nutritionist ID.")
                return

            api_url = "http://127.0.0.1:5000/meetingn/schedule_meeting"
            data = {
                "user_id": user_id,
                "user_name": self.user_dropdown.currentText(),
                "meet_link": meet_link,
                "date": meeting_date,
                "time": meeting_time,
                "nutritionist_id": nutritionist_id,
                "nutritionist_name": nutritionist_name
            }

            response = requests.post(api_url, json=data, headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Meeting scheduled successfully!")
            self.fetch_previous_meetings()
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to schedule meeting: {e}")

    def fetch_previous_meetings(self):
        try:
            api_url_profile = "http://127.0.0.1:5000/nutriprofile/profile"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            profile_response = requests.get(api_url_profile, headers=headers)
            profile_response.raise_for_status()
            profile_data = profile_response.json()

            nutritionist_id = profile_data.get("_id", None)
            if not nutritionist_id:
                QMessageBox.critical(self, "Error", "Could not retrieve nutritionist ID.")
                return

            api_url_meetings = f"http://127.0.0.1:5000/meetingn/get_previous_meetings/{nutritionist_id}"
            response = requests.get(api_url_meetings, headers=headers)
            response.raise_for_status()
            meetings = response.json()

            if not meetings:
                self.previous_meetings_label.setText("No previous meetings found.")
                return

            

            meetings_text = "<h3>Previous Meetings:</h3><ul>"

            for m in meetings:
             user_name = m.get('user_name', 'User')
             date = m.get('date', 'Unknown Date')
             time = m.get('time', 'Unknown Time')
             link = m.get('meet_link', 'No Link')
             meetings_text += (
    f"<li><strong>{user_name}</strong> — {date} at {time} - "
    f"<a href='{link}' style='color:#64b5f6;'>{link}</a></li>"
)

            meetings_text += "</ul>"

            self.previous_meetings_label.setHtml(meetings_text)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Could not fetch previous meetings: {e}")

    def go_back(self):
        self.dashboard.show_profile_view()

    def populate_meet_details(self):
        self.fetch_nutritionist_info()
        self.fetch_premium_users()
        self.fetch_previous_meetings()
