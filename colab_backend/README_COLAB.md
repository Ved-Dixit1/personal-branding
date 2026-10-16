# ⚡ Google Colab GPU Backend Setup Guide

This guide allows you to run high-end AI Talking Avatar video models on **Google Colab's Free T4 GPU** and connect them directly to your Streamlit Personal Branding Studio.

---

## 🎯 How It Works

```
┌─────────────────────────────────┐               ┌─────────────────────────────────┐
│   Streamlit Local Studio        │  REST API     │   Google Colab (Free T4 GPU)    │
│  (UI, Avatars, Voice, Scripts)  ├──────────────►│  (FastAPI + LivePortrait/Model) │
│                                 │◄──────────────┤                                 │
│  Outputs 9:16 / 1:1 MP4 Videos  │  Base64 MP4   │  GPU-Accelerated Neural Render  │
└─────────────────────────────────┘               └─────────────────────────────────┘
```

---

## 🚀 3-Step Setup

### Step 1: Open Notebook in Google Colab
1. Go to [Google Colab](https://colab.research.google.com).
2. Click **File** > **Upload Notebook** and select `colab_backend/brand_video_colab_backend.ipynb`.
3. In the Colab menu, ensure GPU is active: **Runtime** > **Change runtime type** > Select **T4 GPU** > Save.

### Step 2: Run The Cells
- Execute **Step 1** (Check GPU).
- Execute **Step 2** (Install packages).
- Execute **Step 3** (Write server script).
- Execute **Step 4** (Run server with Cloudflare tunnel).
  - *Cloudflare tunnels are 100% free and require zero accounts or tokens.*

### Step 3: Copy Your Tunnel URL
You will see output like:
```text
🎉 SUCCESS! Your Colab Video API is live at:
👉 https://xxxx-xxxx-xxxx.trycloudflare.com
```

Copy that link, open your **Streamlit Studio**, and paste it into the **Google Colab Cloud GPU Bridge** section!

---

## 🛡️ Fallback & Offline Mode
If your Colab instance is not running or you want to draft content offline, the Streamlit app automatically switches to **Offline / Local Simulation Mode**, allowing you to test voices, avatar generation, and scripts instantly without waiting for Colab.
