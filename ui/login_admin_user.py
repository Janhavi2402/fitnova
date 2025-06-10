import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMenu, QSizePolicy, QGridLayout, QFrame
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QRectF, QEasingCurve, QTimer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from ui.login_t_n import Login2Page  

class RoundedImageCard(QFrame):
    def __init__(self,  title, subtitle,sticker_path=None, parent=None):
        super().__init__(parent)
        self.setObjectName("roundedImageCard")
        self.setFixedSize(650, 250)  
        self.title = title
        self.subtitle = subtitle
        self.sticker = QPixmap(sticker_path) if sticker_path else None
        self.hovered = False
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.original_geometry = self.geometry()
        self.setStyleSheet("""
            QFrame#roundedImageCard {
                background-color: rgba(0, 255, 204, 0.1);
                border: 2px solid #00ffcc;
                border-radius: 20px;
            }
            
        """)
        

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw rounded background
        path = self.roundedRectPath(QRectF(self.rect()), 20)  
        painter.setClipPath(path)
        painter.fillPath(path, QColor(15, 32, 39, 230))
      


        title_font = QFont("Segoe UI", 24, QFont.Bold)
        painter.setFont(title_font)
        
        
        painter.setPen(QColor("#00ffc8"))
       
        painter.setPen(QColor("white"))

        title_rect = QRectF(0, 30, self.width() , 40)
        painter.setPen(QColor("#00ffd0"))
        painter.drawText(title_rect, Qt.AlignHCenter | Qt.AlignVCenter, self.title)

        
        
        subtitle_font = QFont("Arial", 14)
        subtitle_rect = QRectF(20, 80, self.width() - 40, self.height() - 100)
        painter.setFont(subtitle_font)
        painter.setPen(QColor("#d0ffd6"))
        painter.drawText(subtitle_rect,Qt.AlignVCenter|Qt.AlignHCenter | Qt.TextWordWrap, self.subtitle)

    def roundedRectPath(self, rectf, radius):
        path = QPainterPath()
        path.addRoundedRect(rectf, radius, radius)
        return path

    def enterEvent(self, event):
        if not self.hovered:
            self.hovered = True
            self.original_geometry = self.geometry()
            start_rect = self.original_geometry
            end_rect = start_rect.adjusted(0, -10, 0, -10)
            self.animation.setStartValue(start_rect)
            self.animation.setEndValue(end_rect)
            self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.hovered:
            self.hovered = False
            start_rect = self.geometry()
            end_rect = self.original_geometry
            self.animation.setStartValue(start_rect)
            self.animation.setEndValue(end_rect)
            self.animation.start()
        super().leaveEvent(event)

class Login1Page(QWidget): 
    def __init__(self, main_window, role=None):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Login Selection")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(800, 600)

        self.apply_styles()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)

        # Top bar layout
        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.setContentsMargins(0, 10, 20, 0)  
        self.top_bar_layout.setAlignment(Qt.AlignRight)

        # Back button
        self.back_button = QPushButton("←", self)
        self.back_button.setFixedSize(40, 40)
        self.back_button.setStyleSheet("""
            QPushButton{
                background-color: transparent;
                color: white;
                font-size : 24px;
                border: none;
            }
            QPushButton:hover{
                color: #00ffcc;
            }
        """)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.go_back_to_main)
        self.back_button.move(10, 10)

        # Login Dropdown
        self.login_button = QPushButton("Login")
        self.login_button.setFixedSize(120, 50)
        self.login_button.setObjectName("loginButton")
        self.login_button.setCursor(Qt.PointingHandCursor)

        # Dropdown menu
        self.menu = QMenu(self)
        self.menu.setObjectName("loginoption")

        roles = ["Member", "Admin", "Trainer", "Nutritionist"]
        for role in roles:
            action = self.menu.addAction(f"Login as {role}")
            action.triggered.connect(lambda checked, r=role: self.open_login_page(r))

        self.login_button.setMenu(self.menu)

        self.top_bar_layout.addWidget(self.login_button)

        # Cards Layout
        self.cards_layout = QGridLayout()
        self.cards_layout.setAlignment(Qt.AlignCenter)
        self.cards_layout.setHorizontalSpacing(30)
        self.cards_layout.setVerticalSpacing(40)
  

       
        self.workouts_card = RoundedImageCard( 
            
            "Workouts",
            "Discover workout plans tailored to your goals and track your progress daily."
        )

        self.schedule_card = RoundedImageCard(
           
            "Schedule",
            "Stay organized with your weekly sessions and never miss a workout or consultation."
        )

        self.report_summary_card = RoundedImageCard(
            
            "Report Summary",
            "Get a visual overview of your fitness journey with progress charts ."
        )

        self.nutritionist_card = RoundedImageCard(
            
            "Nutritionist",
            "Connect with certified nutritionist for tips."
        )

        self.premium_card = RoundedImageCard(
            
            "Premium",
            "Unlock exclusive features and premium content."
        )

        self.trainer_card = RoundedImageCard(
           
            "Trainer",
            "Connect with certified fitness trainers for live sessions, personalized feedback, and tips."
        )

        cards = [
             self.workouts_card,
             self.schedule_card,
             self.report_summary_card,
             self.nutritionist_card,
             self.trainer_card,
             self.premium_card
            ]

        for index , card in enumerate(cards):
           row = index // 2
           col = index % 2
           self.cards_layout.addWidget(card, row, col)


        self.main_layout.addLayout(self.top_bar_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.cards_layout)
        self.main_layout.addStretch(2)

    def go_back_to_main(self):
        if self.main_window:
            self.main_window.go_back_to_main()

    def apply_styles(self):
        css_file = os.path.join(os.path.dirname(__file__), "loginstyle.qss")

        if os.path.exists(css_file):
            with open(css_file, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Error: {css_file} not found!")

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#0f2027"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def open_login_page(self, role):
        self.main_window.role = role
        login_t_n = Login2Page(self.main_window, role)
        self.main_window.setCentralWidget(login_t_n)
        self.main_window.open_page(Login2Page, role=role)

if __name__ == "_main_":
    from main import MainWindow 

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())