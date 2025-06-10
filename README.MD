# 💪 Fitnova – Desktop Fitness & Gym Management App

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/Framework-PyQt5-green?logo=qt&logoColor=white)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-brightgreen?logo=mongodb&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Fitnova** is a comprehensive desktop application designed to streamline individual fitness journeys and optimize gym management operations. It offers personalized health tracking, workout guidance, nutrition support, and role-based dashboards to deliver a smooth and engaging experience for everyone—from users to trainers, nutritionists, and administrators.

---

## 🧩 Features

### 🏋️ Health and Progress Tracking
- Collects user health inputs and fitness goals.
- Automatically generates personalized reports, including **BMI calculations**.
- Recommends workouts tailored to user profiles.
- Visualizes **workout streaks** and progress over time using interactive graphs.

### 🥗 Nutrition Management
- **Premium users** are paired with **personal trainers and nutritionists**.
- Sessions are scheduled via **Google Meet**, managed by trainers/nutritionists.

### 🔄 Workouts
- All users have access to a curated set of workouts.
- Includes **instructional animations** and a **built-in timer** for guided sessions.

### 🏢 Gym Management
- Users can **take premium** and upload **payment screenshots**.
- Admins can **verify payments** and activate premium features through their dashboard.

### 📊 Role-Based Dashboards
- **Users**:
  - View workout history and streaks.
  - Premium Users can attend one on one sessions with trainer and nutritionist through google meet.
- **Trainers/Nutritionists**:
  - Manage profiles with qualifications and experience.
  - Schedule and conduct user sessions.
- **Admins**:
  - Approve new accounts and manage memberships.
  - Review and validate payment details.

### 🔐 Authentication System
- Secure **email & password-based login and registration**.
- Role-specific registration:
  - Trainers and nutritionists must submit **qualifications and experience** for approval.

### 🌟 Reviews & Ratings
- Users can provide **review** and rate trainers/nutritionists.
- Promotes continuous service improvement based on user input.

---

## 🚀 Installation

> Make sure Python 3.x and all dependencies are installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/Janhavi2402/fitnova.git
   cd gymmanagement
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database in `Backend/database.py`:
   - Create a MongoDB database named **Fitnova** with the following collections:
     ```
     users_collection,
     trainer_collection,
     nutritionist_collection,
     admin_collection,
     member_Dashboard,
     meeting_collection,
     meeting_nutritionist_collection,
     user_Report
     ```

4. Set up the `.env` file with the following:
   ```
   MAIL_USERNAME=your_email@example.com      # Authorized email for sending mails
   MAIL_PASSWORD=your_email_password
   JWT_SECRET_KEY=your_generated_jwt_secret
   ```

   👉 Generate the JWT secret key using:
   ```python
   import secrets
   print("JWT Secret Key:", secrets.token_hex(32))
   ```

5. Start the backend server:
   ```bash
   cd Backend
   python app.py
   ```

6. Run the main application:
   ```bash
   python main.py
   ```

---

## 🛠️ Tech Stack

- **Python** (PyQt5 for desktop UI)
- **Backend** (Flask)
- **MongoDB** for data storage
- **Matplotlib/Plotly** for visualizations
- **JWT & password hashing** for secure authentication

---

## 📁 Project Structure

```
gymmanagement/
├── Backend/
├── ui/
├── uploads/
├── .gitignore
├── README.md
├── main.py
└── requirements.txt
```

---

## 👨‍💻 Developed By
- [**Muskan Tomar**](https://github.com/Vaish-011)
- [**Rachita Laad**](https://github.com/RACHITALAAD)
- [**Viditi Joshi**](https://github.com/vj2573)
- [**Janhavi Patil**](https://github.com/Janhavi2402)
- [**Rasika Kale**](https://github.com/rasika2114)

---

## 🤝 Contribution

We welcome contributions! Feel free to open issues or submit pull requests to help improve **Fitnova**.