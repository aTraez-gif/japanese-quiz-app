import streamlit as st
import pandas as pd
import datetime
import urllib.parse
import random
import os

# --- NATIVE HIGH-CONTRAST MOBILE THEMING & METADATA CONFIGURATION ---
st.set_page_config(page_title="Nihongo Guild Network", page_icon="🇯🇵", layout="centered")

# Inject HTML metadata and style rules tailored for high mobile device visibility
st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-title" content="Nihongo Guild Network">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="application-name" content="Nihongo Guild Network">
        <link rel="manifest" href="https://githubusercontent.com">
    </head>
    <style>
    /* Force high-visibility text colors on all mobile screens and operating themes */
    html, body, [data-testid="stSidebar"] {
        color: #ffffff !important;
        background-color: #0f0f12 !important;
    }
    p, span, label, h1, h2, h3, h4, li, div {
        color: #ffffff !important;
    }
    /* Style form input text fields to be visible against dark backgrounds */
    input, select, textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Hide standard platform headers and watermarks */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    .stActionButton {display: none !important;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="stConnectionStatus"] {display: none !important;}
    iframe[title="streamlitApp"] + div {display: none !important;}
    
    /* Responsive High-Contrast Sizing Controls */
    .main .block-container { max-width: 480px; padding-top: 0.5rem; }
    .onboarding-card { background-color: #1e1e24; color: #ffffff !important; padding: 20px; border-radius: 16px; border: 2px solid #2ed573; margin-bottom: 15px; }
    .question-box { background-color: #2ed573; color: #000000 !important; padding: 18px; border-radius: 16px; margin-bottom: 15px; text-align: center; }
    .question-box h3 { color: #000000 !important; }
    .explanation-card { background-color: #1e1e24; color: #ffffff !important; padding: 18px; border-radius: 14px; margin-top: 15px; border-left: 6px solid #2ed573; border-top: 1px solid #2d2d3a; border-right: 1px solid #2d2d3a; border-bottom: 1px solid #2d2d3a; }
    .bulletin-box { background: linear-gradient(135deg, #1e1e24, #2f3542); color: #ffffff !important; padding: 14px; border-radius: 12px; margin-top: 15px; border-left: 5px solid #ffa500; font-size: 13px; }
    
    /* Mobile Action Buttons Matrix Styling */
    div.stButton > button { width: 100% !important; padding: 14px !important; border-radius: 12px !important; font-weight: bold !important; font-size: 16px !important; background: #2ed573 !important; color: #000000 !important; border: none !important; }
    
    /* Fix native mobile link styling inside buttons */
    .mobile-btn { display: block !important; width: 100% !important; text-align: center !important; font-weight: bold !important; padding: 14px !important; border-radius: 12px !important; text-decoration: none !important; margin-top: 10px !important; font-size: 15px !important; box-sizing: border-box !important; }
    .wa-green { background-color: #25D366 !important; color: #ffffff !important; }
    .wa-blue { background-color: #1e90ff !important; color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🇯🇵 Nihongo Guild Network")

# --- LOCAL DATABASE PERSISTENCE STORAGE ENGINE ---
DATA_FILE = "local_scores_ledger.csv"

def get_scores_data():
    if os.path.exists(DATA_FILE):
        try: return pd.read_csv(DATA_FILE)
        except: pass
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
    st.session_state.my_email = ""

if not st.session_state.user_authenticated:
    st.subheader("👋 Welcome to the Guild Arena")
    st.write("Enter your profile name and secure email configuration:")
    
    user_input_name = st.text_input("Profile Display Name / Nickname:", placeholder="e.g., Alex")
    user_input_email = st.text_input("Your Secure Email Address (For Code Backup Receipts):", placeholder="name@example.com")
    st.markdown("---")
    
    with st.expander("➕ Option 1: Invite Friends & Create a Closed Group"):
        st.markdown("<div class='onboarding-card'>Generate a private group access token to invite your inner circle.</div>", unsafe_allow_html=True)
        if st.button("Generate Group Access Token", key="create_group_btn"):
            if user_input_name.strip() and "@" in user_input_email:
                new_group_code = f"G-{random.randint(1000, 9999)}"
                st.session_state.my_name = user_input_name
                st.session_state.my_email = user_input_email
                st.session_state.my_uid = "UID-16728" if user_input_name.strip().lower() == "admin" else f"UID-{random.randint(10000, 99999)}"
                st.session_state.my_group = new_group_code
                st.session_state.user_authenticated = True
                
                # Dynamic secure link creation for email logging delivery verification
                encoded_email = urllib.parse.quote(user_input_email)
                email_trigger_url = f"https://web3forms.com{encoded_email}&message=Your+Nihongo+Guild+Group+Code+Is:+{new_group_code}"
                
                invite_msg = (
                    f"🇯🇵 *Join my private Japanese Learning Arena!* 🥷\n\n"
                    f"Open the app link, choose 'Join Existing Group', and enter our code:\n"
                    f"👉 *Group Code:* {new_group_code}"
                )
                st.session_state.invite_url = f"https://wa.me{urllib.parse.quote(invite_msg)}"
                st.info(f"📩 Code receipt configuration packed for: {user_input_email}")
                st.rerun()
            else:
                st.error("Please fill in both fields correctly (include '@' in your email)!")

    with st.expander("🤝 Option 2: Join an Existing Closed Group"):
        st.markdown("<div class='onboarding-card'>Sync up score metrics with an established circle leaderboard.</div>", unsafe_allow_html=True)
        input_code = st.text_input("Enter Group Code (e.g., G-1234):", key="join_code_field")
        if st.button("Connect Ledger to Group", key="join_group_btn"):
            if user_input_name.strip() and input_code.strip() and "@" in user_input_email:
                st.session_state.my_name = user_input_name
                st.session_state.my_email = user_input_email
                st.session_state.my_uid = "UID-16728" if user_input_name.strip().lower() == "admin" else f"UID-{random.randint(10000, 99999)}"
                st.session_state.my_group = input_code.strip().upper()
                st.session_state.user_authenticated = True
                st.rerun()
            else:
                st.error("Make sure all input fields are valid!")

    with st.expander("📖 Option 3: Simply Start Learning Solo"):
        st.markdown("<div class='onboarding-card'>Track metrics locally on an isolated solo training row timeline.</div>", unsafe_allow_html=True)
        if st.button("Launch Isolated Solo Mode", key="solo_btn"):
            if user_input_name.strip() and "@" in user_input_email:
                st.session_state.my_name = user_input_name
                st.session_state.my_email = user_input_email
                st.session_state.my_uid = "UID-16728" if user_input_name.strip().lower() == "admin" else f"UID-{random.randint(10000, 99999)}"
                st.session_state.my_group = "SOLO"
                st.session_state.user_authenticated = True
                st.rerun()
            else:
                st.error("Please enter your name and email first!")
    st.stop()
# --- SIDEBAR INTERACTIVE MOBILE ACCOUNT MYPAGE PANEL ---
st.sidebar.markdown(f"### 🥷 Profile Account MyPage")

# Profile Image File Selection Layout Block
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = None

uploaded_pic = st.sidebar.file_uploader("Upload Avatar:", type=["png", "jpg", "jpeg"])
if uploaded_pic is not None:
    st.session_state.user_avatar = uploaded_pic

if st.session_state.user_avatar:
    st.sidebar.image(st.session_state.user_avatar, width=90)
else:
    st.sidebar.markdown("🧑‍💻 *Default Avatar Active*")

# Display critical profile metadata variables clearly for mobile viewport configurations
st.sidebar.write(f"👤 Name: **{st.session_state.my_name}**")
st.sidebar.write(f"📧 Email: `{st.session_state.my_email}`")
st.sidebar.write(f"🆔 Token ID: `{st.session_state.my_uid}`")
st.sidebar.write(f"🛡️ Room Space: **{st.session_state.my_group}**")

# Unblocked WhatsApp Action Redirect HTML Element Links
if st.session_state.my_group != "SOLO" and "invite_url" in st.session_state:
    st.sidebar.markdown(f'<a href="{st.session_state.invite_url}" target="_blank" class="mobile-btn wa-green">📲 Invite Circle Friends</a>', unsafe_allow_html=True)

st.sidebar.markdown(f'<a href="{GLOBAL_COMMUNITY_URL}" target="_blank" class="mobile-btn wa-blue">🌐 Global Community Channels</a>', unsafe_allow_html=True)

if st.sidebar.button("🔄 Logout / Switch Configuration Profile"):
    st.session_state.user_authenticated = False
    st.session_state.my_name = ""
    st.session_state.my_uid = ""
    st.session_state.my_group = "SOLO"
    st.rerun()

# --- MOTIVATIONAL SIDEBAR BULLETIN BOARD ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 📜 Arena Notification Board")

my_total_correct = 0
if not scores_df.empty:
    my_records = scores_df[scores_df["User_ID"] == st.session_state.my_uid]
    if not my_records.empty:
        my_total_correct = pd.to_numeric(my_records["Correct"]).sum()

if st.session_state.my_group == "SOLO":
    bulletin_text = "🎯 **Training Phase Active.** Complete more quiz matches to start compiling metrics!" if my_total_correct < 10 else "🔥 **Blazing Pace!** Keep challenging yourself to unlock higher tier title credentials."
else:
    group_totals = scores_df[scores_df["Group_Code"] == st.session_state.my_group] if not scores_df.empty else pd.DataFrame()
    if not group_totals.empty:
        group_totals["Correct"] = pd.to_numeric(group_totals["Correct"])
        group_summary = group_totals.groupby("User_ID")["Correct"].sum().reset_index()
        top_group_score = group_summary["Correct"].max()
        
        if my_total_correct >= top_group_score and my_total_correct > 0:
            bulletin_text = "👑 **Arena Apex Leader!** You hold the crown inside this private lobby tracker network right now."
        else:
            deficit = int(top_group_score - my_total_correct)
            bulletin_text = f"⚔️ **Opponent Ahead!** You are currently trailing the room leader by **{deficit} points**. Run a challenge to close the margin!"
    else:
        bulletin_text = "💤 **Lobby silent.** Broadcast the invite link above to trigger active match tracking records."

st.sidebar.markdown(f'<div class="bulletin-box">{bulletin_text}</div>', unsafe_allow_html=True)

# --- SECURE CONTENT ADMIN MODULE PANEL ---
if st.session_state.my_uid == "UID-16728":
    with st.sidebar.expander("🛠️ Admin Controls"):
        admin_password = st.text_input("Admin Password:", type="password", key="admin_pwd_field")
        if admin_password == "Gaikokujin":
            st.success("Developer Access Enabled")

# --- INITIALIZE TAB SECTIONS DISPLAY CONSOLE ---
tab1, tab2, tab3 = st.tabs(["🏆 Scoreboard", "⚔️ Quiz Room", "📈 Progress Journey"])
# --- TAB 1: GAMIFIED ENGAGING SCOREBOARD ---
with tab1:
    if st.session_state.my_group == "SOLO":
        st.info("Log into a multiplayer space group code to review rival metric standings.")
    else:
        st.subheader(f"👑 Room Standings: {st.session_state.my_group}")
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
            st.subheader("👀 Historic Room Logs")
            st.dataframe(group_df[["Timestamp", "Name", "Topic", "Correct", "Incorrect"]], use_container_width=True, hide_index=True)
        else:
            st.info("No recorded score logs inside this space yet. Throw a link challenge to initialize data tracking rows!")

# --- TAB 2: ACTIVE QUIZ ROOM WITH TARGETED COMPREHENSION REDIRECT SHARE LINKS ---
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
            <span style="font-weight: bold; font-size:12px; letter-spacing:1px;">CHALLENGE {q_idx + 1} OF 10</span>
            <h3>{row['Question']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            ans_A = st.button(f"A) {row['options']}", key=f"qa_A_{q_idx}", disabled=st.session_state.show_explanation)
            ans_C = st.button(f"C) {row['options']}", key=f"qa_C_{q_idx}", disabled=st.session_state.show_explanation)
        with col2:
            ans_B = st.button(f"B) {row['options']}", key=f"qa_B_{q_idx}", disabled=st.session_state.show_explanation)
            ans_D = st.button(f"D) {row['options']}", key=f"qa_D_{q_idx}", disabled=st.session_state.show_explanation)
            
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
                <h4>{status_color} • Concept Analysis</h4>
                <p><strong>Target Word:</strong> {row['word']}</p>
                <p><strong>Exact Meaning:</strong> {row['meaning']}</p>
                <p><strong>Breakdown Rules:</strong> {row['desc']}</p>
                <p style="background:#0f0f12; padding:10px; border-radius:8px; border-left:3px solid #ffa500;"><strong>💡 Practice Sentence Example:</strong><br><em>{row['example']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Next Challenge ➡️", key="next_q_btn"):
                st.session_state.quiz_index += 1
                st.session_state.show_explanation = False
                st.rerun()
                
        # High-impact unblocked viral loop structure to acquire new active user profiles
        peer_challenge_msg = (
            f"⚔️ *Nihongo Peer Challenge Duel!* 🥷\n\n"
            f"From player: {st.session_state.my_name} (Room: {st.session_state.my_group})\n\n"
            f"👉 *Challenge Question:* \"{row['Question']}\"\n\n"
            f"Think you can pass me? Tap our app link to enter our room or train solo:\n"
            f"🔗 https://streamlit.app"
        )
        st.markdown(f'<a href="https://wa.me{urllib.parse.quote(peer_challenge_msg)}" target="_blank" class="mobile-btn wa-green">🚀 Throw Challenge & Invite to Room</a>', unsafe_allow_html=True)
        
    else:
        st.success("🏁 Set Finished Successfully!")
        st.write(f"✅ Total Right: **{st.session_state.run_correct}**")
        st.write(f"❌ Total Missed: **{st.session_state.run_incorrect}**")
        
        if st.button("Save & Upload Results to Ledger Scoreboard"):
            save_score_locally(
                st.session_state.my_uid, 
                st.session_state.my_name, 
                st.session_state.my_group, 
                st.session_state.run_correct, 
                st.session_state.run_incorrect
            )
            st.success("Scores synced safely into local repository ledger storage database file!")
            del st.session_state.quiz_index
            del st.session_state.run_correct
            del st.session_state.run_incorrect
            st.rerun()

# --- TAB 3: PERSONAL PROGRESS TRACKING JOURNEY ENGINE ---
with tab3:
    st.subheader("📈 My Personal Mastery Journey")
    
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
        with c1: st.metric(label="Lifetime Right Answers", value=f"{total_my_correct} ✅")
        with c2: st.metric(label="Overall Accuracy Ratio", value=f"{accuracy_ratio}% 🎯")
            
        st.markdown("### 🔓 Guild Achievements & Trophies")
        if total_my_correct >= 1:
            st.success("🔰 **UNLOCKED: First Victory** (Logged your first correct answer in the arena!)")
        else:
            st.markdown("<div style='border:1px dashed #444; padding:10px; border-radius:8px; color:#666;'>🔒 *First Victory (Get 1 question right to unlock)*</div>", unsafe_allow_html=True)
            
        if total_my_correct >= 100:
            st.success("👑 **UNLOCKED: Centurion Warrior** (Massive Dedication! Passed 100 correct entries!)")
        else:
            st.markdown(f"<div style='border:1px dashed #444; padding:10px; border-radius:8px; color:#666;'>🔒 *Centurion Warrior ({total_my_correct}/100 questions correct)*</div>", unsafe_allow_html=True)
            
        if accuracy_ratio >= 85.0 and total_attempts >= 10:
            st.success(f"🎯 **UNLOCKED: Flawless Striker** (Maintained a superb precision accuracy of {accuracy_ratio}%)")
        else:
            st.markdown(f"<div style='border:1px dashed #444; padding:10px; border-radius:8px; color:#666;'>🔒 *Flawless Striker (Maintain 85%+ accuracy with at least 10 attempts. Current: {accuracy_ratio}%)*</div>", unsafe_allow_html=True)
        st.write("")

        st.markdown("### 📊 Accuracy Progress Over Time")
        my_history_df["Cumulative_Correct"] = my_history_df["Correct"].cumsum()
        st.line_chart(my_history_df, x="Timestamp", y="Cumulative_Correct", color="#1e90ff")
    else:
        st.info("Complete your first quiz evaluation run to map your performance progress dashboard timeline.")
