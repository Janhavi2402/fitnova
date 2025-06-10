import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QProgressBar, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMovie
import requests 

# Dictionary to map exercises to GIFs
EXERCISE_GIFS = {
    "Abdominal Crunches": "ui\workouts\AbsBeginner\Eabdominalcrunches (2).gif",
    "Jumping Jacks": "ui\workouts\AbsBeginner\jumping jack.gif",
    "Leg Raises": "ui\workouts\AbsBeginner\legRaises.gif",
    "Mountain Climber": "ui\workouts\AbsBeginner\mountainClimber.gif",
    "Russian Twists": "ui\workouts\AbsBeginner\ErussianTwist.gif",
    "Bicycle Crunches": "ui\workouts\AbsIntermediate\BicycleCrunches.gif",
    "Butt Bridge": "ui\workouts\AbsIntermediate\ButtBridge.gif",
    "Side Bridges Left": "ui\workouts\AbsIntermediate\sideBridgesLeft.gif",
    "Plank (60 sec)": "ui\workouts\AbsIntermediate\plank.gif",
    "V-Ups": "ui\workouts\AbsIntermediate\Vup.gif",
    "Abs Crunches": "ui\workouts\AbsAdvanced\Eabscrunch (1).gif",
    "Cobra Stretch": "ui\workouts\AbsAdvanced\CobraStretch.gif",
    "Pushups": "ui\workouts\AbsAdvanced\PushUP.gif",
    "Situps": "ui\workouts\AbsAdvanced\sitUps.gif",
    "Spine Lumber Twist": "ui\workouts\AbsAdvanced\spineLumberTwist.gif",
    "Arm Circles (Clockwise)": "ui\workouts\ArmBegineer\EarmCircleClockwise.gif",
    "Arm Raises": "ui\workouts\ArmBegineer\EarmRaises.gif",
    "Diagonal Plank": "ui\workouts\ArmBegineer\diagonalPlank.gif",
    "Tricep Dips": "ui\workouts\ArmBegineer\TricepDips.gif",
    "Burpees": "ui\workouts\ArmIntermediate\Eburpees2.gif",
    "Floor Tricep Dips": "ui\workouts\ArmIntermediate\EfloorTricepDips.gif",
    "Leg Barbell Curl": "ui\workouts\ArmIntermediate\leg barbell curl.gif",
    "Skipping": "ui\workouts\ArmIntermediate\skipping.gif",
    "Tricep Stretch": "ui\workouts\ArmIntermediate\Etricep strech.gif",
    "Alternating Hooks": "ui\workouts\ArmAdvanced\Ealternating hooks.gif",
    "Doorway Curls": "ui\workouts\ArmAdvanced\doorway curls.gif",
    "Modified Pushup Low Hold": "ui\workouts\ArmAdvanced\modified pushup low hold.gif",
    "Push Up and Rotation": "ui\workouts\ArmAdvanced\push up and rotation.gif",
    "Standing Biceps Stretch": "ui\workouts\ArmAdvanced\standing biceps stretch.gif",
    "Chest Stretch": "ui\workouts\ChestBegineer\chest stretch.gif",
    "Inclined Push-ups": "ui\workouts\ChestBegineer\inclined push ups.gif",
    "Knee Push-ups": "ui\workouts\ChestBegineer\knee push ups.gif",
    "Triceps Dips": "ui\workouts\ChestBegineer\Etriceps dips.gif",
    "Wide Arm Push-ups": "ui\workouts\ChestBegineer\wide arm push ups.gif",
    "Decline Push-ups": "ui\workouts\ChestIntermediate\decline push up.gif",
    "Hindu Push-ups": "ui\workouts\ChestIntermediate\hindu push up.gif",
    "Inclined Push-ups": "ui\workouts\ChestIntermediate\inclined push ups.gif",
    "Push-up and Rotation": "ui\workouts\ChestIntermediate\push up and rotation.gif",
    "Shoulder Stretch": "ui\workouts\ChestIntermediate\shoulder stretch.gif",
    "Bench Press": "ui\workouts\ChestAdvanced\Ebench press.gif",
    "Box Push-ups": "ui\workouts\ChestAdvanced\Ebox push up.gif",
    "Burpees": "ui\workouts\ArmIntermediate\Eburpees2.gif",
    "Pull Over": "ui\workouts\ChestAdvanced\pull over.gif",
    "Donkey Kicks Left": "ui\workouts\LegBegineer\donkeyKicksLeft.gif",
    "Knee To Chest Stretch Right": "ui\workouts\LegBegineer\KneeToChestStretchRight.gif",
    "Side Lying Leg Lift Left": "ui\workouts\LegBegineer\sideLyingLegLiftLeft.gif",
    "Squats": "ui\workouts\LegBegineer\squats.gif",
    "Sumo Squat Calf Raises With Wall": "ui\workouts\LegBegineer\SumoSquatCalfRaisesWithWall.gif",
    "Calf Stetch Right": "ui\workouts\LegIntermediate\calfStrecthRight.gif",
    "Fire Hydrant Left": "ui\workouts\LegIntermediate\Efire hydrant left.gif",
    "Jumping Jacks": "ui\workouts\LegIntermediate\JumpingJacks.gif",
    "lunges": "ui\workouts\LegIntermediate\lunges.gif",
    "Side Leg Circles Left": "uui\workouts\LegIntermediate\side leg circles left.gif",
    "Burpees": "ui\workouts\ArmIntermediate\Eburpees2.gif",
    "Curtsy Lunges": "ui\workouts\LegAdvanced\Curtsy Lunges.gif",
    "Single Leg Deadlift Exercise": "ui\workouts\LegAdvanced\Single Leg Deadlift Exercise.gif",
    "Sumo Squat": "ui\workouts\LegAdvanced\sumo squat.gif",
    "Wall Sit": "ui\workouts\LegAdvanced\wall sit.gif",
    "Bench Press": "ui\workouts\ShoulderAndBackBegineer\Ebench press.gif",
    "Pull Over": "ui\workouts\ShoulderAndBackBegineer\pull over.gif",
    "Rhomboid Pulls": "ui\workouts\ShoulderAndBackBegineer\Erhomboid pulls.gif",
    "Side Lying Floor Stretch Left": "ui\workouts\ShoulderAndBackBegineer\side lying floor stretch left.gif",
    "Arm Scissors": "ui\workouts\ShoulderAndBackInterediate\Earm scissors.gif",
    "Cat Cow Pose": "ui\workouts\ShoulderAndBackInterediate\cat cow pose.gif",
    "Child's Pose": "ui\workouts\ShoulderAndBackInterediate\child's pose.gif",
    "Hip Hinge": "ui\workouts\ShoulderAndBackInterediate\hip hinge.gif",
    "Trcipeps Kickback": "ui\workouts\ShoulderAndBackInterediate\Etriceps kickback.gif",
    "Hyperextension": "ui\workouts\ShoulderAndBackAdvanced\hyperextensions.gif",
    "Pike Push-ups": "ui\workouts\ShoulderAndBackAdvanced\pike push ups.gif",
    "Reverse Push-ups": "ui\workouts\ShoulderAndBackAdvanced\Ereverse push ups.gif",
    "Side Lying Floor Stretch Left": "ui\workouts\ShoulderAndBackAdvanced\side lying floor stretch left.gif",
    "Swimmer and Superman": "ui\workouts\ShoulderAndBackAdvanced\swimmer and superman.gif",

}

