import streamlit as st
from openai import OpenAI

# ------------- OPENAI CLIENT -------------
# Make sure OPENAI_API_KEY is set in env or Streamlit secrets
# e.g. st.secrets["OPENAI_API_KEY"] if deploying
client = OpenAI()


# ------------- PAGE CONFIG + GLOBAL STYLE -------------
st.set_page_config(page_title="Social Media Agent AI", layout="wide")

st.markdown(
    """
<style>
/* Background gradient */
.main {
    background: radial-gradient(circle at top left, #ffe0f2 0, #ffffff 40%, #e3f2ff 100%);
}

/* Global font */
html, body, [class*="css"] {
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #020617);
    color: #e5e7eb;
}
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3, 
section[data-testid="stSidebar"] p {
    color: #e5e7eb;
}

/* Brand title */
.hero-title {
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 0;
    background: linear-gradient(90deg,#ec4899,#8b5cf6,#0ea5e9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Hero subtitle */
.hero-sub {
    font-size: 16px;
    color: #4b5563;
}

/* Gradient info bar */
.hero-bar {
    padding: 14px 18px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(90deg,rgba(236,72,153,0.12),rgba(59,130,246,0.12));
    border: 1px solid rgba(236,72,153,0.35);
    font-size: 13px;
    margin-bottom: 16px;
}

/* Card container */
.card {
    background: #ffffffcc;
    border-radius: 18px;
    padding: 22px 22px 18px 22px;
    box-shadow: 0 18px 45px rgba(15,23,42,0.12);
    border: 1px solid #e5e7eb;
}

/* Section headings */
h2, h3 {
    font-weight: 700;
    color: #111827;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#ec4899,#8b5cf6);
    color: white;
    border-radius: 999px;
    padding: 0.6rem 1.6rem;
    border: none;
    font-weight: 600;
    font-size: 15px;
}
.stButton>button:hover {
    background: linear-gradient(90deg,#f97316,#ec4899);
}

/* Text area & inputs */
textarea, input, select {
    border-radius: 10px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 999px;
    padding: 8px 18px;
    background-color: #f3f4f6;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg,#ec4899,#8b5cf6) !important;
    color: #ffffff !important;
}

/* Code block */
code {
    font-size: 13px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------- SIDEBAR -------------
with st.sidebar:
    st.markdown("### 🎛 Social Studio")
    st.markdown(
        "Your mini **content studio** for planning posts, captions, hooks & hashtags "
        "for Instagram, LinkedIn & YouTube Shorts."
    )
    st.markdown("---")
    st.markdown("**Tips for best results:**")
    st.markdown(
        """
- Be specific in *Niche* & *Audience*  
- Choose a tone that matches your brand  
- Use the same brand details for both tabs  
        """
    )
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit + OpenAI")


# ------------- HERO SECTION -------------
st.markdown(
    '<div class="hero-bar">⚡ Social Media Content Studio · AI-powered planning & copy</div>',
    unsafe_allow_html=True,
)

st.markdown('<h1 class="hero-title">Social Media Agent AI</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Plan a full month of posts, generate high-performing captions, '
    "and stay consistent across platforms — in minutes.</p>",
    unsafe_allow_html=True,
)

st.write("")  # small spacer

# ------------- BRAND INPUTS (TOP AREA) -------------
with st.container():
    col_a, col_b = st.columns([2, 1.4])

    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🧩 Brand Profile")

        c1, c2 = st.columns(2)
        with c1:
            brand = st.text_input("Brand Name", placeholder="Delightlyf Wellness Retreats")
            niche = st.text_input(
                "Niche / Category", placeholder="Wellness, eco-tourism, managed farmland"
            )
        with c2:
            audience = st.text_input(
                "Target Audience",
                placeholder="Working professionals from Bangalore seeking nature + passive income",
            )
            tone = st.selectbox(
                "Tone of Voice",
                ["Professional", "Casual", "Fun", "Luxury", "Motivational", "Emotional"],
                index=3,
            )

        platform = st.selectbox(
            "Primary Platform",
            ["Instagram", "LinkedIn", "YouTube Shorts"],
            index=0,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📌 Brand Snapshot")
        if brand:
            st.markdown(f"**Brand:** {brand}")
        else:
            st.markdown("**Brand:** _Not set yet_")

        st.markdown(f"**Niche:** {niche or '_Not set_'}")
        st.markdown(f"**Audience:** {audience or '_Not set_'}")
        st.markdown(f"**Tone:** {tone}")
        st.markdown(f"**Platform:** {platform}")
        st.markdown("</div>", unsafe_allow_html=True)

st.write("")  # spacing

# Make sure session_state keys exist
if "plan" not in st.session_state:
    st.session_state["plan"] = ""
if "caption" not in st.session_state:
    st.session_state["caption"] = ""

# ------------- TABS: PLANNER & CAPTION STUDIO -------------
planner_tab, caption_tab = st.tabs(["📅 Content Planner", "✍️ Caption Studio"])

# ===== TAB 1: CONTENT PLANNER =====
with planner_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("30-Day Content Calendar")

    st.caption(
        "Generate a full month of content ideas with post types tailored to your brand & platform."
    )

    planner_col1, planner_col2 = st.columns([1, 1])

    with planner_col1:
        if st.button("✨ Generate 30-Day Content Plan", use_container_width=True):
            if not brand or not niche or not audience:
                st.warning("Please fill Brand Name, Niche and Audience before generating.")
            else:
                with st.spinner("Thinking like a social media strategist..."):
                    plan_prompt = f"""
                    You are a senior social media strategist.

                    Brand: {brand}
                    Niche: {niche}
                    Target audience: {audience}
                    Tone of voice: {tone}
                    Primary platform: {platform}

                    Create a 30-day content calendar.

                    For each day 1–30, provide:
                    - Day number
                    - Post Type (Reel, Carousel, Static image, LinkedIn post, YT Short, etc.)
                    - 1–2 line content idea that fits the brand, audience, and tone.

                    Focus on variety (education, storytelling, proof, behind-the-scenes, offers, FAQs, objections).
                    Return as a nicely formatted list.
                    """

                    try:
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": plan_prompt}],
                        )
                        st.session_state["plan"] = (
                            response.choices[0].message.content.strip()
                        )
                    except Exception as e:
                        st.error(f"Error generating plan: {e}")

    with planner_col2:
        st.info(
            "💡 *Pro tip:* Re-run this planner with different tones (Fun vs Luxury) "
            "to get alternate content calendars."
        )

    st.write("### 📘 Your 30-Day Plan")
    if st.session_state["plan"]:
        st.markdown(st.session_state["plan"])
    else:
        st.write("_No plan generated yet. Click the button above to create one._")

    st.markdown("</div>", unsafe_allow_html=True)

# ===== TAB 2: CAPTION STUDIO =====
with caption_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("AI Caption & Hashtag Studio")

    st.caption(
        "Paste any idea from your content calendar (or type a new one) and let the agent turn it into a full post."
    )

    idea = st.text_area(
        "Post Idea",
        placeholder="Ex: Weekend detox retreat at our eco-luxury cottages for stressed IT professionals.",
        height=110,
    )

    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        length_choice = st.selectbox(
            "Caption Length",
            ["Short (60–80 words)", "Standard (100–140 words)", "Long (150–220 words)"],
            index=1,
        )
    with col_c2:
        include_emojis = st.checkbox("Include emojis", value=True)

    if st.button("📝 Generate Caption & Hashtags", use_container_width=True):
        if not idea.strip():
            st.warning("Please enter a post idea first.")
        else:
            with st.spinner("Writing your post like a pro copywriter..."):
                caption_prompt = f"""
                You are a top-tier social media copywriter.

                Brand: {brand}
                Niche: {niche}
                Target audience: {audience}
                Tone of voice: {tone}
                Platform: {platform}
                Caption length: {length_choice}
                Emojis: {"Yes, use them naturally." if include_emojis else "No emojis."}

                Post idea:
                {idea}

                Write a complete {platform} post with:
                1. A scroll-stopping hook (max 20 words)
                2. The main caption body in the chosen length and tone
                3. A strong, clear call-to-action
                4. If Instagram → 15 relevant, mixed hashtags
                   If LinkedIn → 8 search-friendly key phrases (not with #)
                   If YouTube Shorts → a list of 10 SEO keywords

                Format clearly with headings like:
                Hook:
                Caption:
                CTA:
                Hashtags/Keywords:
                """

                try:
                    caption_resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": caption_prompt}],
                    )
                    st.session_state["caption"] = (
                        caption_resp.choices[0].message.content.strip()
                    )
                except Exception as e:
                    st.error(f"Error generating caption: {e}")

    st.write("### 🧾 Generated Post")
    if st.session_state["caption"]:
        st.markdown(st.session_state["caption"])
        st.code(st.session_state["caption"], language="markdown")
    else:
        st.write("_No caption generated yet. Enter an idea and click the button above._")

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

