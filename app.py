import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import urllib.parse
import random
import requests

# --- NATIVE HIGH-CONTRAST MOBILE THEMING ---
st.set_page_config(page_title="Nihongo Guild Network", page_icon="🇯🇵", layout="centered")

# Injected CSS with media-query color fail-safes for optimal phone visibility
st.markdown("""
    <style>
    /* Hide default framework wrapper layout margins */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Device Accessibility Styling Rules */
    .main .block-container { max-width: 480px; padding-top: 0.5rem; }
    .onboarding-card { background-color: #ffffff; color: #1e1e24; padding: 20px; border-radius: 16px; border: 2px solid #dee2e6; margin-bottom: 15px; }
    .question-box { background-color: #1e1e24; color: #ffffff; padding: 18px; border-radius: 16px; margin-bottom: 15px; text-align: center; border: 2px solid #2ed573; }
    .explanation-card { background-color: #ffffff; color: #1e1e24; padding: 18px; border-radius: 14px; margin-top: 15px; border-left: 6px solid #2ed573; border-top: 1px solid #dee2e6; border-right: 1px solid #dee2e6; border-bottom: 1px solid #dee2e6; }
    
    /* Mobile-Native Action Grid Customizations */
    div.stButton > button { width: 100% !important; padding: 12px !important; border-radius: 10px !important; font-weight: bold !important; font-size: 15px !important; }
    .wa-link { display: block; text-align: center; background-color: #25D366; color: white !important; font-weight: bold; padding: 12px; border-radius: 10px; text-decoration: none; margin-top: 10px; font-size: 14px; }
    .wa-peer { display: block; text-align: center; background-color: #1e90ff; color: white !important; font-weight: bold; padding: 10px; border-radius: 10px; text-decoration: none; margin-top: 6px; font-size: 13px; }
    </style>
""", unsafe_allow_html=True)

st.title("🇯🇵 Nihongo Guild Network")

# --- GLOBAL DATA DATA LEDGER CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(sheet_name, fallback_cols):
    try:
        return conn.read(worksheet=sheet_name, ttl="0m")
    except:
        return pd.DataFrame(columns=fallback_cols)

scores_df = load_data("Sheet1", ["Timestamp", "User_ID", "Name", "Group_Code", "Topic", "Correct", "Incorrect"])

# --- 🎯 ACTION: PASTE YOUR COPIED WHATSAPP COMMUNITY LINK HERE 🎯 ---
GLOBAL_COMMUNITY_URL = "https://whatsapp.com"
GOOGLE_FORM_URL = "https://google.com"

# --- AUTOMATED MIXED CONCEPT COMPREHENSION MATRIX ---
@st.cache_data
def get_automated_question_bank():
    base_pool = [
        {
            "word": "Mondai nai (問題ない)",
            "meaning": "No problem / There is no issue.",
            "desc": "'Mondai' translates to problem or question, and 'nai' means there isn't any. Use it casually to assure someone that a plan, task, or condition is safely under control.",
            "example": "A: 'Asu no kaigi, ma ni au?' (Meeting tomorrow, will you make it?) \nB: 'Mondai nai desu!' (No problem!)",
            "q_type": "meaning",
            "options": ["Excuse me", "No problem", "Goodbye", "I don't understand"],
            "correct": "B"
        },
        {
            "word": "Arimasu (あります)",
            "meaning": "There is / To have (Inanimate Objects).",
            "desc": "Used strictly for non-living items like places, buildings, plants, or concepts. It states existence or personal possession.",
            "example": "Kuruma ga arimasu. (I have a car / There is a car.)",
            "q_type": "grammar",
            "options": ["People only", "Animals only", "Inanimate objects", "Moving things"],
            "correct": "C"
        },
        {
            "word": "Arimasen (ありません)",
            "meaning": "There is not / Do not have (Inanimate Objects).",
            "desc": "The polite negative form of 'arimasu'. It denotes that a non-living object is missing or not owned.",
            "example": "Jikan ga arimasen. (I do not have time.)",
            "q_type": "meaning",
            "options": ["I will go", "I don't have / there is none", "Please wait", "Thank you"],
            "correct": "B"
        },
        {
            "word": "Ikimasu (行きます)",
            "meaning": "To go.",
            "desc": "An active motion verb indicating movement away from your current position toward a physical destination.",
            "example": "Gakkou e ikimasu. (I am going to school.)",
            "q_type": "meaning",
            "options": ["To eat", "To go", "To speak", "To sleep"],
            "correct": "B"
        },
        {
            "word": "Ikimasen (行きません)",
            "meaning": "Will not go / Do not go.",
            "desc": "The polite negative expression of 'ikimasu'. Used to declare you aren't journeying to a specific location.",
            "example": "Doko mo ikimasen. (I am not going anywhere.)",
            "q_type": "grammar",
            "options": ["I went yesterday", "I want to go", "I am going", "I will not go"],
            "correct": "D"
        }
    ]
    extended_bank = []
    scenarios = ["tomorrow morning", "tonight late", "at the Tokyo office", "with the language team", "at the dynamic arena lounge"]
    for i in range(110):
        for base in base_pool:
            scen = random.choice(scenarios)
            item = base.copy()
            item["ID"] = len(extended_bank) + 1
            if item["q_type"] == "meaning":
                item["Question"] = f"When evaluating a setup scheduled {scen}, what does '{item['word']}' indicate?"
            else:
                item["Question"] = f"Identify the structural rule requirement for using '{item['word']}' safely {scen}."
            extended_bank.append(item)
    return extended_bank

