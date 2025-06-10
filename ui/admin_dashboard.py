import sys
import os
import requests
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSizePolicy, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QBrush


class AdminPage(QWidget):
    def __init__(self, main_window, admin_details):
        super().__init__()
        self.main_window = main_window
        self.admin_details = admin_details

        self.setWindowTitle("Admin Dashboard")
        self.setMinimumSize(1100, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #0D1117;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#titleLabel {
                font-size: 32px;
                font-weight: bold;
            }
            QLabel#sectionTitle {
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 10px;
                color: #58a6ff;
            }
            QLabel.detailKey {
                font-size: 13px;
                color: #8b949e;
            }
            QLabel.detailValue {
                font-size: 16px;
                font-weight: bold;
                color: #c9d1d9;
            }
            QPushButton {
                background-color: #238636;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
            QPushButton#backButton {
                background-color: transparent;
                color: #58a6ff;
                font-size: 16px;
            }
            QPushButton#backButton:hover {
                text-decoration: underline;
            }
            QFrame#card {
                background-color: #161b22;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #30363d;
            }
            QLabel#avatarLabel {
                font-size: 32px;
                font-weight: bold;
                color: white;
                background-color: #238636;
                border-radius: 40px;
                min-width: 80px;
                min-height: 80px;
                max-width: 80px;
                max-height: 80px;
                qproperty-alignment: AlignCenter;
            }
        """)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Header with avatar, name, and logout
        self.create_header()

        # Scrollable body
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        container = QWidget()
        scroll_layout = QVBoxLayout(container)
        scroll_layout.setContentsMargins(40, 20, 40, 20)
        scroll_layout.setSpacing(20)

        section_label = QLabel("Admin Information")
        section_label.setObjectName("sectionTitle")
        scroll_layout.addWidget(section_label)

        # Grid of Info Cards
        grid = QGridLayout()
        grid.setSpacing(25)

        row, col = 0, 0
        icon_map = {
            "Name": "👤",
            "Email": "📧",
            "Role": "🛡️",
            "Department": "🏢",
            "Phone": "📞",
            "Joined": "📅"
        }

        for key, value in self.admin_details.items():
            card = QFrame()
            card.setObjectName("card")
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(8)

            key_label = QLabel(f"{icon_map.get(key, '🔹')} {key}")
            key_label.setProperty("class", "detailKey")
            key_label.setObjectName("detailKey")

            value_label = QLabel(value)
            value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            value_label.setProperty("class", "detailValue")
            value_label.setObjectName("detailValue")

            card_layout.addWidget(key_label)
            card_layout.addWidget(value_label)

            grid.addWidget(card, row, col)

            col += 1
            if col == 2:
                row += 1
                col = 0

        scroll_layout.addLayout(grid)

        # Payment Confirmations
        payments_label = QLabel("Pending Payment Confirmations")
        payments_label.setObjectName("sectionTitle")
        scroll_layout.addWidget(payments_label)

        self.payment_grid = QGridLayout()
        self.payment_grid.setSpacing(25)

        self.load_payment_screenshots()

        scroll_layout.addLayout(self.payment_grid)

        scroll_layout.addStretch()
        scroll_area.setWidget(container)

        self.main_layout.addWidget(scroll_area)

    def create_header(self):
        header = QHBoxLayout()
        header.setContentsMargins(20, 20, 20, 0)

        # Avatar
        avatar = QLabel(self.admin_details.get("Name", "A")[0].upper())
        avatar.setObjectName("avatarLabel")

        # Title & Name
        info_layout = QVBoxLayout()
        title_label = QLabel("Welcome Admin")
        title_label.setObjectName("titleLabel")

        name_label = QLabel(self.admin_details.get("Name", "Admin"))
        name_label.setStyleSheet("font-size: 18px; color: #8b949e;")
        info_layout.addWidget(title_label)
        info_layout.addWidget(name_label)

        header.addWidget(avatar)
        header.addSpacing(15)
        header.addLayout(info_layout)
        header.addStretch()

        # Back and Logout
        btn_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.go_back_to_main)
        back_btn.setCursor(Qt.PointingHandCursor)

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.go_back_to_main)
        logout_btn.setCursor(Qt.PointingHandCursor)

        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(logout_btn)

        header.addLayout(btn_layout)
        self.main_layout.addLayout(header)

    def go_back_to_main(self):
        from ui.login_admin_user import Login1Page
        self.main_window.setCentralWidget(Login1Page(self.main_window))

    def load_payment_screenshots(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        uploads_folder = os.path.join(base_dir, "..", "uploads")
        uploads_folder = os.path.abspath(uploads_folder)

        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)

        # Clean up previous items in the grid
        for i in reversed(range(self.payment_grid.count())):
            widget_to_remove = self.payment_grid.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        row, col = 0, 0
        found_images = False

        for file_name in os.listdir(uploads_folder):
            if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                found_images = True
                file_path = os.path.join(uploads_folder, file_name)

                name_email = os.path.splitext(file_name)[0]
                parts = name_email.split("_")
                name = parts[0].capitalize() if parts else "Unknown"
                email = parts[1] if len(parts) > 1 else "unknown@example.com"
                response = requests.get("http://localhost:5000/payment/status", params={"email": email})

                if response.status_code == 200:
                    payment = response.json()

                    if payment and payment.get("status") == "pending":
                        found_images = True

                        file_path = os.path.join(uploads_folder, file_name)

                        card = QFrame()
                        card.setObjectName("card")
                        card_layout = QVBoxLayout(card)
                        card_layout.setSpacing(10)

                        # Username label
                        user_label = QLabel(f"👤 {name}\n📧 {email}")
                        user_label.setObjectName("detailKey")

                        # Image
                        image_label = QLabel()
                        pixmap = QPixmap(file_path)
                        if not pixmap.isNull():
                            pixmap = pixmap.scaled(400, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            image_label.setPixmap(pixmap)
                        else:
                            image_label.setText("Image could not be loaded.")
                        image_label.setStyleSheet("border: 1px solid #30363d;")

                        # Buttons
                        button_layout = QHBoxLayout()
                        confirm_button = QPushButton("✅ Confirm")
                        reject_button = QPushButton("❌ Reject")

                        confirm_button.clicked.connect(lambda _, f=file_name: self.confirm_payment(f))
                        reject_button.clicked.connect(lambda _, f=file_name: self.reject_payment(f))

                        button_layout.addWidget(confirm_button)
                        button_layout.addWidget(reject_button)

                        card_layout.addWidget(user_label)
                        card_layout.addWidget(image_label)
                        card_layout.addLayout(button_layout)

                        self.payment_grid.addWidget(card, row, col)

                        col += 1
                        if col == 2:
                            col = 0
                            row += 1

        if not found_images:
            self.payment_grid.addWidget(QLabel("No payment screenshots found in 'uploads/' folder."))

    def confirm_payment(self, file_name):
        self.update_payment_status(file_name, "confirmed")

    def reject_payment(self, file_name):
        self.update_payment_status(file_name, "rejected")

    def update_payment_status(self, file_name, status):
        try:
          
            parts = os.path.splitext(file_name)[0].split("_")
            if len(parts) < 2:
                QMessageBox.warning(self, "Error", f"Invalid file name format: {file_name}")
                return

            email = "_".join(parts[1:])  # Extract email (removes the name part)

            #  Get latest payment entry for this email
            response = requests.get("http://localhost:5000/payment/status", params={"email": email})

            if response.status_code == 200:
                payment = response.json()

                if not payment:
                    QMessageBox.warning(self, "Error", "No payments found for this email.")
                    return

                # Get the payment id from the response
                payment_id = payment["_id"]

                if not payment_id:
                    QMessageBox.warning(self, "Error", "Payment ID not found.")
                    return

                if status == "confirmed":
                    #  Confirm payment (call the confirm payment route)
                    update_resp = requests.post(
                        f"http://localhost:5000/payment/confirm_payment/{payment_id}",
                        json={"status": status}
                    )
                else:
                    # For rejection, use the existing update route
                    update_resp = requests.post(
                        f"http://localhost:5000/payment/update_status/{payment_id}",
                        json={"status": status}
                    )

                if update_resp.status_code == 200:
                    QMessageBox.information(self, "Success", f"Payment {status}.")
                    self.load_payment_screenshots()  
                else:
                    QMessageBox.warning(self, "Error", "Failed to update payment status.")
            else:
                QMessageBox.warning(self, "Error", "Could not fetch payment data from server.")
        except Exception as e:
            QMessageBox.critical(self, "Exception", str(e))
