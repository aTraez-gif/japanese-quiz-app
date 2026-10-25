import streamlit as st
import pandas as pd
import datetime
import urllib.parse
import random
import os

# --- NATIVE HIGH-CONTRAST MOBILE THEMING ---
st.set_page_config(page_title="Nihongo Guild Network", page_icon="🇯🇵", layout="centered")

st.markdown("""
    <style>
    /* Hide desktop framework container components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Responsive High-Contrast Sizing Controls */
    .main .block-container { max-width: 480px; padding-top: 0.5rem; }
    .onboarding-card { background-color: #ffffff; color: #1e1e24; padding: 20px; border-radius: 16px; border: 2px solid #dee2e6; margin-bottom: 15px; }
    .question-box { background-color: #1e1e24; color: #ffffff; padding: 18px; border-radius: 16px; margin-bottom: 15px; text-align: center; border: 2px solid #2ed573; }
    .explanation-card { background-color: #ffffff; color: #1e1e24; padding: 18px; border-radius: 14px; margin-top: 15px; border-left: 6px solid #2ed573; border-top: 1px solid #dee2e6; border-right: 1px solid #dee2e6; border-bottom: 1px solid #dee2e6; }
    .bulletin-box { background: linear-gradient(135deg, #1e1e24, #2f3542); color: #ffffff; padding: 14px; border-radius: 12px; margin-top: 15px; border-left: 5px solid #ffa500; font-size: 13px; }
    
    /* Mobile Action Buttons Matrix */
    div.stButton > button { width: 100% !important; padding: 12px !important; border-radius: 10px !important; font-weight: bold !important; font-size: 15px !important; }
    .wa-link { display: block; text-align: center; background-color: #25D366; color: white !important; font-weight: bold; padding: 12px; border-radius: 10px; text-decoration: none; margin-top: 10px; font-size: 14px; }
    .wa-peer { display: block; text-align: center; background-color: #1e90ff; color: white !important; font-weight: bold; padding: 10px; border-radius: 10px; text-decoration: none; margin-top: 6px; font-size: 13px; }
    </style>
""", unsafe_allow_html=True)

st.title("🇯🇵 Nihongo Guild Network")

# --- LOCAL LOCAL DATABASE PERSISTENCE STORAGE ENGINE ---
DATA_FILE = "local_scores_ledger.csv"

def get_scores_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except:
            pass
    return pd.DataFrame(columns=["Timestamp", "User_ID", "Name", "Group_Code", "Topic", "Correct", "Incorrect"])

