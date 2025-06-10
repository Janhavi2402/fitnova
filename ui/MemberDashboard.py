from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout,
    QProgressBar, QListWidget, QScrollArea, QFileDialog, QMessageBox, QStackedWidget, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_URL = "http://127.0.0.1:5000/member/details"

from ui.payment import FitNovaPayment
from ui.payment import get_payment_status_by_email
from ui.google_meet import GoogleMeetPageU


class MemberDashboardPage(QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget  

        self.setWindowTitle("Member Dashboard")
        self.setGeometry(200, 200, 800, 800)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #E0E0E0;
            }
            QLabel {
                color: #E0E0E0;
                font-size: 16px;
            }
            QPushButton {
                background-color: #1E88E5;
                color: #FFFFFF;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #42A5F5;
            }
            QProgressBar {
                height: 25px;
                border-radius: 10px;
                background-color: #333333;
                text-align: center;
                color: #FFFFFF;
            }
            QProgressBar::chunk {
                background-color: #1E88E5;
                border-radius: 10px;
            }
            QListWidget {
                background-color: #1E1E1E;
                border: 1px solid #555555;
                font-size: 15px;
                color: #E0E0E0;
                padding: 5px;
            }
            QFrame {
                background-color: #1E1E1E;
                border-radius: 14px;
                padding: 20px;
                border: 1px solid #2C2C2C;
            }
            QFrame:hover {
                border: 1px solid #1E88E5;
            }
        """)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.scroll_area)

        self.outer_layout = QVBoxLayout(self.content_widget)
        self.outer_layout.setSpacing(30)
        self.outer_layout.setContentsMargins(20, 20, 20, 20)

        # Top Row: Profile + Streak
        top_row = QHBoxLayout()
        self.add_profile_card()
        self.add_streak_card()
        top_row.addWidget(self.profile_card, 2)
        top_row.addWidget(self.streak_card, 1)
        self.outer_layout.addLayout(top_row)

        # Workout Section
        self.add_workout_card()
        self.outer_layout.addWidget(self.workout_card)

        # Achievements Section
        self.add_achievements_card()
        self.outer_layout.addWidget(self.achievements_card)

        # Premium Button
        self.add_premium_button()
        self.outer_layout.addWidget(self.premium_button)

        # Google Meet Button
        self.add_google_meet_button()
        self.outer_layout.addWidget(self.google_meet_button)

        # Refresh Button
        self.add_refresh_button()
        self.outer_layout.addWidget(self.refresh_button)

        self.add_graph_card() 
        self.outer_layout.addWidget(self.graph_card)  
        
        self.add_days_vs_workouts_graph() 
        self.outer_layout.addWidget(self.days_vs_workouts_graph)              

        self.access_token = None

    def _create_card(self):
        return QFrame()
    
    def add_google_meet_button(self):
        self.google_meet_button = QPushButton("📅 Google Meet")
        self.google_meet_button.setFixedHeight(45)
        
        # Temporary style for debugging
        self.google_meet_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                border: 2px solid red;  # Add a red border for visibility debugging
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
        """)
        
        self.google_meet_button.clicked.connect(self.go_to_google_meet_page)

    def go_to_google_meet_page(self):
     if not self.access_token:
        QMessageBox.warning(self, "Token Missing", "Access token not set.")
        return
     if not self.member_details:
            QMessageBox.warning(self, "Data Missing", "Member details not loaded.")
            return

     self.google_meet_page = GoogleMeetPageU(dashboard=self, member_details=self.member_details)
     self.stacked_widget.addWidget(self.google_meet_page)
     self.stacked_widget.setCurrentWidget(self.google_meet_page)



    def add_profile_card(self):
        self.profile_card = self._create_card()
        layout = QVBoxLayout(self.profile_card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        self.avatar_label = QLabel("V")
        self.avatar_label.setFixedSize(100, 100)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setStyleSheet("""
            QLabel {
                background-color: #1E88E5;
                color: white;
                font-size: 42px;
                border-radius: 50px;
                font-weight: bold;
            }
        """)

        self.name_label = QLabel("Name: Loading...")
        self.name_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.name_label.setAlignment(Qt.AlignCenter)

        self.email_label = QLabel("Email: Loading...")
        self.email_label.setFont(QFont("Segoe UI", 14))
        self.email_label.setAlignment(Qt.AlignCenter)
        
        self.payment_status_label = QLabel("💳 Payment Status: Loading...")
        self.payment_status_label.setFont(QFont("Segoe UI", 14))
        self.payment_status_label.setStyleSheet("color: #58a6ff;")
        self.payment_status_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.avatar_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.payment_status_label)

    def add_streak_card(self):
        self.streak_card = self._create_card()
        layout = QVBoxLayout(self.streak_card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        self.streak_label = QLabel("🔥 Current Streak: 0 days")
        self.streak_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.streak_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.streak_label)

    def add_workout_card(self):
        self.workout_card = self._create_card()
        layout = QVBoxLayout(self.workout_card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        workout_label = QLabel("🏋️‍♂️ Workout Data")
        workout_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        workout_label.setAlignment(Qt.AlignLeft)

        self.workout_time_label = QLabel("Total Workout Time: 0 minutes")
        self.workout_time_label.setFont(QFont("Segoe UI", 14))

        self.workout_count_label = QLabel("Total Workouts: 0")
        self.workout_count_label.setFont(QFont("Segoe UI", 14))

        self.progress_bar = QProgressBar()

        layout.addWidget(workout_label)
        layout.addWidget(self.workout_time_label)
        layout.addWidget(self.workout_count_label)
        layout.addWidget(self.progress_bar)

    def add_achievements_card(self):
        self.achievements_card = self._create_card()
        layout = QVBoxLayout(self.achievements_card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        label = QLabel("🏆 Achievements & Badges")
        label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        label.setAlignment(Qt.AlignLeft)

        self.achievements_list = QListWidget()

        layout.addWidget(label)
        layout.addWidget(self.achievements_list)

    def add_refresh_button(self):
        self.refresh_button = QPushButton("🔄 Refresh Profile")
        self.refresh_button.setFixedHeight(45)
        self.refresh_button.clicked.connect(self.fetch_and_display_member_data)

    def add_premium_button(self):
        self.premium_button = QPushButton("💎 Get Premium")
        self.premium_button.setFixedHeight(45)
        self.premium_button.setStyleSheet("""
            QPushButton {
                background-color: #AB47BC;
                color: #FFFFFF;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #BA68C8;
            }
        """)
        self.premium_button.clicked.connect(self.go_to_payment_page)

    def add_graph_card(self):
        self.graph_card = self._create_card()
        layout = QVBoxLayout(self.graph_card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        title = QLabel("📈 Streak & Workout Overview")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)

        self.figure = Figure(figsize=(5, 3), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(title)
        layout.addWidget(self.canvas)

        # Make sure the canvas is resized properly
        self.canvas.setMinimumSize(400, 300)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


    def add_days_vs_workouts_graph(self):
        self.days_vs_workouts_graph = self._create_card()
        layout = QVBoxLayout(self.days_vs_workouts_graph)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        title = QLabel("📉 Number of Days vs. Workouts")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)

        self.figure_days_vs_workouts = Figure(figsize=(5, 3), tight_layout=True)
        self.canvas_days_vs_workouts = FigureCanvas(self.figure_days_vs_workouts)

        layout.addWidget(title)
        layout.addWidget(self.canvas_days_vs_workouts)

        # Make sure the canvas is resized properly
        self.canvas_days_vs_workouts.setMinimumSize(400, 300)
        self.canvas_days_vs_workouts.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)    

    def update_graph(self, streak, workout_count):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        x = ["Streak Days", "Workouts"]
        y = [streak, workout_count]

        ax.bar(x, y, color=["#FF7043", "#42A5F5"])
        ax.set_ylabel("Count")
        ax.set_title("Your Fitness Progress")

        self.canvas.draw()


    def update_days_vs_workouts_graph(self, days, workouts):
        self.figure_days_vs_workouts.clear()
        ax = self.figure_days_vs_workouts.add_subplot(111)

        ax.plot(days, workouts, marker='o', color='green', linestyle='-', markersize=8)
        ax.set_xlabel("Days")
        ax.set_ylabel("Workouts")
        ax.set_title("Number of Days vs Workouts")

        self.canvas_days_vs_workouts.draw()

    def upload_payment_screenshot(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Payment Screenshot", "", "Images (*.png *.jpg *.jpeg);;All Files (*)", options=options)
        if file_path:
            QMessageBox.information(self, "Screenshot Uploaded", "Payment screenshot uploaded successfully!")
        else:
            QMessageBox.warning(self, "No File", "No screenshot was uploaded.")

    def set_access_token(self, token):
        self.access_token = token

    def set_member_info(self, data):
        self.member_details = data.get('user', {})
        user = data.get('user', {})
        name = user.get('name', 'N/A')
        email = user.get('email', 'N/A')

        self.name_label.setText(name)
        self.email_label.setText(email)

        self.avatar_label.setText(name[0].upper() if name else "?")
        
        # 💳 Fetch and display payment status
        payment_status = get_payment_status_by_email(email)
        self.payment_status_label.setText(f"💳 Payment Status: {payment_status.capitalize()}")
        
        streak = user.get('streak', 0)
        self.streak_label.setText(f"🔥 Current Streak: {streak} days")

        workout_count = user.get('workout_count', 0)
        total_seconds = workout_count * 20
        self.workout_time_label.setText(f"Total Workout Time: {total_seconds // 60} min {total_seconds % 60} sec")
        self.workout_count_label.setText(f"Total Workouts: {workout_count}")

        self.progress_bar.setMaximum(data.get('goal_total', 10))
        self.progress_bar.setValue(data.get('goal_completed', 0))

        self.achievements_list.clear()
        achievements = data.get('achievements', [])

        for a in achievements:
            self.achievements_list.addItem(f"🏅 {a}")

        if streak >= 5:
            for i in range(5, streak + 1, 5):
                self.achievements_list.addItem(f"🎖️ {i}-Day Streak Badge Unlocked!")

        if not achievements and streak < 5:
            self.achievements_list.addItem("📭 No achievements yet!")

        self.update_graph(streak, workout_count)
        self.update_days_vs_workouts_graph(range(1, streak + 1), [workout_count] * streak)

    def fetch_and_display_member_data(self):
        if not self.access_token:
            return
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(API_URL, headers=headers)
            response.raise_for_status()
            data = response.json()
            self.set_member_info(data)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch data: {e}")
       

    def go_to_payment_page(self):
        member_name = self.member_details.get("name", "Unknown")
        member_email = self.member_details.get("email", "unknown@example.com")

        payment_page = FitNovaPayment(name=member_name, email=member_email)
        self.stacked_widget.addWidget(payment_page)
        self.stacked_widget.setCurrentWidget(payment_page)
