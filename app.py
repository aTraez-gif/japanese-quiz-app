import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import urllib.parse
import random

# --- NATIVE MOBILE OVERRIDES & CAPTURING LAYOUT ---
st.set_page_config(page_title="Nihongo Guild Network", page_icon="🇯🇵", layout="centered")

st.markdown("""
    <style>
    .main .block-container { max-width: 480px; padding-top: 1rem; }
    .onboarding-card { background: #f8f9fa; padding: 20px; border-radius: 16px; border: 1px solid #dee2e6; margin-bottom: 15px; }
    .question-box { background: #f1f2f6; padding: 18px; border-radius: 16px; margin-bottom: 15px; text-align: center; border: 1px solid #ced4da; }
    
    /* Interactive Button Styling */
    div.stButton > button { width: 100% !important; padding: 12px !important; border-radius: 10px !important; font-weight: bold !important; }
    
    /* Dedicated WhatsApp Styling Matrix */
    .wa-link { display: block; text-align: center; background-color: #25D366; color: white !important; font-weight: bold; padding: 12px; border-radius: 10px; text-decoration: none; margin-top: 10px; font-size: 14px;}
    </style>
""", unsafe_allow_html=True)

st.title("🇯🇵 Nihongo Guild Network")

# --- GLOBAL DATA CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(sheet_name, fallback_cols):
    try:
        return conn.read(worksheet=sheet_name, ttl="0m")
    except:
        return pd.DataFrame(columns=fallback_cols)

scores_df = load_data("Sheet1", ["Timestamp", "User_ID", "Name", "Group_Code", "Topic", "Correct", "Incorrect"])
questions_df = load_data("Questions", ["ID", "Question", "Option_A", "Option_B", "Option_C", "Option_D", "Correct_Option"])

# --- 🎯 ACTION: PASTE YOUR COPIED WHATSAPP COMMUNITY LINK HERE 🎯 ---
GLOBAL_COMMUNITY_URL = "https://chat.whatsapp.com/I3ajCTSGOgo2UZpH5GnY2x"

# --- ONBOARDING ENGINE ---
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
    st.session_state.my_name = ""
    st.session_state.my_uid = ""
    st.session_state.my_group = "SOLO"

if not st.session_state.user_authenticated:
    st.subheader("👋 Welcome to the Guild Arena")
    st.write("Choose how you want to learn and track your Japanese progress:")
    
    user_input_name = st.text_input("First, enter your name / nickname:", placeholder="e.g., Alex")
    st.markdown("---")
    
    # PATH A: Create a Closed Group
    with st.expander("➕ Option 1: Invite Friends & Create a Closed Group"):
        st.markdown("<div class='onboarding-card'>Create a private tracking space for you and your friends.</div>", unsafe_allow_html=True)
        if st.button("Generate My Group Code", key="create_group_btn"):
            if user_input_name.strip():
                new_group_code = f"G-{random.randint(1000, 9999)}"
                st.session_state.my_name = user_input_name
                st.session_state.my_uid = f"UID-{random.randint(10000, 99999)}"
                st.session_state.my_group = new_group_code
                st.session_state.user_authenticated = True
                
                invite_msg = (
                    f"🇯🇵 *Join my private Japanese Learning Arena!* 🥷\n\n"
                    f"I set up our tracking lobby. Open the app link, choose 'Join Existing Group', and enter our code:\n"
                    f"👉 *Group Code:* {new_group_code}\n\n"
                    f"Let's see who gets the highest score!"
                )
                st.session_state.invite_url = f"https://wa.me{urllib.parse.quote(invite_msg)}"
                st.rerun()
            else:
                st.warning("Please type your name first!")

    # PATH B: Join Existing Group
    with st.expander("🤝 Option 2: Join an Existing Closed Group"):
        st.markdown("<div class='onboarding-card'>Enter a code shared by your friend to sync scoreboards.</div>", unsafe_allow_html=True)
        input_code = st.text_input("Enter Group Code (e.g., G-1234):", key="join_code_field")
        if st.button("Connect to Group", key="join_group_btn"):
            if user_input_name.strip() and input_code.strip():
                st.session_state.my_name = user_input_name
                st.session_state.my_uid = f"UID-{random.randint(10000, 99999)}"
                st.session_state.my_group = input_code.strip().upper()
                st.session_state.user_authenticated = True
                st.rerun()
            else:
                st.warning("Make sure both Name and Group Code fields are filled out!")

    # PATH C: Solo Learning Journey
    with st.expander("📖 Option 3: Simply Start Learning Solo"):
        st.markdown("<div class='onboarding-card'>Ditch the multiplayer scoreboards and practice on your own timeline.</div>", unsafe_allow_html=True)
        if st.button("Launch Solo Mode", key="solo_btn"):
            if user_input_name.strip():
                st.session_state.my_name = user_input_name
                st.session_state.my_uid = f"UID-{random.randint(10000, 99999)}"
                st.session_state.my_group = "SOLO"
                st.session_state.user_authenticated = True
                st.rerun()
            else:
                st.warning("Please enter your name first!")
                
    st.stop()

