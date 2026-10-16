"""
OmniBrand AI Studio - Streamlit Personal Branding Video Generator
Connected to Google Colab GPU Backend (FastAPI / LivePortrait / SadTalker / Cloudflare)
"""

import os
import time
import base64
import tempfile
import streamlit as st
from PIL import Image

from utils.script_templates import BRANDING_CATEGORIES, MOTION_PROMPT_PRESETS, generate_custom_script
from utils.tts_engine import SUPPORTED_VOICES, generate_voice_audio
from utils.presets import AVATAR_PRESETS, ASPECT_RATIOS
from utils.colab_client import (
    check_colab_connection,
    render_local_preview_video,
    generate_video_via_colab,
    generate_social_copy,
    normalize_url
)

# ---------------------------------------------------------
# Page Configuration & Modern Design Meta
# ---------------------------------------------------------
st.set_page_config(
    page_title="OmniBrand AI Studio | Avatar Video Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "colab_url" not in st.session_state:
    st.session_state.colab_url = ""
if "connection_status" not in st.session_state:
    st.session_state.connection_status = None
if "generated_audio_path" not in st.session_state:
    st.session_state.generated_audio_path = None
if "latest_video_path" not in st.session_state:
    st.session_state.latest_video_path = None
if "video_history" not in st.session_state:
    st.session_state.video_history = []
if "script_text" not in st.session_state:
    st.session_state.script_text = (
        "Most people in tech are wasting 80% of their time on manual tasks.\n\n"
        "Here is the uncomfortable truth: doing more of the same won't get you ahead. "
        "Top performers focus on one thing: automated video and content pipelines. "
        "When I switched my workflow, my inbound reach 10x'd in under 30 days.\n\n"
        "Drop a comment if you agree, or tell me your strategy below."
    )
if "topic_input" not in st.session_state:
    st.session_state.topic_input = "AI automation workflows"
if "industry_input" not in st.session_state:
    st.session_state.industry_input = "Tech & Startups"

# ---------------------------------------------------------
# Custom Modern Dark-Themed Styling (CSS Injection)
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Modern typography import */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Background gradient styling */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 1) 0%, rgba(9, 14, 26, 1) 90%);
    color: #f8fafc;
}

/* Hero Title & Branding Header */
.brand-header-box {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 24px 32px;
    margin-bottom: 24px;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
}

.brand-title {
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #60a5fa 0%, #a855f7 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    padding-bottom: 4px;
}

.brand-subtitle {
    color: #cbd5e1;
    font-size: 1.05rem;
    margin-top: 6px;
    font-weight: 400;
}

/* Pill status tags */
.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 600;
}
.badge-online {
    background: rgba(16, 185, 129, 0.2);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.4);
}
.badge-offline {
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.4);
}
.badge-info {
    background: rgba(99, 102, 241, 0.2);
    color: #a5b4fc;
    border: 1px solid rgba(99, 102, 241, 0.4);
}

/* Glassmorphism Section Cards */
.glass-card {
    background: rgba(30, 41, 59, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
    transition: all 0.25s ease-in-out;
}
.glass-card:hover {
    border-color: rgba(168, 85, 247, 0.45);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
}

.card-title {
    font-size: 1.18rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* High Contrast Input Fields and Text Areas */
.stTextArea textarea, .stTextInput input {
    background-color: #0f172a !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3) !important;
}

/* Primary Action Buttons */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    padding: 12px 28px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 16px rgba(139, 92, 246, 0.45) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
div.stButton > button:first-child:hover {
    box-shadow: 0 6px 24px rgba(139, 92, 246, 0.7) !important;
    transform: translateY(-2px) !important;
}

/* High Contrast Download Buttons */
div.stDownloadButton > button:first-child {
    background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35) !important;
    transition: all 0.2s ease !important;
}
div.stDownloadButton > button:first-child:hover {
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6) !important;
    transform: translateY(-1px) !important;
}

/* Code & monospace blocks */
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    color: #38bdf8 !important;
    background-color: rgba(15, 23, 42, 0.8) !important;
}

