"""
Preset configurations, avatar profiles, motion dynamics, and aspect ratios.
"""

import os
from typing import Dict, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

AVATAR_PRESETS: List[Dict[str, str]] = [
    {
        "id": "founder_female",
        "name": "Sarah | Tech Founder & Executive",
        "tag": "Authoritative & Polished",
        "recommended_voice": "en-US-JennyNeural",
        "image_path": os.path.join(ASSETS_DIR, "founder_female.jpg"),
        "default_motion": "Natural head nod, strong direct eye contact, subtle professional smile"
    },
    {
        "id": "creator_male",
        "name": "Alex | AI Strategist & Creator",
        "tag": "Dynamic & Energetic",
        "recommended_voice": "en-US-ChristopherNeural",
        "image_path": os.path.join(ASSETS_DIR, "creator_male.jpg"),
        "default_motion": "Dynamic facial expressions, energetic eyebrow movements, engaging presenter"
    }
]

ASPECT_RATIOS = {
    "📱 Vertical Reel / Short / TikTok (9:16)": {
        "width": 720,
        "height": 1280,
        "ratio_label": "9:16",
        "platforms": "Instagram Reels, YouTube Shorts, TikTok"
    },
    "💼 Square Feed Post (1:1)": {
        "width": 768,
        "height": 768,
        "ratio_label": "1:1",
        "platforms": "LinkedIn Feed, Instagram Feed, X/Twitter"
    },
    "🖥️ Landscape Thought Leadership (16:9)": {
        "width": 1280,
        "height": 720,
        "ratio_label": "16:9",
        "platforms": "YouTube Full Video, Website Landing Page, LinkedIn Video"
    }
}