# --- SIDEBAR INTERFACE & SYSTEM PROFILE ---
st.sidebar.markdown(f"### 🥷 Profile Card")
st.sidebar.write(f"👤 User: **{st.session_state.my_name}**")
st.sidebar.write(f"🆔 ID: `{st.session_state.my_uid}`")
st.sidebar.write(f"🛡️ Group: **{st.session_state.my_group}**")

# Group Join Sharing Hook
if st.session_state.my_group != "SOLO" and "invite_url" in st.session_state:
    st.sidebar.markdown(f'<a href="{st.session_state.invite_url}" target="_blank" class="wa-link">📲 Share Group Invite via WhatsApp</a>', unsafe_allow_html=True)

st.sidebar.markdown(f'<a href="{GLOBAL_COMMUNITY_URL}" target="_blank" style="background-color:#00a8ff;" class="wa-link">🌐 Join Global WhatsApp Community</a>', unsafe_allow_html=True)

# --- 🛠️ SECURE CONTENT ADMIN DRAWER PANEL 🛠️ ---
st.sidebar.markdown("---")
with st.sidebar.expander("🛠️ Admin Controls (Add Questions)"):
    st.caption("Inject a question straight into the core live Google Sheet registry.")
    with st.form("admin_question_form", clear_on_submit=True):
        new_q_text = st.text_area("Question Text:")
        col_a, col_b = st.columns(2)
        with col_a:
            opt_a = st.text_input("Option A:")
            opt_c = st.text_input("Option C:")
        with col_b:
            opt_b = st.text_input("Option B:")
            opt_d = st.text_input("Option D:")
        
        correct_ans = st.selectbox("Correct Option Key:", ["A", "B", "C", "D"])
        admin_submit = st.form_submit_button("Publish Question Live")
        
        if admin_submit:
            if new_q_text.strip() and opt_a.strip() and opt_b.strip():
                next_id = int(questions_df["ID"].max() + 1) if not questions_df.empty else 1
                
                new_q_row = pd.DataFrame([{
                    "ID": int(next_id),
                    "Question": new_q_text.strip(),
                    "Option_A": opt_a.strip(),
                    "Option_B": opt_b.strip(),
                    "Option_C": opt_c.strip(),
                    "Option_D": opt_d.strip(),
                    "Correct_Option": correct_ans
                }])
                
                updated_questions = pd.concat([questions_df, new_q_row], ignore_index=True)
                conn.update(worksheet="Questions", data=updated_questions)
                st.success(f"Success! Question #{next_id} added.")
                st.rerun()
            else:
                st.error("Fields cannot be left blank!")

# --- PRIMARY DISPLAY ROUTER ---
tab1, tab2 = st.tabs(["🏆 Arena Scoreboard", "⚔️ Active Quiz"])

# --- TAB 1: ARENA SCOREBOARD DISPLAY ---
with tab1:
    if st.session_state.my_group == "SOLO":
        st.subheader("📊 Your Practice Runs")
        my_filtered_df = scores_df[scores_df["User_ID"] == st.session_state.my_uid] if not scores_df.empty else pd.DataFrame()
        if not my_filtered_df.empty:
            st.dataframe(my_filtered_df[["Timestamp", "Topic", "Correct", "Incorrect"]], use_container_width=True, hide_index=True)
        else:
            st.info("No recorded practice trials logged yet.")
    else:
        st.subheader(f"📊 Group Scoreboard: {st.session_state.my_group}")
        group_df = scores_df[scores_df["Group_Code"] == st.session_state.my_group] if not scores_df.empty else pd.DataFrame()
        
        if not group_df.empty:
            group_df["Correct"] = pd.to_numeric(group_df["Correct"])
            leaderboard = group_df.groupby(["User_ID", "Name"]).agg(
                Total_Correct=("Correct", "sum"),
                Total_Incorrect=("Incorrect", "sum")
            ).reset_index().sort_values(by="Total_Correct", ascending=False)
            
            st.dataframe(leaderboard, use_container_width=True, hide_index=True)
            st.subheader("👀 Members Action History Log")
            st.dataframe(group_df[["Timestamp", "Name", "Topic", "Correct", "Incorrect"]], use_container_width=True, hide_index=True)
        else:
            st.info("No logs generated by this group zone yet. Share the invitation link above!")

# --- TAB 2: MOBILIZED ACTIVE QUIZ COMPONENT ---
with tab2:
    st.subheader("📝 Live Challenge")
    
    if questions_df.empty:
        st.warning("The database is currently empty. Open the Admin Panel on the left side to add questions.")
    else:
        if "q_index" not in st.session_state:
            st.session_state.q_index = 0
            st.session_state.temp_correct = 0
            st.session_state.temp_incorrect = 0

        q_idx = st.session_state.q_index

        if q_idx < len(questions_df):
            row = questions_df.iloc[q_idx]
            
            st.markdown(f"""
            <div class="question-box">