/* Tab navigation style */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(15, 23, 42, 0.75);
    padding: 8px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #94a3b8;
    font-weight: 600;
    padding: 10px 22px;
}
.stTabs [aria-selected="true"] {
    background: rgba(99, 102, 241, 0.3) !important;
    color: #ffffff !important;
    border-bottom: 2px solid #8b5cf6 !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar: Cloud GPU Bridge & Settings
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Colab GPU Bridge")
    st.caption("Connect your free Google Colab T4 GPU instance to render AI video models.")

    colab_input = st.text_input(
        "Google Colab API URL",
        value=st.session_state.colab_url,
        placeholder="https://xxxx-xxxx.trycloudflare.com",
        help="Paste the public URL generated from your Google Colab notebook cell."
    )
    if colab_input != st.session_state.colab_url:
        st.session_state.colab_url = colab_input
        st.session_state.connection_status = None

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("🔌 Ping Colab", use_container_width=True):
            with st.spinner("Pinging Colab GPU..."):
                status = check_colab_connection(st.session_state.colab_url)
                st.session_state.connection_status = status
    with col_btn2:
        use_simulation = st.checkbox("Local Preview Mode", value=not bool(st.session_state.colab_url), help="Generate instant video preview locally without Colab GPU.")

    # Status Display
    if st.session_state.connection_status:
        c_stat = st.session_state.connection_status
        if c_stat["online"]:
            st.markdown(f'<div class="badge-pill badge-online">● ONLINE: {c_stat["device"]} ({c_stat["latency_ms"]}ms)</div>', unsafe_allow_html=True)
            st.caption(f"Free VRAM: {c_stat['vram']}")
        else:
            st.markdown(f'<div class="badge-pill badge-offline">○ {c_stat["message"]}</div>', unsafe_allow_html=True)
    elif not st.session_state.colab_url:
        st.markdown('<div class="badge-pill badge-info">💡 Offline Preview Active</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📐 Video Layout & Aspect")
    aspect_choice = st.selectbox(
        "Target Platform Format",
        options=list(ASPECT_RATIOS.keys()),
        index=0
    )
    selected_aspect = ASPECT_RATIOS[aspect_choice]["ratio_label"]
    st.caption(f"Optimized for: {ASPECT_RATIOS[aspect_choice]['platforms']}")

    st.markdown("---")
    st.markdown("### 🧠 AI Video Model")
    model_choice = st.selectbox(
        "Animation Pipeline",
        ["LivePortrait (Fast & Ultra-Realistic)", "SadTalker (3D Neural Head)", "Wav2Lip (Accurate Lip-Sync)"],
        index=0
    )
    enhance_face = st.toggle("Enhance Facial Details (GFPGAN)", value=True)

    st.markdown("---")
    st.markdown("### 💡 Cost & Quota")
    col_c1, col_c2 = st.columns(2)
    col_c1.metric("Cloud Cost", "$0.00", "100% Free")
    col_c2.metric("GPU Model", "Tesla T4", "Colab Free")

# ---------------------------------------------------------
# Top Header
# ---------------------------------------------------------
status_badge_html = (
    '<span class="badge-pill badge-online">● Colab GPU Connected</span>'
    if (st.session_state.connection_status and st.session_state.connection_status["online"])
    else '<span class="badge-pill badge-info">🧪 Instant Local Preview Mode</span>'
)

st.markdown(f"""
<div class="brand-header-box">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div>
            <h1 class="brand-title">🎬 OmniBrand AI Video Studio</h1>
            <div class="brand-subtitle">Automate your personal branding with AI talking avatars, neural voice, and Colab GPU rendering.</div>
        </div>
        <div>
            {status_badge_html}
            <span class="badge-pill badge-info" style="margin-left:8px;">🎙️ Edge-TTS Free Neural Voice</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Main Tabs
# ---------------------------------------------------------
tab_studio, tab_viral_kit, tab_colab_guide, tab_history = st.tabs([
    "🎬 Video Creation Studio",
    "🚀 Viral Brand Copy Kit",
    "⚡ Google Colab Setup Guide",
    "📂 Video Archive & History"
])

# =========================================================
# TAB 1: VIDEO STUDIO
# =========================================================
with tab_studio:
    col_left, col_mid, col_right = st.columns([1, 1.2, 1.3], gap="medium")

    # -----------------------------------------------------
    # COLUMN 1: AVATAR SELECTION
    # -----------------------------------------------------
    with col_left:
        st.markdown('<div class="card-title">1️⃣ Avatar & Persona</div>', unsafe_allow_html=True)
        avatar_source = st.radio(
            "Select Avatar Source",
            ["Preset Branding Avatars", "Upload Custom Photo", "Webcam Capture"],
            horizontal=True
        )

        chosen_avatar_path = None
        recommended_voice = "en-US-ChristopherNeural"

        if avatar_source == "Preset Branding Avatars":
            preset_names = [f"{p['name']} ({p['tag']})" for p in AVATAR_PRESETS]
            selected_preset_idx = st.selectbox(
                "Choose AI Persona",
                range(len(AVATAR_PRESETS)),
                format_func=lambda i: preset_names[i]
            )
            preset_data = AVATAR_PRESETS[selected_preset_idx]
            chosen_avatar_path = preset_data["image_path"]
            recommended_voice = preset_data["recommended_voice"]

            if os.path.exists(chosen_avatar_path):
                img = Image.open(chosen_avatar_path)
                st.image(img, caption=f"Active Avatar: {preset_data['name']}", use_container_width=True)
            else:
                st.warning("Preset avatar not found in assets.")

        elif avatar_source == "Upload Custom Photo":
            uploaded_img = st.file_uploader("Upload Portrait (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])
            if uploaded_img is not None:
                tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                tmp_img.write(uploaded_img.read())
                tmp_img.close()
                chosen_avatar_path = tmp_img.name
                st.image(chosen_avatar_path, caption="Uploaded Portrait Avatar", use_container_width=True)
            else:
                st.info("Upload a clear, front-facing headshot for best animation results.")
                chosen_avatar_path = AVATAR_PRESETS[0]["image_path"]

        else: # Webcam Capture
            cam_pic = st.camera_input("Take Live Portrait Headshot")
            if cam_pic is not None:
                tmp_cam = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                tmp_cam.write(cam_pic.read())
                tmp_cam.close()
                chosen_avatar_path = tmp_cam.name
                st.image(chosen_avatar_path, caption="Webcam Headshot", use_container_width=True)
            else:
                chosen_avatar_path = AVATAR_PRESETS[0]["image_path"]

    # -----------------------------------------------------
    # COLUMN 2: VOICE & AUDIO SYNTHESIS
    # -----------------------------------------------------
    with col_mid:
        st.markdown('<div class="card-title">2️⃣ Voice & Audio Track</div>', unsafe_allow_html=True)
        audio_mode = st.radio(
            "Audio Input Method",
            ["Free AI Neural Speech (Edge-TTS)", "Upload Custom Audio (MP3/WAV)"],
            horizontal=True
        )

        final_audio_path = st.session_state.generated_audio_path

        if audio_mode == "Free AI Neural Speech (Edge-TTS)":
            voice_names = [f"{v['name']} - {v['style']}" for v in SUPPORTED_VOICES]
            
            # Find index of recommended voice
            default_voice_idx = 0
            for idx, v in enumerate(SUPPORTED_VOICES):
                if v["id"] == recommended_voice:
                    default_voice_idx = idx
                    break

            selected_voice_idx = st.selectbox(
                "Voice Persona",
                range(len(SUPPORTED_VOICES)),
                index=default_voice_idx,
                format_func=lambda i: voice_names[i]
            )
            selected_voice_id = SUPPORTED_VOICES[selected_voice_idx]["id"]

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                speed_mod = st.slider("Speech Pace", min_value=-20, max_value=30, value=5, step=5, format="%d%%")
            with col_s2:
                pitch_mod = st.slider("Vocal Pitch", min_value=-15, max_value=15, value=0, step=1, format="%dHz")

            st.caption("⚡ Powered by Microsoft Neural Speech (100% Free, Zero API Key Required).")

            if st.button("🔊 Synthesize & Preview Voice", use_container_width=True):
                with st.spinner("Synthesizing neural speech audio..."):
                    try:
                        audio_path = generate_voice_audio(
                            text=st.session_state.script_text,
                            voice_id=selected_voice_id,
                            speed_pct=speed_mod,
                            pitch_hz=pitch_mod
                        )
                        st.session_state.generated_audio_path = audio_path
                        final_audio_path = audio_path
                        st.success("Audio synthesized successfully!")
                    except Exception as err:
                        st.error(f"Speech generation error: {err}")

            if st.session_state.generated_audio_path and os.path.exists(st.session_state.generated_audio_path):
                st.audio(st.session_state.generated_audio_path, format="audio/mp3")

        else: # Upload Custom Audio
            custom_audio = st.file_uploader("Upload Voice File", type=["mp3", "wav", "m4a", "ogg"])
            if custom_audio is not None:
                tmp_aud = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tmp_aud.write(custom_audio.read())
                tmp_aud.close()
                st.session_state.generated_audio_path = tmp_aud.name
                final_audio_path = tmp_aud.name
                st.audio(final_audio_path)
            else:
                st.info("Upload your pre-recorded voice note or cloned voice audio.")

    # -----------------------------------------------------
    # COLUMN 3: SCRIPT & VIDEO PROMPT CRAFTER
    # -----------------------------------------------------
    with col_right:
        st.markdown('<div class="card-title">3️⃣ Script & Motion Prompts</div>', unsafe_allow_html=True)
        
        # Template helper expander
        with st.expander("✨ Viral Personal Branding Script Generator", expanded=False):
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                t_ind = st.text_input("Your Industry/Niche", value=st.session_state.industry_input)
            with col_t2:
                t_top = st.text_input("Core Topic/Pain Point", value=st.session_state.topic_input)

            cat_names = list(BRANDING_CATEGORIES.keys())
            sel_cat = st.selectbox("Format", cat_names)

            if st.button("🪄 Fill Template Into Script"):
                st.session_state.industry_input = t_ind
                st.session_state.topic_input = t_top
                generated_script = generate_custom_script(t_ind, t_top, "authoritative", sel_cat)
                st.session_state.script_text = generated_script
                st.rerun()

        # Script textarea
        script_val = st.text_area(
            "Video Script (What the avatar speaks)",
            value=st.session_state.script_text,
            height=140,
            help="Type or paste the speech script. The avatar's lips and facial expressions will synchronize to this."
        )
        if script_val != st.session_state.script_text:
            st.session_state.script_text = script_val

        # Character and duration estimate
        word_count = len(st.session_state.script_text.split())
        est_duration_sec = round(word_count / 2.5)  # ~150 words per minute
        st.caption(f"📝 {word_count} words | Estimated Duration: ~{est_duration_sec}s | Platform: {selected_aspect}")

        # Motion prompt preset
        motion_names = [p["name"] for p in MOTION_PROMPT_PRESETS]
        chosen_motion_idx = st.selectbox(
            "Avatar Emotion & Body Language",
            range(len(MOTION_PROMPT_PRESETS)),
            format_func=lambda i: motion_names[i]
        )
        custom_motion_prompt = st.text_input(
            "Video Motion Prompt Details",
            value=MOTION_PROMPT_PRESETS[chosen_motion_idx]["prompt"]
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # -------------------------------------------------
        # GENERATE BUTTON & RENDERING PIPELINE
        # -------------------------------------------------
        generate_clicked = st.button("🚀 Render Personal Branding Video", use_container_width=True)

        if generate_clicked:
            if not chosen_avatar_path or not os.path.exists(chosen_avatar_path):
                st.error("Please select or upload an avatar image first.")
            elif not st.session_state.script_text.strip():
                st.error("Please enter a speech script.")
            else:
                progress_placeholder = st.empty()
                progress_bar = st.progress(0)

                # Ensure audio is generated
                if not st.session_state.generated_audio_path or not os.path.exists(st.session_state.generated_audio_path):
                    progress_placeholder.info("🎙️ Synthesizing neural speech audio track...")
                    progress_bar.progress(20)
                    try:
                        voice_id_to_use = selected_voice_id if 'selected_voice_id' in locals() else "en-US-ChristopherNeural"
                        audio_p = generate_voice_audio(st.session_state.script_text, voice_id=voice_id_to_use)
                        st.session_state.generated_audio_path = audio_p
                    except Exception as ex:
                        st.error(f"Error creating voice audio: {ex}")
                        st.stop()

                # Check if Colab is used or local preview
                colab_online = False
                if st.session_state.colab_url and not use_simulation:
                    progress_placeholder.info("⚡ Pinging Google Colab GPU backend...")
                    progress_bar.progress(35)
                    colab_check = check_colab_connection(st.session_state.colab_url)
                    colab_online = colab_check.get("online", False)

                try:
                    if colab_online:
                        progress_placeholder.info(f"🚀 Offloading rendering to Colab GPU ({model_choice})...")
                        progress_bar.progress(60)
                        
                        m_type = "liveportrait" if "LivePortrait" in model_choice else ("sadtalker" if "SadTalker" in model_choice else "wav2lip")
                        out_video = generate_video_via_colab(
                            colab_url=st.session_state.colab_url,
                            avatar_path=chosen_avatar_path,
                            audio_path=st.session_state.generated_audio_path,
                            prompt=custom_motion_prompt,
                            aspect_ratio=selected_aspect,
                            model_type=m_type,
                            enhance_face=enhance_face
                        )
                    else:
                        mode_msg = "🧪 Local Simulation Mode" if use_simulation else "⚠️ Colab unreachable. Falling back to local video renderer"
                        progress_placeholder.info(f"{mode_msg}: Compositing {selected_aspect} video with synced audio track...")
                        progress_bar.progress(60)
                        
                        out_video = render_local_preview_video(
                            avatar_path=chosen_avatar_path,
                            audio_path=st.session_state.generated_audio_path,
                            aspect_ratio=selected_aspect
                        )

                    progress_bar.progress(100)
                    progress_placeholder.success("🎉 Video rendered successfully!")
                    st.session_state.latest_video_path = out_video
                    st.session_state.video_history.insert(0, {
                        "video_path": out_video,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "script": st.session_state.script_text[:120] + "...",
                        "aspect": selected_aspect,
                        "mode": "Colab GPU" if colab_online else "Local Render"
                    })
                except Exception as err:
                    progress_placeholder.error(f"Render failed: {str(err)}")

    # -----------------------------------------------------
    # OUTPUT VIDEO PREVIEW SECTION
    # -----------------------------------------------------
    if st.session_state.latest_video_path and os.path.exists(st.session_state.latest_video_path):
        st.markdown("---")
        st.markdown("### 🎬 Generated Personal Branding Video")
        
        v_col1, v_col2 = st.columns([1.5, 1], gap="large")
        with v_col1:
            st.video(st.session_state.latest_video_path)
            with open(st.session_state.latest_video_path, "rb") as vf:
                st.download_button(
                    label="⬇️ Download High-Res MP4 Video",
                    data=vf.read(),
                    file_name=os.path.basename(st.session_state.latest_video_path),
                    mime="video/mp4",
                    use_container_width=True
                )
        with v_col2:
            st.markdown("#### 🎯 Video Meta & Quality")
            st.markdown(f"- **Format:** `{selected_aspect}` ({aspect_choice.split()[0]})")
            st.markdown(f"- **Audio Engine:** Microsoft Neural (`{recommended_voice}`)")
            st.markdown(f"- **Motion Prompt:** *\"{custom_motion_prompt[:80]}...\"*")
            st.markdown(f"- **Local File:** `{os.path.basename(st.session_state.latest_video_path)}`")
            st.info("💡 Next Step: Check the **'🚀 Viral Brand Copy Kit'** tab for ready-to-paste LinkedIn, X, and Instagram captions!")

# =========================================================
# TAB 2: VIRAL BRAND COPY KIT
# =========================================================
with tab_viral_kit:
    st.markdown('<div class="card-title">📱 Viral Post & Caption Copywriter</div>', unsafe_allow_html=True)
    st.caption("AI-generated social media posts and hashtags tailored to accompany your generated video.")

    copy_data = generate_social_copy(
        script_text=st.session_state.script_text,
        topic=st.session_state.topic_input,
        industry=st.session_state.industry_input
    )

    c_tab1, c_tab2, c_tab3 = st.tabs(["💼 LinkedIn Post", "🐦 Twitter / X Thread", "📸 Instagram & Reels"])
    with c_tab1:
        st.text_area("LinkedIn Post (Optimized for algorithm reach & comments)", value=copy_data["linkedin"], height=240)
        st.caption("Tip: Add the video as a native document or MP4 upload for 3x organic reach on LinkedIn.")
    with c_tab2:
        st.text_area("X / Twitter Post", value=copy_data["x_post"], height=160)
    with c_tab3:
        st.text_area("Instagram / TikTok Caption & Hashtags", value=copy_data["reels"], height=200)

# =========================================================
# TAB 3: GOOGLE COLAB SETUP GUIDE
# =========================================================
with tab_colab_guide:
    st.markdown('<div class="card-title">⚡ How to Run On Free Google Colab GPU</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Google Colab gives you **free access to an NVIDIA Tesla T4 GPU (15GB VRAM)**. 
    By running our pre-configured backend in Colab, all heavy AI video generation happens in the cloud for free!
    """)

    col_g1, col_g2 = st.columns([1, 1], gap="medium")
    with col_g1:
        st.markdown("""
        ### 📋 3 Easy Steps:
        
        1. **Download the Notebook**:
           Click the download button on the right to get `brand_video_colab_backend.ipynb`.
        
        2. **Open in Google Colab**:
           Go to [colab.research.google.com](https://colab.research.google.com), upload the notebook, and ensure GPU is selected (`Runtime > Change runtime type > T4 GPU`).
        
        3. **Run All Cells & Copy Tunnel URL**:
           Run the cells. The last cell prints a free public tunnel URL:
           ```text
           👉 https://xxxx-xxxx.trycloudflare.com
           ```
           Paste that link in the left sidebar of this app under **Google Colab API URL**, and you're connected!
        """)

    with col_g2:
        st.markdown("### 📥 Download Colab Notebook")
        notebook_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "colab_backend", "brand_video_colab_backend.ipynb")
        if os.path.exists(notebook_path):
            with open(notebook_path, "rb") as nbf:
                st.download_button(
                    label="⬇️ Download brand_video_colab_backend.ipynb",
                    data=nbf.read(),
                    file_name="brand_video_colab_backend.ipynb",
                    mime="application/x-ipynb+json",
                    use_container_width=True
                )
        
        st.markdown("### 💡 Why Free Cloudflare Tunnels?")
        st.markdown("""
        Unlike Ngrok which requires account signups and tokens, **Cloudflare Quick Tunnels** are 100% free, require zero signup, zero API tokens, and generate clean HTTPS endpoints directly from Google Colab.
        """)

# =========================================================
# TAB 4: VIDEO ARCHIVE & HISTORY
# =========================================================
with tab_history:
    st.markdown('<div class="card-title">📂 Video Archive & Library</div>', unsafe_allow_html=True)
    if not st.session_state.video_history:
        st.info("No videos generated in this session yet. Go to the Video Creation Studio to create your first personal branding video!")
    else:
        for idx, item in enumerate(st.session_state.video_history):
            with st.container():
                st.markdown(f"#### Video #{len(st.session_state.video_history) - idx} - {item['timestamp']}")
                h_col1, h_col2 = st.columns([1, 2])
                with h_col1:
                    if os.path.exists(item["video_path"]):
                        st.video(item["video_path"])
                with h_col2:
                    st.markdown(f"**Format:** `{item['aspect']}` | **Engine:** `{item['mode']}`")
                    st.markdown(f"**Script Snippet:** *\"{item['script']}\"*")
                    if os.path.exists(item["video_path"]):
                        with open(item["video_path"], "rb") as hf:
                            st.download_button(
                                label="⬇️ Download MP4",
                                data=hf.read(),
                                file_name=f"brand_video_{idx}.mp4",
                                mime="video/mp4",
                                key=f"dl_hist_{idx}"
                            )
                st.markdown("---")