def save_score_locally(uid, name, group, correct, incorrect):
    df = get_scores_data()
    new_row = pd.DataFrame([{
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "User_ID": str(uid),
        "Name": str(name),
        "Group_Code": str(group),
        "Topic": "Dynamic Automation Set",
        "Correct": int(correct),
        "Incorrect": int(incorrect)
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

scores_df = get_scores_data()

GLOBAL_COMMUNITY_URL = "https://whatsapp.com"

# --- AUTOMATED MIXED CONCEPT COMPREHENSION MATRIX POOL ---
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
                st.session_state.my_uid = "UID-16728" if user_input_name.strip().lower() == "admin" else f"UID-{random.randint(10000, 99999)}"
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
                st.session_state.my_uid = "UID-16728" if user_input_name.strip().lower() == "admin" else f"UID-{random.randint(10000, 99999)}"
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
                st.session_state.my_uid = "UID-16728" if user_input_name.strip().lower() == "admin" else f"UID-{random.randint(10000, 99999)}"
                st.session_state.my_group = "SOLO"
                st.session_state.user_authenticated = True
                st.rerun()
            else:
                st.warning("Please enter your name first!")
    st.stop()
# --- SIDEBAR INTERACTIVE ACCOUNTS MYPAGE PANEL ---
st.sidebar.markdown(f"### 🥷 MyPage Account Settings")

# Profile Avatar Upload and Persistent Logic
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = None

uploaded_pic = st.sidebar.file_uploader("Upload Profile Image:", type=["png", "jpg", "jpeg"])
if uploaded_pic is not None:
    st.session_state.user_avatar = uploaded_pic

if st.session_state.user_avatar:
    st.sidebar.image(st.session_state.user_avatar, width=100)
else:
    st.sidebar.markdown("🧑‍💻 *No avatar uploaded yet.*")

st.sidebar.write(f"👤 Warrior User: **{st.session_state.my_name}**")
st.sidebar.write(f"🆔 System Token: `{st.session_state.my_uid}`")
st.sidebar.write(f"🛡️ Battle Space: **{st.session_state.my_group}**")

# Reset Application Session Token to Return to Top Options
if st.sidebar.button("🔄 Logout / Back to Top Options"):
    st.session_state.user_authenticated = False
    st.session_state.my_name = ""
    st.session_state.my_uid = ""
    st.session_state.my_group = "SOLO"
    st.rerun()

if st.session_state.my_group != "SOLO" and "invite_url" in st.session_state:
    st.sidebar.markdown(f'<a href="{st.session_state.invite_url}" target="_blank" class="wa-link">📲 Share Group Invite via WhatsApp</a>', unsafe_allow_html=True)

st.sidebar.markdown(f'<a href="{GLOBAL_COMMUNITY_URL}" target="_blank" style="background-color:#00a8ff;" class="wa-link">🌐 Join Global WhatsApp Community</a>', unsafe_allow_html=True)

# --- MOTIVATIONAL SIDEBAR BULLETIN BOARD ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 📜 Guild Bulletin Announcement")

my_total_correct = 0
if not scores_df.empty:
    my_records = scores_df[scores_df["User_ID"] == st.session_state.my_uid]
    if not my_records.empty:
        my_total_correct = pd.to_numeric(my_records["Correct"]).sum()

if st.session_state.my_group == "SOLO":
    if my_total_correct >= 20:
        bulletin_text = "🔥 **Outstanding work!** You are outperforming typical casual solo learners. Keep pushing for the 100 benchmark!"
    else:
        bulletin_text = "🌱 **Journey begun.** Keep tackling core quiz assessments to increase your rank metrics!"
else:
    # Filter matrix context values to map leader comparisons
    group_totals = scores_df[scores_df["Group_Code"] == st.session_state.my_group] if not scores_df.empty else pd.DataFrame()
    if not group_totals.empty:
        group_totals["Correct"] = pd.to_numeric(group_totals["Correct"])
        group_summary = group_totals.groupby("User_ID")["Correct"].sum().reset_index()
        top_group_score = group_summary["Correct"].max()
        
        if my_total_correct >= top_group_score and my_total_correct > 0:
            bulletin_text = "👑 **Apex Standing!** You are currently commanding the highest accurate score in your closed circle. Protect the throne!"
        else:
            deficit = int(top_group_score - my_total_correct)
            bulletin_text = f"⚔️ **Battle Alert!** You are trailing the group leader by exactly **{deficit} points**. Run another quiz set to catch up!"
    else:
        bulletin_text = "💤 **Lobby quiet.** Send the invite link above to bring opponents into this scorecard grid!"

st.sidebar.markdown(f'<div class="bulletin-box">{bulletin_text}</div>', unsafe_allow_html=True)

# --- SECURE CONTENT ADMIN MODULE PANEL ---
if st.session_state.my_uid == "UID-16728":
    with st.sidebar.expander("🛠️ Admin Controls"):
        admin_password = st.text_input("Admin Password:", type="password", key="admin_pwd_field")
        if admin_password == "Gaikokujin":
            st.success("Developer Access Enabled")

# --- EXECUTE APP NAVIGATION DECK SPLITTING LAYOUT ---
tab1, tab2, tab3 = st.tabs(["🏆 Arena Scoreboard", "⚔️ Active Quiz Room", "📈 My Personal Progress"])
# --- TAB 1: GAMIFIED ENGAGING SCOREBOARD ---
with tab1:
    if st.session_state.my_group == "SOLO":
        st.info("Log into a multiplayer group to view leaderboard statuses.")
    else:
        st.subheader(f"👑 Guild Arena Standings ({st.session_state.my_group})")
        group_df = scores_df[scores_df["Group_Code"] == st.session_state.my_group] if not scores_df.empty else pd.DataFrame()
        
        if not group_df.empty:
            group_df["Correct"] = pd.to_numeric(group_df["Correct"])
            group_df["Incorrect"] = pd.to_numeric(group_df["Incorrect"])
            
            leaderboard = group_df.groupby(["User_ID", "Name"]).agg(
                Total_Correct=("Correct", "sum"),
                Total_Incorrect=("Incorrect", "sum")
            ).reset_index()
            
            def calculate_badge(row_data):
                score = row_data["Total_Correct"]
                if score >= 50: return "👑 Master Shogun"
                elif score >= 25: return "⚔️ Ronin Elite"
                return "🌾 Student Novice"
                
            leaderboard["Guild Badge Title"] = leaderboard.apply(calculate_badge, axis=1)
            leaderboard = leaderboard.sort_values(by="Total_Correct", ascending=False)
            
            st.dataframe(leaderboard[["Name", "Guild Badge Title", "Total_Correct", "Total_Incorrect"]], use_container_width=True, hide_index=True)
            st.subheader("👀 Members Live Attempt Stream")
            st.dataframe(group_df[["Timestamp", "Name", "Topic", "Correct", "Incorrect"]], use_container_width=True, hide_index=True)
        else:
            st.info("No recorded score logs yet inside this zone. Use your invite links above!")
# --- TAB 2: ACTIVE QUIZ ROOM WITH DIRECT PEER-CHALLENGE LINK ROUTING ---
with tab2:
    st.subheader("📝 Live Challenge")
    
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.run_correct = 0
        st.session_state.run_incorrect = 0
        st.session_state.show_explanation = False
        st.session_state.last_answer_status = ""

    q_idx = st.session_state.quiz_index

    if q_idx < 10:
        row = questions_list[q_idx]
        
        st.markdown(f"""
        <div class="question-box">
            <span style="font-weight: bold; text-transform: uppercase; font-size:12px; letter-spacing:1px; color:#2ed573;">CHALLENGE {q_idx + 1} OF 10</span>
            <h2 style="margin-top:5px; margin-bottom:5px; color:#ffffff; font-size:18px;">{row['Question']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            ans_A = st.button(f"A) {row['options'][0]}", key=f"qa_A_{q_idx}", disabled=st.session_state.show_explanation)
            ans_C = st.button(f"C) {row['options'][2]}", key=f"qa_C_{q_idx}", disabled=st.session_state.show_explanation)
        with col2:
            ans_B = st.button(f"B) {row['options'][1]}", key=f"qa_B_{q_idx}", disabled=st.session_state.show_explanation)
            ans_D = st.button(f"D) {row['options'][3]}", key=f"qa_D_{q_idx}", disabled=st.session_state.show_explanation)
            
        user_choice = None
        if ans_A: user_choice = "A"
        if ans_B: user_choice = "B"
        if ans_C: user_choice = "C"
        if ans_D: user_choice = "D"
        
        if user_choice and not st.session_state.show_explanation:
            correct_key = row['correct']
            if user_choice == correct_key:
                st.session_state.run_correct += 1
                st.session_state.last_answer_status = "CORRECT"
            else:
                st.session_state.run_incorrect += 1
                st.session_state.last_answer_status = "INCORRECT"
            st.session_state.show_explanation = True
            st.rerun()

        if st.session_state.show_explanation:
            status_color = "🟢 CORRECT!" if st.session_state.last_answer_status == "CORRECT" else "🔴 INCORRECT"
            st.markdown(f"""
            <div class="explanation-card">
                <h4 style="margin:0px; color:#2f3542;">{status_color} • Concept Analysis</h4>
                <hr style="margin:8px 0px; border-color:#ced4da;">
                <p style="margin:4px 0px;"><strong>Item:</strong> {row['word']}</p>
                <p style="margin:4px 0px;"><strong>Exact Meaning:</strong> {row['meaning']}</p>
                <p style="margin:4px 0px;"><strong>Breakdown:</strong> {row['desc']}</p>
                <p style="margin:4px 0px; background:#f1f2f6; padding:8px; border-radius:6px; border-left:3px solid #ff7f50;"><strong>💡 Practice Sentence Example:</strong><br><em>{row['example']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Next Challenge ➡️", key="next_q_btn"):
                st.session_state.quiz_index += 1
                st.session_state.show_explanation = False
                st.rerun()
                
        st.write("")
        peer_challenge_msg = (
            f"⚔️ *Nihongo Peer Challenge Duel!* 🥷\n\n"
            f"Hey! {st.session_state.my_name} is throwing a live question text to you from Room {st.session_state.my_group}.\n\n"
            f"👉 *Question:* \"{row['Question']}\"\n\n"
            f"Reply to this text message and let me know your answer choice option (A, B, C, or D) to settle who has a better grasp!"
        )
        st.markdown(f'<a href="https://wa.me{urllib.parse.quote(peer_challenge_msg)}" target="_blank" class="wa-peer">🚀 Throw Question to a Friend on WhatsApp</a>', unsafe_allow_html=True)
        
    else:
        st.success("🏁 Challenge Completed Successfully!")
        st.write(f"✅ Total Right: **{st.session_state.run_correct}**")
        st.write(f"❌ Total Missed: **{st.session_state.run_incorrect}**")
        
        if st.button("Save & Upload Results to Ledger Scoreboard"):
            # Trigger our newly fixed, local persistent writer method
            save_score_locally(
                st.session_state.my_uid, 
                st.session_state.my_name, 
                st.session_state.my_group, 
                st.session_state.run_correct, 
                st.session_state.run_incorrect
            )
            st.success("Scores synced safely into repository database file!")
            
            del st.session_state.quiz_index
            del st.session_state.run_correct
            del st.session_state.run_incorrect
            st.rerun()
# --- TAB 3: PERSONAL PROGRESS TRACKING TIMELINE ENGINE ---
with tab3:
    st.subheader("📈 My Personal Mastery Journey")
    
    # Reload fresh file logs on state changes
    fresh_df = get_scores_data()
    my_history_df = fresh_df[fresh_df["User_ID"] == str(st.session_state.my_uid)] if not fresh_df.empty else pd.DataFrame()
    
    if not my_history_df.empty:
        my_history_df["Correct"] = pd.to_numeric(my_history_df["Correct"])
        my_history_df["Incorrect"] = pd.to_numeric(my_history_df["Incorrect"])
        
        total_my_correct = int(my_history_df["Correct"].sum())
        total_my_incorrect = int(my_history_df["Incorrect"].sum())
        total_attempts = total_my_correct + total_my_incorrect
        
        accuracy_ratio = round((total_my_correct / total_attempts) * 100, 1) if total_attempts > 0 else 0
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="Lifetime Right Answers", value=f"{total_my_correct} ✅")
        with c2:
            st.metric(label="Overall Accuracy Ratio", value=f"{accuracy_ratio}% 🎯")
            
        st.markdown("### 🔓 Guild Achievements & Trophies")
        
        if total_my_correct >= 1:
            st.success("🔰 **UNLOCKED: First Victory** (Logged your first correct answer in the arena!)")
        else:
            st.markdown("<div style='background-color:#ffffff; border:1px dashed #ced4da; padding:10px; border-radius:8px; color:#a4b0be;'>🔒 *First Victory (Get 1 question right to unlock)*</div>", unsafe_allow_html=True)
            
        if total_my_correct >= 100:
            st.success("👑 **UNLOCKED: Centurion Warrior** (Massive Dedication! Passed 100 correct entries!)")
        else:
            st.markdown(f"<div style='background-color:#ffffff; border:1px dashed #ced4da; padding:10px; border-radius:8px; color:#a4b0be;'>🔒 *Centurion Warrior ({total_my_correct}/100 questions correct)*</div>", unsafe_allow_html=True)
            
        if accuracy_ratio >= 85.0 and total_attempts >= 10:
            st.success(f"🎯 **UNLOCKED: Flawless Striker** (Maintained a superb precision accuracy of {accuracy_ratio}%)")
        else:
            st.markdown(f"<div style='background-color:#ffffff; border:1px dashed #ced4da; padding:10px; border-radius:8px; color:#a4b0be;'>🔒 *Flawless Striker (Maintain 85%+ accuracy with at least 10 attempts. Current: {accuracy_ratio}%)*</div>", unsafe_allow_html=True)
        st.write("")

        st.markdown("### 📊 Accuracy Progress Over Time")
        my_history_df["Cumulative_Correct"] = my_history_df["Correct"].cumsum()
        st.line_chart(my_history_df, x="Timestamp", y="Cumulative_Correct", color="#1e90ff")
    else:
        st.info("Complete your first quiz evaluation run to map your performance progress dashboard timeline.")
