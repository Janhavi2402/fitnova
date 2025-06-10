from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLabel, QSizePolicy, QGraphicsOpacityEffect
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPropertyAnimation
import sys

# Import UI pages
from ui.login_admin_user import Login1Page
from ui.ReportSummary import reportSummary


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fit Nova – Gym Management System")
        self.setGeometry(100, 100, 800, 600)
        self.role = None

        # Apply Enhanced Dark Theme and CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f0f0f;
            }

            QLabel#app_intro {
                color: #CCCCCC;
            }

            QLabel#title_label {
                color: #BB86FC;
                letter-spacing: 1px;
                padding: 10px;
            }

            QPushButton {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-size: 17px;
                font-weight: 600;
                padding: 12px;
                border: 2px solid #BB86FC;
                border-radius: 12px;

            }

            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #BB86FC, stop:1 #985EFF);
                color: #000000;
                font-weight: bold;
            }

            QPushButton:pressed {
                background-color: #3700B3;
                color: white;
            }

            QWidget {
                background-color: #0f0f0f;
                color: #E0E0E0;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

        self.pages = {
            "Continue to Login": Login1Page,
        }

        self.setup_main_page()

    def setup_main_page(self):
        """Creates and displays the enhanced main page with animation."""
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(20)

        # Top bar layout (placeholder if needed later)
        self.top_bar_layout = QVBoxLayout()

        # Title with animation
        self.title_label = QLabel("Welcome to FitNova!!", self)
        self.title_label.setObjectName("title_label")
        self.title_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)

        self.opacity_effect = QGraphicsOpacityEffect(self.title_label)
        self.title_label.setGraphicsEffect(self.opacity_effect)

        # Intro / Description
        self.intro_label = QLabel(
            "FitNova helps you track your workouts, monitor health metrics, and get personalized fitness plans.\n"
            "Manage your gym activities, get nutrition guidance, and stay on top of your fitness journey—all in one place!",
            self
        )
        self.intro_label.setObjectName("app_intro")
        self.intro_label.setFont(QFont("Segoe UI", 13))
        self.intro_label.setAlignment(Qt.AlignCenter)
        self.intro_label.setWordWrap(True)
        self.intro_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.intro_label.setMaximumWidth(800)
        self.intro_label.setMinimumHeight(10)

        # Add widgets to layout
        self.main_layout.addLayout(self.top_bar_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.intro_label, alignment=Qt.AlignCenter)
        self.main_layout.addSpacing(30)

        # Buttons
        for text, page_class in self.pages.items():
            button = QPushButton(text)
            button.setFixedHeight(45)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.clicked.connect(lambda checked, p=page_class: self.open_page(p))
            self.main_layout.addWidget(button)

        self.main_layout.addStretch(2)
        self.setCentralWidget(self.main_widget)

        self.animate_title()  # Start animation on launch

    def animate_title(self):
        """Creates fade-in animation for the title label."""
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1500)  # 1.5 seconds
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def open_page(self, page_class, data=None, role=None):
        """Opens the respective page inside the main window."""
        if role is not None:
            self.new_page = page_class(self, role)
        else:
            self.new_page = page_class(self)
        self.setCentralWidget(self.new_page)

    def open_report_summary(self):
        self.report_summary = reportSummary()
        self.report_summary.back_to_home_signal.connect(self.go_back_to_login)
        self.setCentralWidget(self.report_summary)

    def go_back_to_login(self):
        """Go back to Login1Page when back signal is received"""
        self.setCentralWidget(Login1Page(self))

    def go_back_to_main(self):
        """Return to main welcome screen"""
        self.setup_main_page()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Optional global fallback dark style
    app.setStyleSheet("""
        QWidget {
            background-color: #0f0f0f;
            color: white;
        }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
