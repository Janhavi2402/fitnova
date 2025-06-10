import os
import requests
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QLineEdit,
    QFormLayout,
    QStackedWidget,
    QMessageBox
)
from PyQt5.QtGui import QPixmap , QIcon , QFont
from PyQt5.QtCore import Qt, pyqtSignal
import json
from ui.google_meet_page_t import GoogleMeetPage

class TrainerProfileView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("trainerProfileView")
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        form_container = QWidget()
        form_container.setObjectName("formContainer")
        form_container_layout = QVBoxLayout(form_container)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        label_font = QFont()
        label_font.setPointSize(14)
        label_font.setBold(True)

        self.name_label = QLabel()
        form_layout.addRow("Name:", self.name_label)
        self.email_label = QLabel()
        form_layout.addRow("Email:", self.email_label)
        self.phone_label = QLabel()
        form_layout.addRow("Phone:", self.phone_label)
        self.age_label = QLabel()
        form_layout.addRow("Age:", self.age_label)
        self.experience_label = QLabel()
        form_layout.addRow("Experience:", self.experience_label)
        self.gender_label = QLabel()
        form_layout.addRow("Gender:", self.gender_label)
        self.specialization_label = QLabel()
        form_layout.addRow("Specialization:", self.specialization_label)
        self.degree_label = QLabel()
        form_layout.addRow("Degree:", self.degree_label)
        self.location_label = QLabel()
        form_layout.addRow("Location:", self.location_label)
        self.role_label = QLabel()
        form_layout.addRow("Role:", self.role_label)

        for i in range(form_layout.rowCount()):
            label_item = form_layout.itemAt(i, QFormLayout.LabelRole)
            if label_item and isinstance(label_item.widget(), QLabel):
                label = label_item.widget()
                label.setFont(label_font)
                label.setStyleSheet("background-color: transparent; color: black ; margin: 8px; ")

        form_container_layout.addLayout(form_layout)
        self.layout.addWidget(form_container)


    def set_profile_data(self, data):
        if data:
            self.name_label.setText(f"{data.get('username', 'N/A')}")
            self.email_label.setText(f"{data.get('email', 'N/A')}")
            self.phone_label.setText(f"{data.get('phone', 'N/A')}")
            self.age_label.setText(f"{data.get('age', 'N/A')}")
            self.experience_label.setText(f"{data.get('experience', 'N/A')}")
            self.gender_label.setText(f"{data.get('gender', 'N/A')}")
            self.specialization_label.setText(f"{data.get('specialization', 'N/A')}")
            self.degree_label.setText(f"{data.get('degree', 'N/A')}")
            self.location_label.setText(f"{data.get('location', 'N/A')}")
            self.role_label.setText(f"{data.get('role', 'N/A')}")

            data_labels = [
                self.name_label, self.email_label, self.phone_label,
                self.age_label, self.experience_label, self.gender_label,
                self.specialization_label, self.degree_label,
                self.location_label, self.role_label
            ]

            for label in data_labels:
                label.setStyleSheet(
                    "background-color: white; "
                    "border: 1px solid #bdc3c7; "
                    "padding: 8px; "
                    "border-radius: 5px; "
                    "margin: 5px;"
                )
        else:
            self.name_label.setText("N/A")
            self.email_label.setText("N/A")
            self.phone_label.setText("N/A")
            self.age_label.setText("N/A")
            self.experience_label.setText("N/A")
            self.gender_label.setText("N/A")
            self.specialization_label.setText("N/A")
            self.degree_label.setText("N/A")
            self.location_label.setText("N/A")
            self.role_label.setText("N/A")
            # self.profile_picture_label.setText("No Picture")



