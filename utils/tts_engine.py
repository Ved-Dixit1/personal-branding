"""
Free Text-to-Speech Engine using Edge-TTS (Microsoft Neural Voices).
100% free, no API keys required, crystal clear voice quality for branding videos.
"""

import asyncio
import os
import tempfile
from typing import Dict, List, Optional

SUPPORTED_VOICES: List[Dict[str, str]] = [
    {
        "id": "en-US-ChristopherNeural",
        "name": "Christopher (US Male - Authoritative & Executive)",
        "gender": "Male",
        "locale": "en-US",
        "style": "Thought Leadership / Business"
    },
    {
        "id": "en-US-GuyNeural",
        "name": "Guy (US Male - Energetic & Casual Creator)",
        "gender": "Male",
        "locale": "en-US",
        "style": "Viral Hooks / Reels"
    },
    {
        "id": "en-US-JennyNeural",
        "name": "Jenny (US Female - Clear & Engaging)",
        "gender": "Female",
        "locale": "en-US",
        "style": "Tech & Storytelling"
    },
    {
        "id": "en-US-AriaNeural",
        "name": "Aria (US Female - Expressive & Polished)",
        "gender": "Female",
        "locale": "en-US",
        "style": "Executive Coach"
    },
    {
        "id": "en-GB-RyanNeural",
        "name": "Ryan (UK Male - Deep & Sophisticated)",
        "gender": "Male",
        "locale": "en-GB",
        "style": "Documentary / Luxury"
    },
    {
        "id": "en-GB-SoniaNeural",
        "name": "Sonia (UK Female - Articulate & Crisp)",
        "gender": "Female",
        "locale": "en-GB",
        "style": "Corporate Authority"
    },
    {
        "id": "en-IN-PrabhatNeural",
        "name": "Prabhat (India Male - Natural & Confident)",
        "gender": "Male",
        "locale": "en-IN",
        "style": "Global Tech Founder"
    },
    {
        "id": "en-IN-NeerjaNeural",
        "name": "Neerja (India Female - Warm & Professional)",
        "gender": "Female",
        "locale": "en-IN",
        "style": "Educator / Founder"
    }
]

async def _synthesize_async(text: str, voice: str, rate: str = "+0%", pitch: str = "+0Hz", output_path: Optional[str] = None) -> str:
    """Async generation using edge_tts Communicate."""
    import edge_tts
    
    if not output_path:
        fd, output_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)
    return output_path

def generate_voice_audio(text: str, voice_id: str = "en-US-ChristopherNeural", speed_pct: int = 0, pitch_hz: int = 0, output_path: Optional[str] = None) -> str:
    """Synchronous interface to generate high-fidelity speech audio file."""
    clean_text = text.strip()
    if not clean_text:
        raise ValueError("Script text cannot be empty.")
        
    rate_str = f"{'+' if speed_pct >= 0 else ''}{speed_pct}%"
    pitch_str = f"{'+' if pitch_hz >= 0 else ''}{pitch_hz}Hz"
    
    try:
        # Run in fresh event loop or existing loop safely
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        path = loop.run_until_complete(_synthesize_async(clean_text, voice_id, rate_str, pitch_str, output_path))
        loop.close()
        return path
    except Exception as e:
        # Fallback or re-raise
        raise RuntimeError(f"Edge-TTS generation failed: {str(e)}")
