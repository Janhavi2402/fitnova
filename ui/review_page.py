import requests
from PyQt5 import QtWidgets, QtGui, QtCore



class ReviewPage(QtWidgets.QWidget):
    def __init__(self,stacked_widget ):
        super().__init__()
        self.stacked_widget = stacked_widget # Store reference to main window
        self.setStyleSheet("background-color: #08142B;")  # Dark theme background
        self.selected_rating = 0  # Stores selected rating (1-5)
        
        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("Submit Your Review")
        title.setStyleSheet("color: #00FFFF; font-size: 50px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)

        self.review_input = QtWidgets.QTextEdit()
        self.review_input.setPlaceholderText("Write your review here...")
        self.review_input.setFixedHeight(450)  # Set a fixed height
        self.review_input.setStyleSheet("""
            background-color: rgba(0, 255, 255, 0.1);
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
            border: 2px solid #00FFFF;
             min-height: 450px;
        """)
         # Star Rating Layout
        star_layout = QtWidgets.QHBoxLayout()
        self.stars = []
        for i in range(5):
            star_btn = QtWidgets.QPushButton("★")
            star_btn.setFixedSize(50, 50)
            star_btn.setStyleSheet("font-size: 30px; color: gray; border: none;")
            star_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

            # Connect signals
            star_btn.enterEvent = lambda event, index=i: self.hover_stars(index + 1)  # Hover effect
            star_btn.leaveEvent = lambda event: self.reset_hover()  # Reset hover
            star_btn.clicked.connect(lambda checked, index=i: self.set_rating(index + 1))  # Click to select

            self.stars.append(star_btn)
            star_layout.addWidget(star_btn)   

        # Spacer for adding space between input box and submit button
        spacer = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        
        submit_btn = QtWidgets.QPushButton("Submit Review")
        submit_btn.setStyleSheet("""
            QPushButton {
        background-color: rgba(0, 255, 255, 0.7);  /* Slightly dull cyan */
        color: black;
        font-size: 18px;
        border-radius: 12px;
        font-weight: bold;
        padding: 8px;
    }
    QPushButton:hover {
        background-color: rgba(0, 255, 255, 1);  /* Brighter cyan on hover */
    }
    QPushButton:pressed {
        background-color: rgba(0, 200, 200, 1);  /* Slightly darker cyan on click */
    }
        """)
        submit_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        submit_btn.clicked.connect(self.submit_review)

        layout.addWidget(title)
        layout.addWidget(self.review_input)
        layout.addLayout(star_layout)  
        layout.addItem(spacer)
        layout.addWidget(submit_btn)

    def set_rating(self, rating):
        """Updates the selected rating and changes star colors"""
        self.selected_rating = rating
        self.update_star_colors()

    def hover_stars(self, rating):
        """Changes star color on hover"""
        for i, star_btn in enumerate(self.stars):
            if i < rating:
                star_btn.setStyleSheet("font-size: 30px; color: #FFD700; border: none;")  # Gold on hover
            else:
                star_btn.setStyleSheet("font-size: 30px; color: gray; border: none;")

    def reset_hover(self):
        """Resets stars to selected rating after hover"""
        self.update_star_colors()

    def update_star_colors(self):
        """Applies color based on selected rating"""
        for i, star_btn in enumerate(self.stars):
            if i < self.selected_rating:
                star_btn.setStyleSheet("font-size: 30px; color: #FFD700; border: none;")  # Gold for selected
            else:
                star_btn.setStyleSheet("font-size: 30px; color: gray; border: none;")  # Gray for unselected

    def submit_review(self):
    #  Get review text & rating
        review_text = self.review_input.toPlainText().strip()
        rating = self.selected_rating  

    #  Validate review text
        if not review_text:
           QtWidgets.QMessageBox.warning(self, "Empty Review", "Please write something before submitting.")
           return

    #  Validate rating
        if rating == 0:
           QtWidgets.QMessageBox.warning(self, "No Rating", "Please select a star rating before submitting.")
           return

    # Define the API endpoint (Flask backend)
        url = "http://127.0.0.1:5000/review/submit"

    #  Send the review and rating to the Flask API
        try:
            response = requests.post(url, json={"review": review_text, "rating": rating}) 

            if response.status_code == 201:
               QtWidgets.QMessageBox.information(self, "Thank You", "Your review has been submitted successfully!")
               self.review_input.clear()  # Clear input field
               self.selected_rating = 0  # Reset rating
               self.update_star_colors()  # Reset stars UI
               
              #  Ensure stacked_widget is properly used for navigation
               if isinstance(self.stacked_widget, QtWidgets.QStackedWidget):
                  self.stacked_widget.setCurrentIndex(4)  # Switch to ReviewDisplayPage
                
                #  Refresh the reviews on the display page
                  review_display_page = self.stacked_widget.widget(2)  # Get ReviewDisplayPage instance
                  if hasattr(review_display_page, "load_reviews"):
                    review_display_page.load_reviews()  # Reload all reviews
                
               else:
                QtWidgets.QMessageBox.warning(self, "Navigation Error", "Could not switch to the review display page.")
            else:
               QtWidgets.QMessageBox.warning(self, "Error", f"Failed to submit review: {response.json().get('message', 'Unknown error')}")
    
        except requests.exceptions.ConnectionError:
               QtWidgets.QMessageBox.critical(self, "Server Error", "Failed to connect to the server. Make sure the backend is running.")

class ReviewDisplayPage(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setStyleSheet("background-color: #08142B;")  # Dark background

        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("User Reviews")
        title.setStyleSheet("color: #00FFFF; font-size: 36px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)

         # Create a Scroll Area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")  # Remove border

        # Create a QWidget for content inside the scroll area
        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)


        self.review_list = QtWidgets.QTextEdit()
        self.review_list.setReadOnly(True)
        self.review_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)  
        self.review_list.setStyleSheet("""
            background-color: rgba(0, 255, 255, 0.1);
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
            border: 2px solid #00FFFF;
                                       
        """)
        scroll_layout.addWidget(self.review_list)  # Add review list inside scroll widget
        scroll_area.setWidget(scroll_widget)  # Set scroll widget inside scroll area

        back_btn = QtWidgets.QPushButton("⬅ Back")
        back_btn.setFixedSize(100, 40)
        back_btn.setStyleSheet("""
            QPushButton {
                background: none;
                color: #00FFFF;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        back_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        back_btn.clicked.connect(self.go_back)

        layout.addWidget(title)
        layout.addWidget(scroll_area)
        layout.addWidget(back_btn, alignment=QtCore.Qt.AlignCenter)

        self.load_reviews()  # Fetch and display reviews

    def load_reviews(self):
        url = "http://127.0.0.1:5000/review/all"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                reviews = response.json()
                formatted_reviews = "\n\n".join([f"⭐ {r['rating']}/5 - {r['review']}" for r in reviews])
                self.review_list.setText(formatted_reviews)
            else:
                self.review_list.setText("Failed to load reviews.")
        except requests.exceptions.ConnectionError:
            self.review_list.setText("Error: Could not connect to the server.")


    def go_back(self):
        if isinstance(self.stacked_widget, QtWidgets.QStackedWidget):
           self.stacked_widget.setCurrentIndex(3)  # Switch back to ReviewPage
        else:
           QtWidgets.QMessageBox.warning(self, "Navigation Error", "Could not go back to the review submission page.")