class TrainerDashboard(QWidget):
    def __init__(self, trainer_data=None, main_window=None, parent=None):
        super().__init__(parent)
        self.icon_dir = os.path.dirname(os.path.abspath(__file__))
        self.main_window = main_window
        self.trainer_data = trainer_data
        self.setWindowTitle("Trainer Dashboard")
        self.setGeometry(100, 100, 800, 600)

        # Initialize views first
        self.profile_view = TrainerProfileView()
        self.edit_profile_widget = self.create_edit_profile_form()
        self.view_profile_widget = TrainerProfileView()

        # Create content area and store widget for later use
        self.content_area_widget = QStackedWidget()
        self.google_meet_widget = QLabel("Google Meet Integration Here")
        self.google_meet_widget.setAlignment(Qt.AlignCenter)

        self.google_meet_name_label = QLabel()
        self.google_meet_name_label.setAlignment(Qt.AlignCenter)

        self.google_meet_name_widget = QWidget()
        google_meet_name_layout = QVBoxLayout(self.google_meet_name_widget)
        google_meet_name_layout.addWidget(self.google_meet_name_label)

        # Add all widgets to the stacked widget
        self.content_area_widget.addWidget(self.view_profile_widget)
        self.content_area_widget.addWidget(self.edit_profile_widget)
        self.content_area_widget.addWidget(self.google_meet_widget)
        self.content_area_widget.addWidget(self.google_meet_name_widget)

        self.google_meet_page_t = GoogleMeetPage(self, self.main_window.access_token)
        self.content_area_widget.addWidget(self.google_meet_page_t)

        # Now that content_area_widget is ready, create sidebar
        self.sidebar = self.create_sidebar()

        # Layout setup
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area_widget)

        self.load_stylesheet()
        self.fetch_and_display_profile()
        self.show_view_profile()
        print("TrainerDashboard __init__ completed")

    def load_stylesheet(self):
        stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trainer_dashboard.qss")
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Stylesheet NOT found at {stylesheet_path}")

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        self.back_button = QPushButton("←")
        self.back_button.setFixedSize(40 , 40)
        self.back_button.setObjectName("sidebarButton")
        self.back_button.clicked.connect(self.go_back_to_login)
        sidebar_layout.addWidget(self.back_button)

        # Header frame with image and name
        header_frame = QFrame()
        header_frame.setObjectName("trainer_info_frame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignCenter)

        self.profile_picture_label = QLabel()
        self.profile_picture_label.setFixedSize(100, 100)
        self.profile_picture_label.setAlignment(Qt.AlignCenter)
        self.profile_picture_label.setObjectName("profile_picture_label")
        header_layout.addWidget(self.profile_picture_label)

        self.trainer_name_label = QLabel()
        self.trainer_name_label.setAlignment(Qt.AlignCenter)
        self.trainer_name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;background-color: transparent;")
        header_layout.addWidget(self.trainer_name_label)

        sidebar_layout.addWidget(header_frame)
        self.view_profile_button = QPushButton("View Profile")
        view_icon_path= os.path.join(self.icon_dir , "view_icon.png")
        self.view_profile_button.setIcon(QIcon(view_icon_path))
        self.view_profile_button.setObjectName("sidebarButton")
        self.view_profile_button.clicked.connect(self.show_view_profile)
        sidebar_layout.addWidget(self.view_profile_button)

        # Sidebar buttons
        self.edit_profile_button = QPushButton("Edit Profile")
        self.edit_profile_button.setIcon(QIcon(os.path.join(self.icon_dir, "edit_icon.png")))
        self.edit_profile_button.setObjectName("sidebarButton")
        self.edit_profile_button.clicked.connect(self.show_edit_profile)
        sidebar_layout.addWidget(self.edit_profile_button)

        self.google_meet_button = QPushButton("Google Meet")
        self.google_meet_button.setIcon(QIcon(os.path.join(self.icon_dir, "google_meeticon.png")))
        self.google_meet_button.setObjectName("sidebarButton")
        self.google_meet_button.clicked.connect(self.show_google_meet_page_t)
        sidebar_layout.addWidget(self.google_meet_button)

        sidebar_layout.addStretch()
        self.set_trainer_info()

        return sidebar
    
    def go_back_to_login(self):
        if self.main_window:
            from gymmanagement.ui.login_t_n import Login2Page 
            self.main_window.open_page(Login2Page, role="Trainer")

        
    def show_google_meet_page_t(self):
     self.google_meet_page_t.populate_meet_details()
     self.content_area_widget.setCurrentWidget(self.google_meet_page_t)


    def create_content_area(self):
     print("create_content_area started")

    # Create the stacked widget that holds content views
     self.content_area_widget = QStackedWidget()
     self.content_area_widget.setObjectName("content_area_widget")

    # Placeholder widgets
     self.google_meet_widget = QLabel("Google Meet Integration Here")
     self.google_meet_widget.setAlignment(Qt.AlignCenter)

     self.google_meet_name_label = QLabel()
     self.google_meet_name_label.setAlignment(Qt.AlignCenter)

     self.google_meet_name_widget = QWidget()
     google_meet_name_layout = QVBoxLayout(self.google_meet_name_widget)
     google_meet_name_layout.addWidget(self.google_meet_name_label)

    # Add widgets to stacked widget
     self.content_area_widget.addWidget(self.view_profile_widget)
     self.content_area_widget.addWidget(self.edit_profile_widget)
     self.content_area_widget.addWidget(self.profile_view)
     self.content_area_widget.addWidget(self.google_meet_widget)
     self.content_area_widget.addWidget(self.google_meet_name_widget)

    # Wrap the stacked widget in a frame
     container = QFrame()
     layout = QVBoxLayout(container)
     layout.addWidget(self.content_area_widget)

     print("create_content_area finished")
     return container  


    def set_trainer_info(self):
        if self.trainer_data:
            name = self.trainer_data.get("username", "Trainer Name")
            self.trainer_name_label.setText(name)
            
            image_path = os.path.join(self.icon_dir , "trainerimage.png")
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                self.profile_picture_label.setPixmap(
                    pixmap.scaled(100 , 100 , Qt.KeepAspectRatio)
                )
            else:
                self.profile_picture_label.setText("No Picture00");
        else:
            self.trainer_name_label.setText("Trainer Name")
            self.profile_picture_label.setText("No Picture")

    def create_edit_profile_form(self):
        edit_profile_widget = QScrollArea()
        edit_profile_widget.setWidgetResizable(True)
        edit_profile_widget.setObjectName("edit_profile_widget")

        edit_profile_container = QWidget()
        edit_profile_container.setObjectName("formFrame")
        edit_profile_layout = QVBoxLayout(edit_profile_container) 

        form_layout = QFormLayout()  # Inner form layout
        form_layout.setSpacing(15)

        label_font = QFont()
        label_font.setPointSize(14)
        label_font.setBold(True)

        input_font = QFont()
        input_font.setPointSize(12)

        self.name_input = QLineEdit()
        form_layout.addRow("Name ", self.name_input)
        self.email_input = QLineEdit()
        form_layout.addRow("Email ", self.email_input)
        self.phone_input = QLineEdit()
        form_layout.addRow("Phone ", self.phone_input)
        self.age_input = QLineEdit()
        form_layout.addRow("Age ", self.age_input)
        self.experience_input = QLineEdit()
        form_layout.addRow("Experience ", self.experience_input)
        self.gender_input = QLineEdit()
        form_layout.addRow("Gender ", self.gender_input)
        self.specialization_input = QLineEdit()
        form_layout.addRow("Specialization ", self.specialization_input)
        self.degree_input = QLineEdit()
        form_layout.addRow("Degree ", self.degree_input)
        self.location_input = QLineEdit()
        form_layout.addRow("Location ", self.location_input)
        self.role_input = QLineEdit()
        form_layout.addRow("Role ", self.role_input)

        for i in range(form_layout.rowCount()):
            label_item = form_layout.itemAt(i , QFormLayout.LabelRole)
            if label_item and isinstance(label_item.widget() , QLabel):
                label = label_item.widget()
                label.setFont(label_font)
                label.setStyleSheet("background-color: transparent ; color: black ; margin: 8px");

        # self.populate_edit_form()
        edit_profile_layout.addLayout(form_layout)

        self.save_profile_button = QPushButton("Save Profile")
        self.save_profile_button.setObjectName("saveButton")
        self.save_profile_button.clicked.connect(self.save_profile)

        edit_profile_layout.addWidget(self.save_profile_button)

        edit_profile_widget.setWidget(edit_profile_container)
        return edit_profile_widget

    def populate_edit_form(self):
        if self.trainer_data:
            self.name_input.setText(self.trainer_data.get("username", ""))
            self.email_input.setText(self.trainer_data.get("email", ""))
            self.phone_input.setText(self.trainer_data.get("phone", ""))
            self.age_input.setText(str(self.trainer_data.get("age", "")))
            self.experience_input.setText(str(self.trainer_data.get("experience", "")))
            self.gender_input.setText(self.trainer_data.get("gender", ""))
            self.specialization_input.setText(
                self.trainer_data.get("specialization", "")
            )
            self.degree_input.setText(self.trainer_data.get("degree", ""))
            self.location_input.setText(self.trainer_data.get("location", ""))
            self.role_input.setText(self.trainer_data.get("role", ""))

    def show_profile_view(self):
        print("show_profile_view started")
        self.content_area_widget.setCurrentWidget(self.profile_view)
        print("show_profile_view finished")

    def show_view_profile(self):
        print("show_view_profile started")
        self.view_profile_widget.set_profile_data(self.trainer_data)
        self.content_area_widget.setCurrentWidget(self.view_profile_widget)

    def show_edit_profile(self):
        # self.content_area_widget.setCurrentIndex(1) 
        self.content_area_widget.setCurrentWidget(self.edit_profile_widget)
        self.populate_edit_form()

    def show_google_meet(self):
      """Opens Google Meet Page and passes the access token."""
      self.google_meet_page_t = GoogleMeetPage(self, self.main_window.access_token)
      self.content_area_widget.addWidget(self.google_meet_page_t)
      self.google_meet_page_t.populate_meet_details()
    def save_profile(self):
        updated_data = {
            "username": self.name_input.text(),
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
            "age": self.age_input.text(),
            "experience": self.experience_input.text(),
            "gender": self.gender_input.text(),
            "specialization": self.specialization_input.text(),
            "degree": self.degree_input.text(),
            "location": self.location_input.text(),
            "role": self.role_input.text(),
        }

        try:
            api_url = "http://127.0.0.1:5000/trainerprofile/editprofile"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.main_window.access_token}",
            }
            response = requests.put(api_url , json=updated_data , headers=headers)
            response.raise_for_status()
            QMessageBox.information(self , "Profile Updated" , "Profile saved successfully!")
            self.fetch_and_display_profile()
           
        except requests.exceptions.RequestException as e:
            print(f"Oh No! Error in updating profile: {e}")
            QMessageBox.critical(self , "Error" , f"Could not update profile: {e}")
        except Exception as e:
            print(f"Unexpected error in updating the profile : {e}")
            QMessageBox.critical(self , "Error" , f"An error occurred: {e}")


    def fetch_and_display_profile(self):
        print("fetch_and_display_profile started")
        try:
            print(f"Main Window: {self.main_window}")
            print(f"Access Token: {getattr(self.main_window, 'access_token', 'Token not found')}") 
            api_url = "http://127.0.0.1:5000/trainerprofile/profile"
            headers = {
                "Authorization": f"Bearer {self.main_window.access_token}"            
            }
            print(f"Headers being sent: {headers}")
            response = requests.get(api_url , headers=headers)
            response.raise_for_status()

            profile_data = response.json()

            self.trainer_data = profile_data
            self.profile_view.set_profile_data(profile_data)
            self.view_profile_widget.set_profile_data(profile_data)
            # self.content_area_widget.setCurrentWidget(self.profile_view)

            self.set_trainer_info()
            self.show_view_profile()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching profile as : {e}")
            QMessageBox.critical(self , "Error" , f"Could not fetch profile : {e}")
        except Exception as e:
            print(f"Unexpected error fetching profile: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

        # if self.trainer_data:
        #     self.trainer_data.update(updated_data)
        #     self.set_trainer_info()
        #     print("Updated trainer data:", self.trainer_data)
        #     from PyQt5.QtWidgets import QMessageBox

        #     QMessageBox.information(
        #         self, "Profile Updated", "Profile saved successfully!"
        #     )


