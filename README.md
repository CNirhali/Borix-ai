# Borix Order MVP 🚀

Borix is an AI-powered SaaS tool explicitly built to eliminate chaotic workflows for small and medium-sized businesses (SMBs). This repository contains the MVP ("Stage 1 Development") for **Borix Order**, demonstrating how unstructured, native-language chats (like WhatsApp or Instagram DMs) can be instantly interpreted and converted into structured queue items for a Merchant Point-of-Sale (POS) or Kitchen Display.

## Features

- **Split-Pane Realistic Demo:**
  - **Customer Chat Simulator:** A responsive chat UI where users can type orders using casual slang (e.g., *"bhai 2 cold coffee aur 1 sandwich parcel dena"*).
  - **Merchant POS Dashboard:** A live-updating grid tracking queue status, active orders, and calculated item totals.
- **Intelligent NLP Engine (Mocked MVP):** The backend actively extracts intent, recognizes items (like Cold Coffee and Sandwiches), aggregates quantities, and generates structured order objects.
- **Micro-Animations & Premium UI:** The frontend is built entirely using vanilla tech (HTML/CSS/JS) but utilizes modern design systems (glassmorphism, vibrant syntax, smooth transitions) for an incredibly premium feel.
- **Media Converter Engine (`converter.py`):** A custom built-in script designed to easily convert animated `.webp` screen recordings into `.mp4` videos, `.gif` files, or `.png` thumbnails for sharing demos on social media platforms like LinkedIn.

## Technology Stack

- **Backend:** Python + FastAPI 
- **Frontend:** Vanilla HTML5, CSS3, JavaScript
- **Utilities:** Python's Pillow, imageio, and numpy for media conversion

## Installation & Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CNirhali/Borix-ai.git
   cd Borix.Ai
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI Server:**
   ```bash
   python -m uvicorn main:app --port 8085
   ```

4. **View the live app:**
   Open your browser and navigate to `http://127.0.0.1:8085`. Try chatting in the customer UI on the left!

## Using the Built-In Media Converter

If you capture a demo of Borix using a `.webp` screen recruiter, LinkedIn and other platforms often do not natively play it. You can use the included `converter.py` to fix this!

Convert to MP4 (Best for LinkedIn/Twitter):
```bash
python converter.py demo_recording.webp output.mp4
```

Convert to GIF:
```bash
python converter.py demo_recording.webp output.gif
```

Extract the first frame as a high-quality PNG thumbnail:
```bash
python converter.py demo_recording.webp thumbnail.png
```

---

*This project was completed automatically by an Agentic Coding Assistant during early stage scaffolding.*
