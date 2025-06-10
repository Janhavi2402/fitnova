from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QStackedWidget, QFrame , QHBoxLayout
from PyQt5.QtCore import QTimer, QPropertyAnimation, QByteArray
from PyQt5 import QtWidgets, QtGui, QtCore
from ui.exercise_page import ExercisePage
from ui.MemberDashboard import MemberDashboardPage
from ui.review_page import ReviewPage, ReviewDisplayPage
from ui.ReportSummary  import reportSummary
from ui.ReportdisplayPage import reportDisplay
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
import requests

API_URL = "http://127.0.0.1:5000/member/details"  


class WorkoutContentPage(QtWidgets.QWidget):
    def __init__(self, workout_page):
        super().__init__()  
        
        self.workout_page = workout_page
        self.setStyleSheet ("background-color: #0d1b45;") 
        self.access_token = None

        layout = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel("🏋 Workout Sections")
        title.setStyleSheet(" background-color: #0d1b45; color: #00FF00; font-size: 30px; font-weight: bold; ")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(20)

        self.sections = ["Abs", "Arms", "Chest", "Leg", "ShoulderAndBack"]
        grid_layout = QtWidgets.QGridLayout()
        row, col = 0, 0

        for section in self.sections:
            section_widget = self.create_section_widget(section)
            grid_layout.addWidget(section_widget, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        layout.addLayout(grid_layout)
        layout.addStretch()

    def create_section_widget(self, section_name):
        section_widget = QtWidgets.QWidget()
        section_layout = QtWidgets.QVBoxLayout(section_widget)

        title = QtWidgets.QLabel(f"🔥 {section_name} Workouts")
        title.setStyleSheet(" color: white; font-size: 22px; font-weight: bold; ")
        title.setAlignment(QtCore.Qt.AlignCenter)
        section_layout.addWidget(title)

        levels = ["Beginner", "Intermediate", "Advanced"]
        for level in levels:
            btn = QtWidgets.QPushButton(level)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(0, 255, 0, 0.6);
                    color: black;
                    font-size: 16px;
                    padding: 10px;
                    border-radius: 8px;
                    border: 2px solid rgba(0, 255, 0, 0.8);
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(0, 255, 0, 1);
                    color: black;
                    border: 2px solid white;
                }
                QPushButton:pressed {
                    background: rgba(0, 255, 0, 0.9);
                }
            """)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            section_layout.addWidget(btn)

           
            btn.clicked.connect(lambda _, sec=section_name, lvl=level: self.workout_page.show_exercise_page(sec, lvl))
            section_layout.addWidget(btn)

        section_layout.addStretch()
        return section_widget
    


class ExerciseDetailPage(QtWidgets.QWidget):

    def get_exercises(self, section, level):
        """Returns a list of exercises based on section and level."""
        exercise_data = {
            "Abs": {
                "Beginner": ["Abdominal Crunches", "Jumping Jacks", "Leg Raises", "Mountain Climber", "Russian Twists"],
                "Intermediate": ["Bicycle Crunches", "Butt Bridge", "Side Bridges Left", "Plank (60 sec)", "V-Ups"],
                "Advanced": ["Abs Crunches", "Cobra Stretch", "Pushups", "Situps", "Spine Lumber Twist"]
            },
            "Arms": {
                "Beginner": ["Arm Circles (Clockwise)", "Arm Raises", "Chest Press Pulse", "Diagonal Plank"],
                "Intermediate": ["Tricep Dips", "Burpees", "Floor Tricep Dips", "Leg Barbell Curl", "Skipping", "Tricep Stretch"],
                "Advanced": ["Alternating Hooks", "Doorway Curls", "Modified Pushup Low Hold", "Push Up and Rotation", "Standing Biceps Stretch"]
            },
            "Chest": {
                "Beginner": ["Chest Stretch", "Inclined Push-ups", "Knee Push-ups", "Triceps Dips", "Wide Arm Push-ups"],
                "Intermediate": ["Decline Push-ups", "Hindu Push-ups", "Inclined Push-ups", "Push-up and Rotation", "Shoulder Stretch"],
                "Advanced": ["Bench Press", "Box Push-ups", "Burpees", "Pull Over", "Spiderman Push-ups"]
            },

            "Leg": {
        "Beginner": ["Donkey Kicks Left", "Knee To Chest Stretch Right", "Side Lying Leg Lift Left", "Squats", "Sumo Squat Calf Raises With Wall"],
        "Intermediate": ["Calf Stretch Right", "Fire Hydrant Left", "Jumping Jacks", "Lunges", "Side Leg Circles Left"],
        "Advanced": ["Burpees", "Curtsy Lunges", "Single Leg Deadlift Exercise", "Sumo Squat", "Wall Sit"]
    },

    "ShoulderAndBack": {
        "Beginner": ["Arm Raises", "Bench Press", "Pull Over", "Rhomboid Pulls", "Side Lying Floor Stretch Left"],
        "Intermediate": ["Arm Scissors", "Cat Cow Pose", "Child's Pose", "Hip Hinge", "Triceps Kickback"],
        "Advanced": ["Child's Pose", "Hyperextensions", "Pike Push-ups", "Reverse Push-ups", "Side Lying Floor Stretch Left", "Swimmer and Superman"]
    }
        }

        return exercise_data.get(section, {}).get(level, ["No exercises found"])

    def show_exercise_detail(self, exercise_name):
        """Displays selected exercise information."""
       
        exercise_page = ExercisePage(exercise_name, self,access_token=self.access_token) 
        self.pages.addWidget(exercise_page)  
        self.pages.setCurrentWidget(exercise_page)


    def go_back(self):
        """Goes back to the workout page."""
        self.workout_page.pages.setCurrentWidget(self.workout_page.workout_page)

    def __init__(self, section_name, level, workout_page,access_token=None):
        super().__init__()
        self.workout_page = workout_page
        self.setStyleSheet("background-color: #0d1b45; color: white;")  
        self.access_token = access_token

        layout = QtWidgets.QVBoxLayout(self)

    
        title = QtWidgets.QLabel(f"🔥 {section_name} - {level} Exercises")
        title.setStyleSheet("""
    font-size: 60px;  /* Bigger & Bolder */
    font-weight: 900;
    color: #00FF00;  /* Neon Green */
    
   
    padding: 10px;  /* Space around text */
    letter-spacing: 3px; /* Stylish Spacing */
