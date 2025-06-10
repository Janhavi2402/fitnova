from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QComboBox, QLineEdit, QTextEdit, QMainWindow)
from PyQt5.QtCore import Qt
import requests

class reportSummary(QWidget):
    def __init__(self, main_window,username):
        super().__init__()
        
        self.main_window = main_window 
        self.username = username
        self.initUI()

    def initUI(self):
        self.setWindowTitle("FitNova - Health Report")
        self.setGeometry(100, 100, 500, 600)

        self.setStyleSheet("""
            QWidget { background-color: black; color: white; font-size: 16px; }
            QLabel { font-size: 20px; font-weight: bold; text-align: center; color: #0ff; }
            QLineEdit, QComboBox, QTextEdit {
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

        self.layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget(self)
        self.pages = []
        self.inputs = {}

        # --- Pages ---
        self.add_welcome_page()

        self.questions = [
            ("About You", "How do you identify?", ["Male", "Female", "Other"]),
            ("About You", "Your email address?", None),
            ("About You", "How old are you?", None),
            ("About You", "Your height in cm?", None),
            ("About You", "Your weight in kg?", None),
            ("Goals", "What's your goal?", ["Lose Weight", "Gain Muscle", "Stay Fit"]),
            ("Goals", "Your target weight?", None),
            ("Goals", "Your current body type?", ["Ectomorph", "Mesomorph", "Endomorph"]),
            ("Goals", "Your focus area?", None),
            ("Fitness Analysis", "Any previous workout experience?", ["Yes", "No"]),
            ("Fitness Analysis", "How fit are you?", ["Beginner", "Intermediate", "Advanced"]),
            ("Fitness Analysis", "Any medical conditions?", None),
            ("Fitness Analysis", "How often do you exercise?", ["Never", "Sometimes", "Regularly"]),
            ("Lifestyle", "How often do you walk?", None),
            ("Lifestyle", "When was the last time you were at your ideal weight?", None),
            ("Lifestyle", "Sleep every night (in hours)?", None),
            ("Lifestyle", "Feel any anxiety or stress?", ["Yes", "No"]),
            ("Lifestyle", "What motivates you the most?", None)
        ]

        self.add_question_pages()
        self.add_report_page()

        for page in self.pages:
            self.stacked_widget.addWidget(page)

        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

    def add_welcome_page(self):
        welcome_page = QWidget()
        welcome_layout = QVBoxLayout()
        label = QLabel("Hii.. Welcome to FitNova! Let's start with an intro")
        label.setAlignment(Qt.AlignCenter)
        button = QPushButton("Next")
        button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        welcome_layout.addWidget(label)
        welcome_layout.addWidget(button)
        welcome_page.setLayout(welcome_layout)
        self.pages.append(welcome_page)

    def add_question_pages(self):
        for index, (section, question, options) in enumerate(self.questions):
            page = QWidget()
            layout = QVBoxLayout()
            label = QLabel(f"{section}\n{question}")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

            if options:
                input_widget = QComboBox()
                input_widget.addItems(options)
            else:
                input_widget = QLineEdit()

            self.inputs[question] = input_widget
            layout.addWidget(input_widget)

            back_btn = QPushButton("Back")
            next_btn = QPushButton("Next" if index < len(self.questions) - 1 else "Submit")

            if index > 0:
                back_btn.clicked.connect(self.create_back_handler(index))
            else:
                back_btn.setEnabled(False)

            if index < len(self.questions) - 1:
                next_btn.clicked.connect(self.create_next_handler(index))
            else:
                next_btn.clicked.connect(self.generate_report)

            layout.addWidget(back_btn)
            layout.addWidget(next_btn)
            page.setLayout(layout)
            self.pages.append(page)

    def create_back_handler(self, index):
        return lambda: self.stacked_widget.setCurrentIndex(index)

    def create_next_handler(self, index):
        return lambda: self.stacked_widget.setCurrentIndex(index + 2)

    def add_report_page(self):
        self.report_page = QWidget()
        layout = QVBoxLayout()

        self.report_area = QTextEdit()
        self.report_area.setReadOnly(True)
        layout.addWidget(self.report_area)

        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(self.go_to_login2_page)
        layout.addWidget(back_btn)

        self.report_page.setLayout(layout)
        self.pages.append(self.report_page)

    def go_to_login2_page(self):
        if self.main_window:
            from ui.login_t_n import Login2Page  
            login2 = Login2Page(self.main_window, role="Member")
            self.main_window.setCentralWidget(login2)
        else:
            print("Main window not set. Can't navigate to login page.")

    def generate_report(self):
        try:
            user_data = {
                "name": self.username,
                "email": self.inputs["Your email address?"].text(),
                "age": self.inputs["How old are you?"].text(),
                "weight": self.inputs["Your weight in kg?"].text(),
                "height": self.inputs["Your height in cm?"].text(),
                "goal": self.inputs["What's your goal?"].currentText(),
                "fitness_level": self.inputs["How fit are you?"].currentText(),
            }
            response = requests.post("http://127.0.0.1:5000/report/generate_report", json=user_data)

            if response.status_code == 201:
                data = response.json().get("report", {})
                if not data:
                    self.report_area.setText("No data received from the server.")
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
                self.stacked_widget.setCurrentIndex(len(self.pages) - 1)
            else:
                self.report_area.setText("Error generating report. Please try again.")
        except Exception as e:
            print("Error:", str(e))
            self.report_area.setText(f"Error: {str(e)}")

