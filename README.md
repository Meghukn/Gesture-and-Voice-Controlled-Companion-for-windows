# Gesture-and-Voice-Controlled-Companion-for-windows
Mitra – A Smart Multimodal Virtual Assistant  Mitra is an advanced virtual assistant designed to enhance user interaction through voice commands, hand gestures, and facial recognition. It supports both English and Kannada.


## ✨ Features

**Voice Assistant** – Execute commands using natural language processing.
**Multilingual Support** – Recognizes and responds in English, Kannada, and Hindi.
**Hand Gesture Recognition** – Perform actions like opening applications using predefined gestures.
**Facial Authentication** – Ensures secure access by verifying the user’s identity.



## 🔧 Tech Stack

**Python** – (version 3.9.10) Backend logic and processing.
**MediaPipe** – Hand gesture tracking.
**OpenCV** – Facial recognition and authentication.
**Eel** – Frontend integration for an app-like interface.
**SpeechRecognition & pyttsx3** – Voice input and response generation.


## 📂 Project Structure

| File/Folder    | Description |
|---------------|-------------|
| **main.py**    | Initializes the assistant and handles input. |
| **run.py**     | Starts the assistant with face authentication. |
| **backend/**   | Core logic for processing voice, face, and gestures. |
| **frontend/**  | Manages UI elements using the *Eel* library. |
| **mitra.db**   | Stores user-related data. |
| **_pycache_/** | Auto-generated Python cache files. |



## 🎤 Usage Guide

### *Voice Commands*
- "Open YouTube"
- "Search for AI advancements"
- "Tell me the time"

### *Hand Gestures*
| Gesture  | Action |
|----------|---------|
| 👍 (Thumbs Up)  | Opens Notepad |
| ✌ (V Sign)    | Opens Calculator |
| 👌 (OK Sign)   | Opens Browser |
| 👋 (Hello Sign) | Opens File Explorer |

### *Face Authentication*
- The system verifies the user before enabling assistant functionalities.
- Only registered users can access the assistant.