""")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        
        container = QtWidgets.QWidget()
        container.setStyleSheet("""
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                stop:0 rgba(0, 255, 0, 0.2), stop:1 rgba(0, 0, 255, 0.2));
    border-radius: 15px;
    padding: 20px;
    border: 2px solid rgba(255, 255, 255, 0.2);
 
""")

        container_layout = QtWidgets.QVBoxLayout(container)

     
        exercises = self.get_exercises(section_name, level)
        for exercise in exercises:
            exercise_btn = QtWidgets.QPushButton(f"👉 {exercise}")
            exercise_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(0, 255, 0, 0.3);
                    color: white;
                    font-size: 20px;
                    padding: 15px;
                    border-radius: 12px;
                    font-weight: bold;
                    border: 2px solid rgba(0, 255, 0, 0.7);
                  
                }
                QPushButton:hover {
                    background: rgba(0, 255, 0, 0.8);
                    color: black;
                    border: 2px solid white;
                
                }
                QPushButton:pressed {
                    background: rgba(0, 255, 0, 1);
                    color: black;
                }
            """)
            exercise_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            exercise_btn.clicked.connect(lambda _, ex=exercise: self.show_exercise_detail(ex))
            container_layout.addWidget(exercise_btn)

        container.setLayout(container_layout)
        layout.addWidget(container)

        # back_btn = QtWidgets.QPushButton("⬅ Back")
        # back_btn.setFixedWidth(120)  
        # back_btn.setStyleSheet("""
        #     QPushButton {
        #         background: rgba(255, 255, 255, 0.2);
        #         color: white;
        #         font-size: 18px;
        #         padding: 12px;
        #         border-radius: 10px;
        #         font-weight: bold;
        #         border: 2px solid rgba(0, 255, 0, 0.7);
        #     }
        #     QPushButton:hover {
        #         background: rgba(0, 255, 0, 1);
        #         color: black;
        #         border: 2px solid white;
            
        #     }
        # """)
        # back_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # back_btn.clicked.connect(self.go_back)
        # layout.addWidget(back_btn)

    def get_exercises(self, section, level):
        """Returns a list of exercises based on section and level."""
        exercise_data = {
    "Abs": {
        "Beginner": ["Abdominal Crunches", "Jumping Jacks", "Leg Raises", "Mountain Climber", "Russian Twists"],
        "Intermediate": ["Bicycle Crunches", "Butt Bridge", "Side Bridges Left", "Plank (60 sec)", "V-Ups"],
        "Advanced": ["Abs Crunches", "Cobra Stretch", "Pushups", "Situps", "Spine Lumber Twist"]
    },
    "Arms": {
        "Beginner": ["Arm Circles (Clockwise)", "Arm Raises", "Chest Press Pulse", "Diagonal Plank"],
        "Intermediate": ["Tricep Dips", "Burpees", "Floor Tricep Dips", "Leg Barbell Curl", "Skipping", "Tricep Stretch"],
        "Advanced": ["Alternating Hooks", "Doorway Curls", "Modified Pushup Low Hold", "Push Up and Rotation", "Standing Biceps Stretch"]
    },
    "Chest": {
        "Beginner": ["Chest Stretch", "Inclined Push-ups", "Knee Push-ups", "Triceps Dips", "Wide Arm Push-ups"],
        "Intermediate": ["Decline Push-ups", "Hindu Push-ups", "Inclined Push-ups", "Push-up and Rotation", "Shoulder Stretch"],
        "Advanced": ["Bench Press", "Box Push-ups", "Burpees", "Pull Over", "Spiderman Push-ups"]
    },
    "Leg": {
        "Beginner": ["Donkey Kicks Left", "Knee To Chest Stretch Right", "Side Lying Leg Lift Left", "Squats", "Sumo Squat Calf Raises With Wall"],
        "Intermediate": ["Calf Stretch Right", "Fire Hydrant Left", "Jumping Jacks", "Lunges", "Side Leg Circles Left"],
        "Advanced": ["Burpees", "Curtsy Lunges", "Single Leg Deadlift Exercise", "Sumo Squat", "Wall Sit"]
    },

    "ShoulderAndBack": {
        "Beginner": ["Arm Raises", "Bench Press", "Pull Over", "Rhomboid Pulls", "Side Lying Floor Stretch Left"],
        "Intermediate": ["Arm Scissors", "Cat Cow Pose", "Child's Pose", "Hip Hinge", "Triceps Kickback"],
        "Advanced": ["Child's Pose", "Hyperextensions", "Pike Push-ups", "Reverse Push-ups", "Side Lying Floor Stretch Left", "Swimmer and Superman"]
    }
}

        return exercise_data.get(section, {}).get(level, ["No exercises found"])

    def show_exercise_detail(self, exercise_name):
        """Displays selected exercise information."""
        exercise_page = ExercisePage(exercise_name, self.workout_page,access_token=self.access_token)  # Pass exercise name to the ExercisePage
        self.workout_page.pages.addWidget(exercise_page)  # Add to stacked widget
        self.workout_page.pages.setCurrentWidget(exercise_page) 

    def go_back(self):
        """Goes back to the workout page."""
        self.workout_page.pages.setCurrentWidget(self.workout_page.workout_page)




