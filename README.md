# 🎬 OmniBrand AI — Automated Personal Branding Video Studio

> **Automate your personal branding for free.** Generate high-converting talking avatar videos from a portrait image, voice audio, and viral prompt scripts using a **Streamlit** frontend connected to an AI video generating model hosted on a **Google Colab Free T4 GPU**.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io)
[![Google Colab](https://img.shields.io/badge/Colab-Free%20T4%20GPU-F9AB00.svg)](https://colab.research.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Cloudflare Tunnel](https://img.shields.io/badge/Tunnel-Cloudflare%20Free-F38020.svg)](https://cloudflare.com)

---

## 📌 Table of Contents
- [Why OmniBrand AI?](#-why-omnibrand-ai)
- [System Architecture](#-system-architecture)
- [Core Features](#-core-features)
- [How It Works (Step-by-Step)](#-how-it-works-step-by-step)
- [Quick Start Guide](#-quick-start-guide)
  - [1. Local Streamlit App Setup](#1-local-streamlit-app-setup)
  - [2. Google Colab GPU Backend Setup](#2-google-colab-gpu-backend-setup)
- [Supported Formats & Models](#-supported-formats--models)
- [Viral Personal Branding Frameworks](#-viral-personal-branding-frameworks)
- [Repository Structure](#-repository-structure)
- [API Reference](#-api-reference)
- [License](#-license)

---

## 💡 Why OmniBrand AI?

Personal branding is the highest leverage asset for founders, engineers, and creators. However:
- Studio equipment and editing software cost thousands of dollars.
- Recording daily videos takes 2–4 hours of filming and multiple takes.
- Commercial AI video generation tools (HeyGen, Synthesia) charge expensive monthly subscriptions with strict minute limits.

**OmniBrand AI solves this 100% for free:**
1. **Zero Cloud Costs**: Uses Google Colab's free NVIDIA Tesla T4 GPU (15GB VRAM) for AI video rendering.
2. **Zero Speech Costs**: Uses Microsoft Neural Speech (`edge-tts`) for ultra-realistic voice synthesis with zero API keys.
3. **Zero Tunneling Subscriptions**: Uses Cloudflare Quick Tunnels (no account, token, or ngrok limits).
4. **End-to-End Automation**: From viral script generation to video rendering and multi-platform social media captions.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────┐
│              Streamlit Studio (Local Web UI)           │
│                                                        │
│  📸 Avatar Selection (Upload, Webcam, Preset Personas) │
│  🎙️ Neural Voice (Free Edge-TTS - 8+ Personas)        │
│  ✍️ Script Generator (Hooks, Contrarian, Frameworks)   │
│  📱 Multi-Aspect Ratio (9:16 Reels, 1:1, 16:9)         │
│  🚀 Social Media Copy Kit (LinkedIn, X, Instagram)     │
└───────────────────────────┬────────────────────────────┘
                            │
               REST API     ▼     Base64 MP4
  ┌─────────────────────────────────────────────────────┐
  │         Google Colab Cloud GPU Backend              │
  │                                                     │
  │  ⚡ NVIDIA Tesla T4 GPU (15GB VRAM — Free Tier)      │
  │  🧠 LivePortrait / SadTalker / Wav2Lip Model Engine │
  │  🌐 FastAPI Wrapper + Cloudflare Public Tunnel      │
  └─────────────────────────────────────────────────────┘
```

---

## ✨ Core Features

### 1. 📸 Avatar & Persona Selection
- **Preset Brand Personas**: Curated high-resolution studio portraits (Tech Founder, Creative Strategist, AI Innovator).
- **Custom Photo Upload**: Use any front-facing portrait of yourself (`.jpg`, `.png`, `.webp`).
- **Webcam Snapshot**: Capture a live portrait headshot directly inside your browser.

### 2. 🎙️ Voice & Audio Synthesis
- **Microsoft Neural Speech (Edge-TTS)**: Crystal clear, human-like voice synthesis with zero API keys or costs.
- **Voice Library**: Supports American, British, and Indian professional voices (*Christopher, Guy, Jenny, Aria, Ryan, Sonia, Prabhat, Neerja*).
- **Pace & Vocal Pitch Controls**: Customize speaking speed (-20% to +30%) and pitch.
- **Custom Voice Audio**: Upload your own pre-recorded voice clips or cloned voice audio (`.mp3`, `.wav`).

### 3. ✍️ Viral Script & Video Prompt Crafter
- **Framework Templates**:
  - *🔥 Viral Hook & Contrarian Take*: Designed for high engagement and comments.
  - *💡 3-Step Actionable Playbook*: Establishes domain authority.
  - *🚀 Founder Story & Turning Point*: Builds trust and authentic connection.
  - *⚡ Quick Tech / AI Trend Breakdown*: Positions you as a forward-thinking operator.
- **Body Language & Motion Prompts**: Choose between *Confident Authority*, *High-Energy Creator*, *Thoughtful Mentor*, or custom prompt instructions.
- **Duration Estimator**: Real-time word count and estimated speech duration counter.

### 4. 📱 Multi-Platform Aspect Ratio
- **`9:16` Vertical Reel**: Optimized for Instagram Reels, YouTube Shorts, and TikTok.
- **`1:1` Square Feed**: Tailored for LinkedIn Feed, Instagram Feed, and X/Twitter.
- **`16:9` Landscape**: Full widescreen for YouTube and website landing pages.

### 5. 🚀 Viral Brand Copy Kit
One-click generator for accompanying social media captions and hashtags:
- **LinkedIn Post**: Hook, algorithm-friendly formatting, and engagement question.
- **Twitter / X Thread / Post**: Concise 280-character post with engagement prompt.
- **Instagram / TikTok**: Trend-optimized caption with relevant hashtags.

### 6. 🧪 Local Preview & Offline Mode
If your Colab instance is idle or you want to draft content offline, the app features a bundled local video compositor (powered by `imageio-ffmpeg`) that generates playable, audio-synced preview MP4 videos with zero external dependencies.

---

## 🚀 Quick Start Guide

### 1. Local Streamlit App Setup

#### Prerequisites
- Python 3.10 or higher
- Git

#### Installation
```bash
# Clone the repository
git clone https://github.com/Ved-Dixit1/personal-branding.git
cd personal-branding

# Run the launcher (automatically sets up venv & installs dependencies)
chmod +x run.sh
./run.sh
```

Or install manually:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

---

### 2. Google Colab GPU Backend Setup

To offload heavy neural video rendering to a free NVIDIA Tesla T4 GPU:

1. Open [Google Colab](https://colab.research.google.com).
2. Click **File** > **Upload Notebook** and upload `colab_backend/brand_video_colab_backend.ipynb`.
3. In the Colab menu, make sure GPU is enabled:
   - Navigate to **Runtime** > **Change runtime type** > Select **T4 GPU** > Click **Save**.
4. Click **Runtime** > **Run All** (or run cells sequentially).
5. The final cell will start the FastAPI server, create a free Cloudflare tunnel, and print your public URL:
   ```text
   ============================================================
   🎉 SUCCESS! Your Colab Video API is live at:
   👉 https://xxxx-xxxx-xxxx.trycloudflare.com
   ============================================================
   ```
6. Copy that URL, paste it into the **Google Colab API URL** field in the left sidebar of the Streamlit Studio, and click **🔌 Ping Colab**.
7. The status badge will change to:
   > `● ONLINE: Tesla T4 (15.0 GB VRAM)`

---

## 🧠 Supported Formats & Models

| Model Pipeline | Strengths | Recommended Platform |
| :--- | :--- | :--- |
| **LivePortrait** | Ultra-realistic micro-expressions, rapid inference | 9:16 Vertical Reels & Shorts |
| **SadTalker** | 3D head pose control, expressive eye gaze | 1:1 LinkedIn & Square Feeds |
| **Wav2Lip** | Accurate lip synchronization | High-speed tutorials & quick tips |

---

## 📂 Repository Structure

```text
personal-branding/
├── app.py                             # Main Streamlit web application
├── requirements.txt                   # Core Python dependencies
├── run.sh                             # 1-click startup script
├── .gitignore                         # Git ignore rules
├── colab_backend/
│   ├── brand_video_colab_backend.ipynb# Ready-to-run Google Colab Notebook
│   ├── colab_server.py                # Standalone Colab FastAPI backend script
│   └── README_COLAB.md                # Colab GPU deployment instructions
├── utils/
│   ├── colab_client.py                # REST API wrapper & connection manager
│   ├── tts_engine.py                  # Free Microsoft Edge-TTS voice engine
│   ├── script_templates.py            # Viral personal branding frameworks
│   └── presets.py                     # Avatar presets & aspect ratio configs
└── assets/
    ├── founder_female.jpg             # High-res preset avatar
    └── creator_male.jpg               # High-res preset avatar
```

---

## 📡 API Reference (Colab FastAPI Backend)

The Colab backend exposes the following REST endpoints:

### `GET /health`
Returns GPU status and memory availability.
```json
{
  "status": "healthy",
  "colab_gpu_online": true,
  "gpu_device": "Tesla T4",
  "free_vram_gb": 14.75,
  "timestamp": 1729074000
}
```

### `POST /generate`
Generates a synchronized talking head video.

**Request Body (JSON):**
```json
{
  "avatar_base64": "<base64-encoded-image>",
  "audio_base64": "<base64-encoded-audio>",
  "prompt": "Natural head nod, strong direct eye contact, confident thought leader",
  "aspect_ratio": "9:16",
  "model_type": "liveportrait",
  "enhance_face": true
}
```

**Response Body (JSON):**
```json
{
  "status": "success",
  "task_id": "a1b2c3d4",
  "video_base64": "<base64-encoded-mp4>",
  "execution_time_seconds": 12.4
}
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing & Community

Pull requests and feature ideas are welcome! Feel free to open an issue to suggest new avatar styles, voice options, or branding script templates.
