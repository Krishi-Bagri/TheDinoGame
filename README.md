# The Dino Game

## Project Overview
This project utilizes real-time pose estimation to detect specific body poses using a webcam and triggers corresponding keyboard actions. The primary goal is to recognize poses like bending, jumping, and running, and simulate key presses (e.g., pressing the spacebar for a jump) using the PyAutoGUI library. The project leverages OpenCV for video capture, MediaPipe for pose estimation, and PyAutoGUI for automating keyboard inputs.

## Technologies Used
- *Programming Language*: Python 3.x
- *Libraries*:
  - OpenCV for video capture and image processing
  - MediaPipe for real-time pose detection
  - PyAutoGUI for simulating keyboard inputs
  - NumPy for numerical operations
- *Tools*:
  - Webcam for real-time video input
- *Operating System*: Windows 10 or Linux

## Setup Instructions
To set up the project locally, follow these steps:

1. *Clone the repository:*
    bash
    git clone https://github.com/your-username/pose-detection.git
    cd pose-detection
    

2. *Install the required Python libraries:*
    bash
    pip install -r requirements.txt
    

3. *Ensure your environment is set up:*
    - Make sure you have a functioning webcam connected to your computer.
    - Install the necessary drivers and tools for your operating system if needed.

## Usage Instructions
To use the project:

1. *Run the script*:
    bash
    python pose_detection.py
    
    The script will start capturing video from your webcam and detecting poses in real-time.

2. *Perform the following actions*:
   - *Bend*: If both legs are bent at an angle less than 90°, the script detects a "BEND" action and simulates pressing the "down" arrow key.
   - *Jump*: If both legs are straight (angle greater than 160°) and hands are in a jumping position, the script detects a "JUMP" action and simulates pressing the "space" key.
   - *Run*: When the hands are parallel to the ground, the script detects a "RUN" action. No key press is simulated, but this action is recognized.

3. *Exit the program*:
   - Press q on your keyboard to exit the application.