questions_list = get_automated_question_bank()

# --- APP ONBOARDING SYSTEM DECK ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.my_name = ""
    st.session_state.my_uid = ""
    st.session_state.my_group = "SOLO"

if not st.session_state.user_authenticated:
    st.subheader("👋 Welcome to the Guild Arena")
    st.write("Enter your profile name to setup your tracking token:")
    
    user_input_name = st.text_input("Profile Display Name / Nickname:", placeholder="e.g., Alex")
    st.markdown("---")
    
    with st.expander("➕ Option 1: Invite Friends & Create a Closed Group"):
        st.markdown("<div class='onboarding-card'>Generate a private group access token to invite your inner circle.</div>", unsafe_allow_html=True)
        if st.button("Generate Group Access Token", key="create_group_btn"):
            if user_input_name.strip():
                new_group_code = f"G-{random.randint(1000, 9999)}"
                st.session_state.my_name = user_input_name
                
                # Check if this is the Master Admin logging in
                if user_input_name.strip().lower() == "admin":
                    st.session_state.my_uid = "UID-16728"
                else:
                    st.session_state.my_uid = f"UID-{random.randint(10000, 99999)}"
                    
                st.session_state.my_group = new_group_code
                st.session_state.user_authenticated = True
                
                invite_msg = (
                    f"🇯🇵 *Join my private Japanese Learning Arena!* 🥷\n\n"
                    f"Open the link, select 'Join Existing Group', and enter our code:\n"
                    f"👉 *Group Code:* {new_group_code}"
                )
                st.session_state.invite_url = f"https://wa.me{urllib.parse.quote(invite_msg)}"
                st.rerun()
            else:
                st.warning("Please type your name first!")

    with st.expander("🤝 Option 2: Join an Existing Closed Group"):
        st.markdown("<div class='onboarding-card'>Sync up score metrics with an established circle leaderboard.</div>", unsafe_allow_html=True)
        input_code = st.text_input("Enter Group Code (e.g., G-1234):", key="join_code_field")
        if st.button("Connect Ledger to Group", key="join_group_btn"):
            if user_input_name.strip() and input_code.strip():
                st.session_state.my_name = user_input_name
                
                # Check if this is the Master Admin logging in
                if user_input_name.strip().lower() == "admin":
                    st.session_state.my_uid = "UID-16728"
                else:
                    st.session_state.my_uid = f"UID-{random.randint(10000, 99999)}"
                    
                st.session_state.my_group = input_code.strip().upper()
                st.session_state.user_authenticated = True
                st.rerun()
            else:
                st.warning("Make sure fields are filled out properly!")

    with st.expander("📖 Option 3: Simply Start Learning Solo"):
        st.markdown("<div class='onboarding-card'>Track metrics locally on an isolated solo training row timeline.</div>", unsafe_allow_html=True)
        if st.button("Launch Isolated Solo Mode", key="solo_btn"):
            if user_input_name.strip():
                st.session_state.my_name = user_input_name
                
                # Check if this is the Master Admin logging in
                if user_input_name.strip().lower() == "admin":
                    st.session_state.my_uid = "UID-16728"
                else:
                    st.session_state.my_uid = f"UID-{random.randint(10000, 99999)}"
                    
                st.session_state.my_group = "SOLO"
                st.session_state.user_authenticated = True
                st.rerun()
            else:
                st.warning("Please enter your name first!")
    st.stop()

# --- SIDEBAR COMPONENT REGISTRY DECK ---
    st.sidebar.markdown(f"### 🥷 Profile Card")
st.sidebar.write(f"👤 User: {st.session_state.my_name}")
st.sidebar.write(f"🆔 ID: {st.session_state.my_uid}")
st.sidebar.write(f"🛡️ Group: {st.session_state.my_group}")
if st.session_state.my_group != "SOLO" and "invite_url" in st.session_state:
st.sidebar.markdown(f'📲 Share Group Invite via WhatsApp', unsafe_allow_html=True)
st.sidebar.markdown(f'🌐 Join Global WhatsApp Community', unsafe_allow_html=True)
