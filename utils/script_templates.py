"""
Script templates and prompt generators for personal branding videos.
High engagement formats designed for LinkedIn, YouTube Shorts, Instagram Reels, and X (Twitter).
"""

BRANDING_CATEGORIES = {
    "🔥 Viral Hook & Contrarian Take": {
        "description": "Challenge conventional wisdom to instantly grab attention and drive comments.",
        "templates": [
            {
                "title": "Stop Doing X (Do Y Instead)",
                "hook": "Most people in {industry} are wasting 80% of their time on {bad_habit}.",
                "body": "Here is the uncomfortable truth: doing more of the same won't get you ahead. Instead, top 1% performers focus on one thing: {core_secret}. When I switched my strategy to this, my results 10x'd in under 30 days.",
                "cta": "Drop a comment if you agree, or tell me why I'm wrong. Let's debate."
            },
            {
                "title": "Unpopular Opinion",
                "hook": "Unpopular opinion: {popular_trend} is completely overrated.",
                "body": "Everyone tells you that you need {popular_trend} to succeed in {industry}. But after analyzing top winners, here is what actually moves the needle: {core_secret}. Keep it simple, execute ruthlessly, and ignore the noise.",
                "cta": "Share this with someone who needs to hear this today."
            }
        ]
    },
    "💡 3-Step Actionable Framework": {
        "description": "High-value tutorial format that positions you as a trusted subject matter expert.",
        "templates": [
            {
                "title": "The 3-Step Playbook",
                "hook": "Here is the exact 3-step playbook I use to master {industry} from scratch.",
                "body": "Step 1: Eliminate the clutter and lock in your primary target.\nStep 2: Automate your repetitive workflows with modern AI tools.\nStep 3: Measure outcomes obsessively every Friday.\nMaster these 3, and you'll outperform 95% of your competition.",
                "cta": "Save this video for later so you don't lose the framework."
            },
            {
                "title": "Zero to One Strategy",
                "hook": "If I lost everything and had to rebuild my {industry} brand from zero today, here is my day-one roadmap.",
                "body": "First, I'd pick a razor-sharp niche. Second, I'd build in public and publish daily video insights. Third, I'd network directly with 5 leaders every single morning. Consistency compounds faster than talent.",
                "cta": "Follow my profile for daily tactics on scaling your authority."
            }
        ]
    },
    "🚀 Founder Story & Behind The Scenes": {
        "description": "Build deep emotional connection and authentic trust through vulnerability and triumph.",
        "templates": [
            {
                "title": "The Turning Point",
                "hook": "Six months ago, I was ready to quit {industry}. Here is what changed everything.",
                "body": "I had hit a complete wall. Zero traction, endless burn. But then I realized my mistake: I was building for everyone instead of solving one urgent problem. The moment we focused on {core_secret}, everything clicked.",
                "cta": "What's the biggest lesson failure taught you? Tell me below."
            },
            {
                "title": "Building In Public",
                "hook": "We just hit a milestone I never thought was possible when starting out in {industry}.",
                "body": "Here's the raw truth no one talks about: success isn't a straight line. It's 100 days of unseen discipline, pivoting when things break, and staying obsessed with delivering value.",
                "cta": "Hit subscribe/follow to join the journey behind the scenes."
            }
        ]
    },
    "⚡ Quick Tech / AI Trend Breakdown": {
        "description": "Position yourself as an innovator riding modern tech waves.",
        "templates": [
            {
                "title": "AI Automation Advantage",
                "hook": "AI won't replace you in {industry}, but someone using AI will.",
                "body": "While others are debating the future, forward-thinking operators are already saving 15 hours a week using automated video and workflows. Here's your cue to start experimenting today.",
                "cta": "Type 'AI' in the comments and I'll send you my curated toolkit."
            }
        ]
    }
}

MOTION_PROMPT_PRESETS = [
    {
        "name": "👔 Confident Authority (Default)",
        "prompt": "Natural head nod, strong direct eye contact, subtle professional smile, confident thought leader posture, smooth micro-expressions."
    },
    {
        "name": "🔥 High-Energy Creator",
        "prompt": "Dynamic facial expressions, energetic eyebrow movements, frequent smiling, enthusiastic head tilt, vibrant engaging presenter."
    },
    {
        "name": "🧠 Thoughtful & Reflective",
        "prompt": "Slight introspective head tilts, gentle nodding, focused gaze, calm and measured facial expression, analytical mentor demeanor."
    },
    {
        "name": "🤝 Friendly & Conversational",
        "prompt": "Warm inviting smile, natural pauses, authentic conversational micro-expressions, approachable coach persona."
    }
]

def generate_custom_script(industry: str, topic: str, tone: str, category: str, secret: str = "") -> str:
    """Generate a cohesive personalized branding video script."""
    secret_val = secret if secret else f"mastering consistency and high-leverage workflows in {industry}"
    cat_data = BRANDING_CATEGORIES.get(category, list(BRANDING_CATEGORIES.values())[0])
    tpl = cat_data["templates"][0]
    
    hook = tpl["hook"].replace("{industry}", industry).replace("{bad_habit}", topic).replace("{popular_trend}", topic)
    body = tpl["body"].replace("{industry}", industry).replace("{core_secret}", secret_val).replace("{popular_trend}", topic)
    cta = tpl["cta"]
    
    return f"{hook}\n\n{body}\n\n{cta}"