class WorkoutPage(QtWidgets.QWidget):
    def __init__(self,main_window):
        self.main_window = main_window 
        super().__init__()  
        self.setStyleSheet("background-color: #050A1A;")

        main_layout = QtWidgets.QHBoxLayout(self)

        sidebar = QtWidgets.QWidget()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("""
            background: rgba(10, 40, 80, 0.9);
            border-radius: 15px;
            border: 2px solid rgba(0, 255, 255, 0.6);
        """)

        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)

        title_layout = QHBoxLayout()
        # back_btn = QtWidgets.QPushButton("⬅")
        # back_btn.setFixedSize(40 , 40 )
        # back_btn.setStyleSheet("""
        #     QPushButton {
        #         background: none;
        #         color: #00FFFF;
        #         font-size: 20px;
        #         font-weight: bold;
        #         border: none;
        #     }
        #     QPushButton:hover {
        #         color: white;
        #     }
        # """)
        # back_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # back_btn.clicked.connect(self.go_back)

        title = QtWidgets.QLabel("FITNOVA 💪")
        title.setStyleSheet("""
            color: #00FFFF;
            font-size: 28px;
            font-weight: bold;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)

        # title_layout.addWidget(back_btn)
        title_layout.addWidget(title)
        title_layout.addStretch()

        sidebar_layout.addLayout(title_layout)

        self.dashboard_btn = self.create_sidebar_button("🏠 Dashboard")
        self.report_btn = self.create_sidebar_button("📊 Report")
        self.workout_btn = self.create_sidebar_button("🏋 Workouts")
        self.review_btn = self.create_sidebar_button("⭐ Review")  
        self.logout_btn = self.create_sidebar_button("🚪 Logout")

        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(self.dashboard_btn)
        sidebar_layout.addWidget(self.report_btn)
        sidebar_layout.addWidget(self.workout_btn)
        sidebar_layout.addWidget(self.review_btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.logout_btn)  

        separator = QFrame()
        separator.setFixedWidth(5)
        separator.setStyleSheet("background-color: #00FFFF; border-radius: 2px;")

        self.pages = QStackedWidget()
        self.member_dashboard_page = MemberDashboardPage(self.pages)
        self.report_page = reportDisplay(self.main_window)
        self.workout_page = WorkoutContentPage(self)
        self.review_page = ReviewPage(self.pages)  
        self.review_display_page = ReviewDisplayPage(self.pages)
        
        self.pages.addWidget(self.workout_page)
        self.pages.addWidget(self.report_page)
        self.pages.addWidget(self.member_dashboard_page)
        self.pages.addWidget(self.review_page)
        self.pages.addWidget(self.review_display_page)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(separator)
        main_layout.addWidget(self.pages, 1)

        self.dashboard_btn.clicked.connect(self.go_to_dashboard_with_data)
        self.report_btn.clicked.connect(self.go_to_report_with_data)
        self.workout_btn.clicked.connect(lambda: self.pages.setCurrentWidget(self.workout_page))
        self.review_btn.clicked.connect(lambda: self.pages.setCurrentWidget(self.review_page))
        self.logout_btn.clicked.connect(self.go_back)
        
   
        
    def go_to_dashboard_with_data(self):
        if not self.access_token:
           QMessageBox.critical(self, "Error", "Access token is missing.")
           return

        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(API_URL, headers=headers)
            response.raise_for_status()
            member_data = response.json()

            self.member_dashboard_page.set_access_token(self.access_token)
            print(member_data)
            self.member_dashboard_page.set_member_info(member_data)

            member_name = member_data.get("name")
            print("Member Name:", member_name)

            report_response = requests.post(
              "http://127.0.0.1:5000/report/get_report",
              json={"name": member_name}
            )
            
            print(report_response)
            if report_response.status_code == 201:
                report_data = report_response.json().get("report", {})
                self.report_page.set_report_data(report_data)
            else:
               self.report_page.set_report_data(None)

            self.report_page.set_username(member_name)

      
            self.pages.setCurrentWidget(self.member_dashboard_page)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Could not load dashboard: {e}")

    


    def go_to_report_with_data(self):
        if not self.access_token:
           QMessageBox.critical(self, "Error", "Access token is missing.")
           return

        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(API_URL, headers=headers)
            response.raise_for_status()
            data = response.json()
            member_data = data.get("user")

            user_email = member_data.get("email")
            print(user_email)
           
            member_name = member_data.get("name")
            print("Member Name:", member_name)
            print("[DEBUG] Member Name:", member_name)
            print("[DEBUG] Member Email:", user_email)

            report_response = requests.post(
            "http://127.0.0.1:5000/report/get_report",
            json={"email": user_email}
            )

            print("[DEBUG] Report Fetch Status Code:", report_response.status_code)
            print("[DEBUG] Report Fetch Response:", report_response.text)

            
            print(report_response)
            if report_response.status_code == 200 and report_response.json().get("success"):
                report_data = report_response.json().get("report", {})
                self.report_page.set_report_data(report_data)
                print(report_data)
            else:
               self.report_page.set_report_data(None)

            self.report_page.set_username(member_name)

            self.pages.setCurrentWidget(self.report_page)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Could not load dashboard: {e}")




    def show_exercise_page(self, section, level):
        """This method will navigate to the ExerciseDetailPage."""
        exercise_detail_page = ExerciseDetailPage(section, level, self,self.access_token)
        self.pages.addWidget(exercise_detail_page)  
        self.pages.setCurrentWidget(exercise_detail_page) 

    def go_back(self):
        if self.main_window:
            self.main_window.go_back_to_main()

    def create_sidebar_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 255, 255, 0.6);
                color: black;
                font-size: 18px;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 255, 255, 1);
            }
        """)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        return btn
    
    def set_access_token(self, token):
        self.access_token = token
        print(f"WorkoutPage: Access token received: {self.access_token}")
     