import streamlit as st
import ollama

# 1. Page Configuration
st.set_page_config(page_title="curatedLove", page_icon="💝", layout="centered")

# 2. Boutique Styling (Peach & Gold Theme)
st.markdown("""
    <style>
    /* Import a sophisticated font */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;600&display=swap');

    .stApp { 
        background-color: #FFF5EE; /* Soft Peach / Seashell */
        background-image: linear-gradient(180deg, #FFF5EE 0%, #FFEFDB 100%);
    }

    /* Titles and Headers */
    .main-title {
        font-family: 'Playfair Display', serif;
        color: #5D3754;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0px;
    }

    .sub-title {
        font-family: 'Inter', sans-serif;
        color: #8E6E86;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }

    /* Input Labels */
    .stMarkdown p {
        font-family: 'Inter', sans-serif;
        color: #5D3754 !important;
        font-weight: 600;
        margin-bottom: -15px;
    }

    /* Input Box Styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 12px !important;
        border: 1px solid #EAD7D7 !important;
        color: #5D3754 !important;
        padding: 10px 15px !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #D63384 !important;
        box-shadow: 0 0 0 2px rgba(214, 51, 132, 0.2) !important;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        background: linear-gradient(145deg, #D63384, #A02663);
        color: white !important;
        height: 3.5em;
        font-family: 'Inter', sans-serif;
        font-weight: bold;
        border: none;
        box-shadow: 0px 4px 15px rgba(214, 51, 132, 0.3);
        transition: all 0.3s ease;
        margin-top: 10px;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(214, 51, 132, 0.4);
        background: linear-gradient(145deg, #E04090, #B02A6A);
    }

    /* Curation Result Card */
    .curation-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        border-left: 5px solid #D63384;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        color: #2D2D2D;
    }

    hr {
        margin: 2em 0;
        border: 0;
        border-top: 1px solid #EAD7D7;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown('<h1 class="main-title">curatedLove 💝</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ AI-powered personalized gifts for your favorites</p>', unsafe_allow_html=True)

# 4. Input Form Layout
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("👤 **Who is this for?**")
        persona = st.text_input("Who", placeholder="e.g. My mom", label_visibility="collapsed")

        st.markdown("💰 **Budget range?**")
        budget = st.text_input("Budget", placeholder="e.g. $500 - $1000", label_visibility="collapsed")

    with col2:
        st.markdown("🗓️ **What's the occasion?**")
        occasion = st.text_input("Occasion", placeholder="e.g. Mother's Day", label_visibility="collapsed")

        st.markdown("🌈 **What's the vibe?**")
        vibe = st.text_input("Vibe", placeholder="e.g. Sentimental, luxurious", label_visibility="collapsed")

    st.markdown("📝 **Any special details?**")
    details = st.text_area("Details", placeholder="e.g. She loves gardening and vintage jewelry...",
                           label_visibility="collapsed")

# 5. Logic Section
SYSTEM_PROMPT = """
You are a high-end gift concierge named curatedLove.
Suggest exactly 3 gift ideas:
1. 🎁 The Safe Bet
2. 🚀 The Wildcard
3. 🌟 The Experience

For each, provide:
- **Gift Title**
- **Why it fits**
- **Card message** (1 line)

Use a warm, sophisticated tone. Use emojis to highlight key points.
"""

if st.button("✨ Curate My Selection"):
    if persona and occasion:
        with st.spinner("🕯️ Lighting the candles and finding the perfect gifts..."):
            try:
                response = ollama.chat(
                    model="phi3:mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user",
                         "content": f"Persona: {persona}\nOccasion: {occasion}\nBudget: {budget}\nVibe: {vibe}\nDetails: {details}"}
                    ],
                    options={"num_predict": 400}
                )

                st.balloons()
                st.markdown("---")
                st.markdown("### 🥂 Your Bespoke Curation")

                # Wrap the AI output in a styled div
                st.markdown(f"""
                <div class="curation-card">
                    {response["message"]["content"]}
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Make sure Ollama is running! Error: {e}")
    else:
        st.warning("Please tell us at least who this is for and the occasion! 🌸")