class ExercisePage(QWidget):
    def __init__(self, exercise_name, workout_page, parent=None, access_token=None):
        super().__init__(parent)
        self.workout_page = workout_page
        self.exercise_name = exercise_name
        self.access_token = access_token
        self.setMinimumSize(600, 500)

        # Exercise Title
        self.exercise_label = QLabel(self.exercise_name, self)
        self.exercise_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.exercise_label.setAlignment(Qt.AlignCenter)

        # Animated Dummy (GIF)
        self.animation_label = QLabel(self)
        gif_path = EXERCISE_GIFS.get(self.exercise_name, "ui\\workouts\\AbsAdvanced\\PushUP.gif")
        self.movie = QMovie(gif_path)
        self.animation_label.setMovie(self.movie)
        self.movie.start()

        # Timer Label
        self.time_left = 20
        self.timer_label = QLabel(f"00:{self.time_left:02d}", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 18px; color: #007ACC;")

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(100)
        self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #007ACC; }")

        # Buttons
        self.pause_button = QPushButton("Pause", self)
        self.skip_button = QPushButton("Skip", self)
        self.restart_button = QPushButton("Restart", self)
        self.back_button = QPushButton("Back", self)

        # Connect button signals
        self.pause_button.clicked.connect(self.toggle_pause)
        self.skip_button.clicked.connect(self.skip_exercise)
        self.restart_button.clicked.connect(self.restart_exercise)
        self.back_button.clicked.connect(self.go_back)

        # Timer Setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.paused = False

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(self.exercise_label)

        # Center the GIF
        gif_layout = QHBoxLayout()
        gif_layout.addStretch()
        gif_layout.addWidget(self.animation_label)
        gif_layout.addStretch()
        layout.addLayout(gif_layout)

        layout.addWidget(self.timer_label)
        layout.addWidget(self.progress_bar)

        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.skip_button)
        layout.addLayout(button_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.restart_button)
        bottom_layout.addWidget(self.back_button)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(f"00:{self.time_left:02d}")
            self.progress_bar.setValue(int((self.time_left / 20) * 100))
        else:
            self.timer.stop()
            self.movie.stop()
            self.exercise_label.setText("Workout Complete!")
            self.send_workout_complete_request()

    def toggle_pause(self):
        if self.paused:
            self.timer.start(1000)
            self.movie.start()
            self.pause_button.setText("Pause")
        else:
            self.timer.stop()
            self.movie.stop()
            self.pause_button.setText("Resume")
        self.paused = not self.paused

    def skip_exercise(self):
        self.time_left = 5
        self.timer_label.setText(f"00:{self.time_left:02d}")
        self.progress_bar.setValue(int((self.time_left / 30) * 100))

    def restart_exercise(self):
        self.time_left = 20
        self.timer_label.setText(f"00:{self.time_left:02d}")
        self.progress_bar.setValue(100)
        self.timer.start(1000)
        self.movie.start()

    def go_back(self):
        self.workout_page.pages.setCurrentWidget(self.workout_page)

    def send_workout_complete_request(self):
        if not self.access_token:
            print("Access token not found. Cannot send workout completion request.")
            return

        url = "http://127.0.0.1:5000/member/complete_workout" 
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f" Workout count updated: {data['workoutCount']}, Streak: {data['streak']}")
            else:
                print(f" Failed to update workout count: {response.status_code} - {response.text}")
        except Exception as e:
            print(f" Error sending workout update: {e}")

    def set_access_token(self, token):
        self.access_token = token
        print(f"WorkoutPage: Access token received: {self.access_token}")
       