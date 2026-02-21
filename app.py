import streamlit as st
import ollama
import random

# 1. Page Configuration
st.set_page_config(page_title="curatedLove", page_icon="💝", layout="wide")

# 2. Boutique CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;600&display=swap');

    /* UNIFIED FONT */
    * { font-family: 'Playfair Display', serif !important; }

    /* SOLID PEACH BACKGROUND */
    .stApp { 
        background: #FFCCB3;
        background: linear-gradient(135deg, #FFCCB3 0%, #FFB399 100%);
    }

    /* DARK PLUM LABELS */
    .stMarkdown p {
        color: #4A152C !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* INPUT BOXES & CURSOR FIX */
    input, textarea {
        color: #4A152C !important;
        background-color: #FFF5F0 !important;
        caret-color: #D63384 !important; 
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #FFF5F0 !important;
        color: #4A152C !important;
        border-radius: 12px !important;
        border: 2px solid #FF9980 !important;
    }

    /* LOADING CLOUD */
    .loading-cloud {
        background: white;
        padding: 20px 40px;
        border-radius: 50px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        display: inline-block;
        border: 2px solid #D63384;
        color: #D63384;
        font-weight: 700;
        font-size: 1.4rem;
    }

    /* GIFT CARD STYLING */
    .gift-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        border-top: 8px solid #D63384;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        color: #333;
        min-height: 250px;
    }

    .card-label {
        color: #D63384;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-align: center;
        display: block;
    }

    .output-title { font-weight: 700; font-size: 1.3rem; color: #4A152C; display: block; margin-bottom: 8px; }
    .output-why { font-style: italic; color: #555; display: block; margin-bottom: 8px; font-family: 'Inter', sans-serif !important; font-size: 0.95rem; }
    .output-msg { font-weight: 600; color: #D63384; display: block; font-size: 1.1rem; border-left: 3px solid #D63384; padding-left: 10px; margin: 10px 0; }

    /* BUTTONS */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        background: #D63384;
        color: white !important;
        height: 3.5em;
        font-weight: 700;
        border: none;
        box-shadow: 0 8px 20px rgba(214, 51, 132, 0.3);
    }

    .copy-btn button {
        height: 2.2em !important;
        font-size: 0.85rem !important;
        background: #4A152C !important;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown('<h1 style="text-align: center; color: #4A152C; font-size: 3.5rem;">curatedLove 💝</h1>',
            unsafe_allow_html=True)

# 4. Input Layout
with st.container():
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        # Row 1: Identity
        r1_c1, r1_c2, r1_c3 = st.columns([2, 1, 1])
        with r1_c1:
            st.markdown("👤 Who is this for?")
            persona = st.text_input("Who", placeholder="e.g. My Friend", label_visibility="collapsed")
        with r1_c2:
            st.markdown("🎂 Age")
            age = st.number_input("Age", min_value=0, max_value=120, value=25, label_visibility="collapsed")
        with r1_c3:
            st.markdown("⚧ Gender")
            gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Prefer not to say"],
                                  label_visibility="collapsed")

        # Row 2: Context
        r2_c1, r2_c2, r2_c3 = st.columns([2, 2, 2])
        with r2_c1:
            st.markdown("🗓️ The Occasion")
            occasion = st.text_input("Occasion", placeholder="e.g. Housewarming", label_visibility="collapsed")
        with r2_c2:
            st.markdown("🤝 Relationship")
            rel_depth = st.selectbox("Relationship", ["Family 🏠", "Super Close 🤞", "Friendly 😊", "Professional 🤝",
                                                      "Just Reconnecting 🌿"], label_visibility="collapsed")
        with r2_c3:
            st.markdown("💰 Budget")
            budget = st.text_input("Budget", placeholder="e.g. 1500", label_visibility="collapsed")

        st.markdown("📝 Tell us more about their style...")
        details = st.text_area("Details",
                               placeholder="Describe their hobbies, favorite aesthetic, or any inside jokes...",
                               height=70, label_visibility="collapsed")

        curate_clicked = st.button("✨ Curate My Selection")


# 5. Logic
def get_curation():
    SYSTEM_PROMPT = f"""
    You are a luxury gift concierge. 
    Context: Recipient is a {age}-year-old {gender}.
    Relationship: {rel_depth}. 
    Instruction: Tailor the gift ideas and the card message tone strictly to this profile.

    Suggest 3 gift ideas. Format exactly:
    TITLE: [Name]
    WHY: [Reason]
    MESSAGE: [1 line card message]
    Separate ideas with '---'.
    """
    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",
                 "content": f"Persona: {persona}, Occasion: {occasion}, Budget: {budget}, Details: {details}"}
            ],
            options={"temperature": 0.8, "seed": random.randint(1, 99999)}
        )
        return response["message"]["content"].split("---")
    except Exception:
        return ["Error: AI not responding", "", ""]


def render_gift_card(label, content, key_suffix):
    lines = content.strip().split('\n')
    t, w, m = "Gift Idea", "Thinking...", "Card message..."
    for line in lines:
        if "TITLE:" in line.upper(): t = line.replace("TITLE:", "").strip()
        if "WHY:" in line.upper(): w = line.replace("WHY:", "").strip()
        if "MESSAGE:" in line.upper(): m = line.replace("MESSAGE:", "").strip()

    st.markdown(f"""
        <div class="gift-card">
            <span class="card-label">{label}</span>
            <span class="output-title">🎁 {t}</span>
            <span class="output-why"><b>Why:</b> {w}</span>
            <span class="output-msg">"{m}"</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="copy-btn">', unsafe_allow_html=True)
    if st.button(f"📋 Copy Message: {label}", key=f"copy_{key_suffix}"):
        st.code(m, language=None)
        st.toast("Message ready to copy! 📝")
    st.markdown('</div>', unsafe_allow_html=True)


# 6. Result Generation
if curate_clicked:
    if persona and occasion:
        loading = st.empty()
        loading.markdown(
            f'<div style="text-align:center;"><div class="loading-cloud">☁️ 💖 Finding something perfect for a {age}yo {gender}...</div></div>',
            unsafe_allow_html=True)

        items = get_curation()
        loading.empty()
        st.balloons()

        st.markdown(
            "<h2 style='text-align: center; color: #4A152C; margin-bottom: 20px;'>🥂 Your Bespoke Selection</h2>",
            unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            render_gift_card("The Safe Bet", items[0] if len(items) > 0 else "", "safe")
        with r1c2:
            render_gift_card("The Wildcard", items[1] if len(items) > 1 else "", "wild")

        r2s1, r2mid, r2s2 = st.columns([1, 2, 1])
        with r2mid:
            render_gift_card("The Experience", items[2] if len(items) > 2 else "", "exp")

        if st.button("🔄 Regenerate Curation"):
            st.rerun()
    else:
        st.warning("Please tell us who the gift is for and the occasion! 🌸")