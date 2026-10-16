"""
Colab GPU Backend API Client & Video Synthesis Pipeline
Seamlessly manages connection to Google Colab GPU wrapper,
with automatic fallback to local audio-visual compositing.
"""

import os
import time
import base64
import subprocess
import requests
from typing import Dict, Any, Optional, Callable

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def normalize_url(url: str) -> str:
    """Ensure clean URL format without trailing slash."""
    url = url.strip()
    if not url:
        return ""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url.rstrip("/")

def check_colab_connection(url: str, timeout: float = 6.0) -> Dict[str, Any]:
    """
    Ping the Google Colab backend to verify GPU readiness and latency.
    """
    clean_url = normalize_url(url)
    if not clean_url:
        return {
            "online": False,
            "latency_ms": 0,
            "device": "Offline",
            "vram": "0 GB",
            "message": "No Colab URL entered. App is running in Local Simulation Mode."
        }

    headers = {
        "User-Agent": "StreamlitPersonalBranding/1.0",
        "ngrok-skip-browser-warning": "69420",
        "bypass-tunnel-reminder": "true"
    }

    start = time.time()
    try:
        # Check /health or /
        target = f"{clean_url}/health"
        resp = requests.get(target, headers=headers, timeout=timeout)
        latency = round((time.time() - start) * 1000, 1)

        if resp.status_code == 200:
            data = resp.json()
            gpu_device = data.get("gpu_device", "Cloud GPU")
            free_vram = f"{data.get('free_vram_gb', 0)} GB"
            return {
                "online": True,
                "latency_ms": latency,
                "device": gpu_device,
                "vram": free_vram,
                "message": f"Connected to Google Colab ({gpu_device}) in {latency}ms"
            }
        else:
            return {
                "online": False,
                "latency_ms": latency,
                "device": "Error",
                "vram": "0 GB",
                "message": f"Server responded with HTTP {resp.status_code}"
            }
    except requests.exceptions.Timeout:
        return {
            "online": False,
            "latency_ms": round((time.time() - start) * 1000, 1),
            "device": "Timeout",
            "vram": "0 GB",
            "message": "Connection timed out. Check if your Colab cell is still executing."
        }
    except requests.exceptions.ConnectionError:
        return {
            "online": False,
            "latency_ms": 0,
            "device": "Unreachable",
            "vram": "0 GB",
            "message": "Cannot reach URL. Check if your Cloudflare/Ngrok tunnel URL has expired."
        }
    except Exception as e:
        return {
            "online": False,
            "latency_ms": 0,
            "device": "Error",
            "vram": "0 GB",
            "message": f"Connection check failed: {str(e)}"
        }

def render_local_preview_video(avatar_path: str, audio_path: str, aspect_ratio: str = "9:16", output_filename: Optional[str] = None) -> str:
    """
    Render video locally using bundled imageio-ffmpeg when Colab is offline.
    Provides instant offline testing with proper aspect ratio framing.
    """
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    if not output_filename:
        output_filename = f"branding_video_{int(time.time())}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Resolution & aspect ratio filter
    if aspect_ratio == "9:16":
        vf_filter = "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p"
    elif aspect_ratio == "1:1":
        vf_filter = "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p"
    else:  # 16:9
        vf_filter = "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p"

    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1",
        "-i", avatar_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-vf", vf_filter,
        "-shortest",
        output_path
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg render error: {res.stderr}")
    return output_path

def generate_video_via_colab(
    colab_url: str,
    avatar_path: str,
    audio_path: str,
    prompt: str = "",
    aspect_ratio: str = "9:16",
    model_type: str = "liveportrait",
    enhance_face: bool = True,
    timeout: float = 180.0
) -> str:
    """
    Submit job to Google Colab GPU backend and retrieve generated MP4 video.
    """
    clean_url = normalize_url(colab_url)
    if not clean_url:
        raise ValueError("Colab URL is required.")

    # Read binary files as base64
    with open(avatar_path, "rb") as img_f:
        avatar_b64 = base64.b64encode(img_f.read()).decode("utf-8")
    with open(audio_path, "rb") as aud_f:
        audio_b64 = base64.b64encode(aud_f.read()).decode("utf-8")

    payload = {
        "avatar_base64": avatar_b64,
        "audio_base64": audio_b64,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "model_type": model_type,
        "enhance_face": enhance_face
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "StreamlitPersonalBranding/1.0",
        "ngrok-skip-browser-warning": "69420"
    }

    target = f"{clean_url}/generate"
    resp = requests.post(target, json=payload, headers=headers, timeout=timeout)

    if resp.status_code != 200:
        raise RuntimeError(f"Colab GPU generation returned HTTP {resp.status_code}: {resp.text}")

    data = resp.json()
    video_b64 = data.get("video_base64")
    if not video_b64:
        raise RuntimeError("No video payload received from Colab backend.")

    video_bytes = base64.b64decode(video_b64)
    out_filename = f"colab_gpu_video_{int(time.time())}.mp4"
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    with open(out_path, "wb") as f:
        f.write(video_bytes)

    return out_path

def generate_social_copy(script_text: str, topic: str, industry: str) -> Dict[str, str]:
    """
    Generate viral social media posts and hashtags matching the generated video.
    """
    clean_script = script_text.strip()
    clean_topic = topic.strip() or "high performance"
    clean_ind = industry.strip() or "Tech & Business"

    first_line = clean_script.split("\n")[0] if clean_script else f"The biggest mistake in {clean_ind}."
    
    # LinkedIn post
    linkedin = (
        f"🎯 {first_line}\n\n"
        f"Most professionals in {clean_ind} overlook this fundamental reality.\n\n"
        f"In my latest video breakdown, I dive deep into why {clean_topic} changes the game and how you can apply it today.\n\n"
        f"Key takeaway: Consistency and strategic automation will always compound faster than raw hours.\n\n"
        f"👇 Watch the video above and let me know: What has been your experience with this?\n\n"
        f"#PersonalBranding #Leadership #{clean_ind.replace(' ', '')} #Innovation #FutureOfWork #AI"
    )

    # Twitter / X Post
    x_post = (
        f"🧵 {first_line}\n\n"
        f"Here's why focusing on {clean_topic} is the #1 lever for {clean_ind} this year (watch 30s breakdown 👆)\n\n"
        f"RT if you agree."
    )

    # Instagram / TikTok Reels
    reels = (
        f"Drop a '🔥' if you needed to hear this today!\n\n"
        f"Save this reel for when you need a reminder on mastering {clean_topic}.\n\n"
        f".\n.\n.\n"
        f"#viral #reels #personalbrand #founder #{clean_ind.replace(' ', '').lower()} #creator"
    )

    return {
        "linkedin": linkedin,
        "x_post": x_post,
        "reels": reels
    }
