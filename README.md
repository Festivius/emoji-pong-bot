# Instagram Emoji Pong Bot
This project uses OpenCV and PyQt5 to detect a ball and paddle from a screen capture of the Emoji Pong game on Instagram and predict the ball's trajectory. It features real-time updates, trajectory visualization using an overlay window, and automated interaction via PyAutoGUI.
# Features
-  Takes screenshots of the user's screen and identifies where on the screen the game is being played.
-  Uses contour detection and bounding shapes to identify the location of the ball and paddle.
-  Calculates the ball's trajectory by finding the slope it bounces at, using simple math to account for reflections off walls.
-  A transparent PyQt5 window displays the ball’s capture locations and predicted path.
-  Simulates clicks using PyAutoGUI to respond to the ball's trajectory.
# Requirements
- Python 3.8 or higher
- OpenCV
- NumPy
- PyAutoGUI
- MSS
- Pillow
- PyQt5
- Matplotlib

- BlueStacks5 (to run the game on your laptop)
# Usage
1. Download bot.py and the required libraries listed above.
2. Ensure the game window is visible on the screen.
3. Run the script and immediately play the first 1-2 rounds manually.
