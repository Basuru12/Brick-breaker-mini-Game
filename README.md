# Brick Breaker 🎮

A simple **Brick Breaker** game built with [Pygame](https://www.pygame.org/), featuring sound effects, collision handling, and a start/quit menu.  
The paddle follows your mouse, and the goal is to destroy all bricks without letting the ball fall.

---

## 📸 Screenshot
*(Optional – add an image of your game here)*  
![Gameplay Screenshot](screenshot.png)

---

## 🚀 Features
- Start/Quit Menu with clickable buttons  
- Paddle & Ball Physics for realistic gameplay  
- Brick Collision Detection with sound effects  
- Win/Loss States with end messages  
- Customizable Assets (PNG images & MP3 sound files)  

---

## 📂 Folder Structure

├── main.py # Main game file
├── brick.png # Brick image
├── my_paddle.png # Paddle image
├── my_ball.png # Ball image
├── start_btn.png # Start button image
├── exit_btn.png # Exit button image
├── restart_btn.png # Restart button image
├── brick.MP3 # Brick hit sound
├── paddle_sound.MP3 # Paddle hit sound
├── game-music-7408.mp3 # Background music
├── brick-dropped-on-other-bricks-14722.mp3 # Alternate brick sound


---

## 🛠️ Requirements
- Python **3.8+**  
- [Pygame](https://www.pygame.org/news) library  

Install Pygame:
```bash
pip install pygame
🎯 How to Play
Run the game

bash
Copy
Edit
python main.py
Controls

Mouse – Move the paddle left/right

Click "Start" – Begin game

Click "Quit" – Exit game

Objective

Break all the bricks without missing the ball!

⚙️ Customization
You can replace:

Images (.png) with your own sprites

Sound effects (.mp3) with your own audio files

Adjust SCREEN_WIDTH, SCREEN_HEIGHT, and spd in main.py for difficulty
