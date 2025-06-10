import sys
import os
import shutil
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSpacerItem,
    QSizePolicy, QFileDialog
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class FitNovaPayment(QWidget):
    def __init__(self, name, email):
        super().__init__()
        self.name = name
        self.email = email
        self.setWindowTitle("FitNova - Support via PhonePe")
        self.showMaximized()
        self.setStyleSheet(self.dark_theme())
        self.screenshot_uploaded = False
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        title = QLabel("Support FitNova 💪")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        qr_label = QLabel(self)
        pixmap = QPixmap(r"ui\fitnova_qr.png")
        pixmap = pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        qr_label.setPixmap(pixmap)
        qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(qr_label)

        instruction = QLabel("Scan this QR using PhonePe or any UPI app")
        instruction.setFont(QFont("Arial", 16))
        instruction.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction)

        upload_button = QPushButton("📤 Upload Payment Screenshot")
        upload_button.setFont(QFont("Arial", 14))
        upload_button.setObjectName("uploadButton")
        upload_button.clicked.connect(self.upload_screenshot)
        layout.addWidget(upload_button, alignment=Qt.AlignCenter)

        self.confirm_button = QPushButton("✅ I Have Paid")
        self.confirm_button.setFont(QFont("Arial", 18, QFont.Bold))
        self.confirm_button.setObjectName("confirmButton")
        self.confirm_button.setFixedSize(250, 50)
        self.confirm_button.setEnabled(False)
        self.confirm_button.clicked.connect(self.show_success)
        layout.addWidget(self.confirm_button, alignment=Qt.AlignCenter)

        self.screenshot_label = QLabel(self)
        self.screenshot_label.setAlignment(Qt.AlignCenter)
        self.screenshot_label.setVisible(False)
        layout.addWidget(self.screenshot_label)

        self.tick_label = QLabel(self)
        self.tick_label.setAlignment(Qt.AlignCenter)
        self.tick_label.setVisible(False)
        layout.addWidget(self.tick_label)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def show_success(self):
        tick_pixmap = QPixmap(r"ui\tick.png").scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.tick_label.setPixmap(tick_pixmap)
        self.tick_label.setVisible(True)

    def upload_screenshot(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Payment Screenshot", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            # Prepare uploads folder
            upload_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
            os.makedirs(upload_dir, exist_ok=True)

            # Copy uploaded screenshot
            base_name = os.path.basename(file_name)
            file_ext = os.path.splitext(base_name)[1]
            filename = f"{self.name}_{self.email}{file_ext}".replace(" ", "_")
            destination = os.path.join(upload_dir, filename)
            shutil.copy(file_name, destination)

            # Display preview
            pixmap = QPixmap(destination).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.screenshot_label.setPixmap(pixmap)
            self.screenshot_label.setVisible(True)

            self.screenshot_uploaded = True
            self.confirm_button.setEnabled(True)
            self.submit_payment_to_backend(destination)

    def submit_payment_to_backend(self, screenshot_url):
        url = "http://localhost:5000/payment/submit"
        payload = {
          "name": self.name,
           "email": self.email,
           "screenshot_url": screenshot_url  # send path to screenshot
        }

        try:
           response = requests.post(url, json=payload)
           if response.status_code == 201:
             print("Payment submitted successfully to backend")
           else:
             print(" Backend error:", response.status_code, response.text)
        except Exception as e:
            print(" Exception during submission:", str(e))

    def dark_theme(self):
        return """
            QWidget {
                background-color: #0F0F0F;
                color: #FFFFFF;
            }

            QLabel {
                color: #E0E0E0;
            }

            QPushButton {
                background-color: #00C853;
                color: white;
                border: none;
                border-radius: 25px;
                padding: 12px;
            }

            QPushButton#confirmButton:disabled {
                background-color: #555555;
                color: #cccccc;
            }

            QPushButton#confirmButton:hover:enabled {
                background-color: #00E676;
            }

            QPushButton#uploadButton {
                background-color: #1E88E5;
                color: white;
                border-radius: 20px;
                padding: 10px;
                margin-top: 10px;
            }

            QPushButton#uploadButton:hover {
                background-color: #1565C0;
            }
        """
     


def get_payment_status_by_email(email):
    try:
        response = requests.get(f"http://localhost:5000/payment/status?email={email}")
        if response.status_code == 200:
            data = response.json()  
            return data.get("status", "unknown")
        elif response.status_code == 404:
            return "not found"
        else:
            return "error"
    except Exception as e:
        print(f"Exception while fetching payment status: {e}")
        return "error"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FitNovaPayment()
    window.show()
    sys.exit(app.exec_())
