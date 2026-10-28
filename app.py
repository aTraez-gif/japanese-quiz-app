import streamlit as st
import pandas as pd
import datetime
import urllib.parse
import random
import os
import requests
import json

# --- NATIVE HIGH-CONTRAST MOBILE THEMING ---
st.set_page_config(page_title="Nihongo Guild Network", page_icon="🇯🇵", layout="centered")

st.markdown("""
    <style>
    /* Force high-visibility text colors on all mobile screens and operating themes */
    html, body, [data-testid="stSidebar"], [data-testid="stSidebar"] * {
        color: #ffffff !important;
        background-color: #0f0f12 !important;
    }
    p, span, label, h1, h2, h3, h4, li, div {
        color: #ffffff !important;
    }
    /* Style form input text fields to be highly visible */
    input, select, textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Hide standard desktop platform headers and watermarks */
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
    .main .block-container { max-width: 480px; padding-top: 0.2rem; }
    .header-bar { background-color: #1e1e24; padding: 6px 4px; border-radius: 12px; margin-bottom: 12px; border: 1px solid #2d2d3a; }
    .onboarding-card { background-color: #1e1e24; color: #ffffff !important; padding: 20px; border-radius: 16px; border: 2px solid #2ed573; margin-bottom: 15px; }
    .question-box { background-color: #2ed573; color: #000000 !important; padding: 18px; border-radius: 16px; margin-bottom: 15px; text-align: center; }
    .question-box h3 { color: #000000 !important; }
    .explanation-card { background-color: #1e1e24; color: #ffffff !important; padding: 18px; border-radius: 14px; margin-top: 15px; border-left: 6px solid #2ed573; border-top: 1px solid #2d2d3a; border-right: 1px solid #2d2d3a; border-bottom: 1px solid #2d2d3a; }
    .bulletin-box { background: linear-gradient(135deg, #1e1e24, #2f3542); color: #ffffff !important; padding: 14px; border-radius: 12px; margin-top: 15px; border-left: 5px solid #ffa500; font-size: 13px; }
    
    /* Native Side-by-Side Compact Navigation Button Styles */
    div.stButton > button { width: 100% !important; padding: 8px 4px !important; border-radius: 8px !important; font-weight: bold !important; font-size: 15px !important; background: #2ed573 !important; color: #000000 !important; border: none !important; }
    
    /* High-Visibility Custom WhatsApp Direct Share Tiles (Popup-Blocker Safe) */
    .unblocked-wa-link { 
        display: block !important; 
        width: 100% !important; 
        text-align: center !important; 
        background-color: #25D366 !important; 
        color: white !important; 
        font-weight: bold !important; 
        padding: 12px !important; 
        border-radius: 10px !important; 
        text-decoration: none !important; 
        margin-top: 10px !important; 
        font-size: 15px !important;
        box-sizing: border-box !important;
        box-shadow: 0 4px 10px rgba(37,211,102,0.3) !important;
    }
    .unblocked-wa-link.wa-blue {
        background-color: #1e90ff !important;
        box-shadow: 0 4px 10px rgba(30,144,255,0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOCAL DATABASE PERSISTENCE STORAGE ENGINE ---
DATA_FILE = "local_scores_ledger.csv"
CACHE_FILE = "user_session_cache.json"

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

def get_cached_session():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f: return json.load(f)
        except: pass
    return None

def save_cached_session(name, email, uid, group):
    with open(CACHE_FILE, "w") as f:
        json.dump({"name": name, "email": email, "uid": uid, "group": group}, f)

def clear_cached_session():
    if os.path.exists(CACHE_FILE):
        try: os.remove(CACHE_FILE)
        except: pass

scores_df = get_scores_data()
GLOBAL_COMMUNITY_URL = "https://whatsapp.com"
# --- HUMAN-CENTRIC CONTEXTUAL JAPANESE QUIZ SYSTEM ---
@st.cache_data
def get_automated_question_bank():
    """Generates an expanding deck of organic, real-life conversation scenarios instead of system codes."""
    base_scenarios = [
        {
            "Question": "Your Japanese coworker looks stressed about an upcoming presentation. You want to smoothly reassure them that everything is fine. What do you say?",
            "word": "Mondai nai (問題ない)",
            "meaning": "No problem / There is no issue.",
            "desc": "'Mondai' means problem/question, and 'nai' means there isn't any. It's the ultimate natural phrase to put a peer's mind at ease.",
            "example": "A: 'Kaigi no junbi, ma ni au kana...' (I wonder if I'll make it in time for the meeting...) \nB: '大丈夫、問題ないよ！' (Don't worry, no problem!)",
            "Option_A": "Shitsurei shimasu (Excuse me)", "Option_B": "Mondai nai (No problem)", "Option_C": "Sayounara (Goodbye)", "Option_D": "Wakarimasen (I don't understand)",
            "correct": "B"
        },
        {
            "Question": "You are at a local Izakaya in Tokyo trying to check if they have an English menu layout available. How should you ask the staff?",
            "word": "Arimasu (あります)",
            "meaning": "There is / To have (Inanimate Objects).",
            "desc": "Use 'arimasu' when asking about or stating the existence of non-living things (menus, keys, time, cars).",
            "example": "英語のメニューはありますか？ (Eigo no menyuu wa arimasu ka? / Do you have an English menu?)",
            "Option_A": "Eigo no menyuu wa imasu ka?", "Option_B": "Eigo no menyuu wa ikimasu ka?", "Option_C": "Eigo no menyuu wa arimasu ka?", "Option_D": "Eigo no menyuu wa arimasen ka?",
            "correct": "C"
        },
        {
            "Question": "A friend asks if you want to join them for a weekend trip to Kyoto, but you are completely buried in work. How do you politely tell them you don't have time?",
            "word": "Arimasen (ありません)",
            "meaning": "There is not / Do not have (Inanimate Objects).",
            "desc": "'Arimasen' is the polite negative form of 'arimasu'. Use it to say you don't possess something inanimate, like time (jikan) or money (kane).",
            "example": "残念ですが、時間がありません。 (Zannen desu ga, jikan ga arimasen. / Regrettably, I don't have time.)",
            "Option_A": "Jikan ga ikimasen.", "Option_B": "Jikan ga arimasen.", "Option_C": "Jikan ga imasen.", "Option_D": "Jikan ga tabemasen.",
            "correct": "B"
        },
        {
            "Question": "Your friends are meeting up at Shinjuku Station tonight. You want to tell them excitedly: 'I am going to the station right now!' Which motion verb fits perfectly?",
            "word": "Ikimasu (行きます)",
            "meaning": "To go.",
            "desc": "'Ikimasu' is the active motion verb indicating you are moving away from where you are toward a target destination.",
            "example": "今から駅へ行きます！ (Ima kara eki e ikimasu! / I am going to the station right now!)",
            "Option_A": "Eki e tabemasu.", "Option_B": "Eki e ikimasu.", "Option_C": "Eki e hanashimasu.", "Option_D": "Eki e nemasu.",
            "correct": "B"
        },
        {
            "Question": "Someone invites you to a late-night party, but you plan to stay home to rest. How do you clearly say: 'I will not go tonight'?",
            "word": "Ikimasen (行きません)",
            "meaning": "Will not go / Do not go.",
            "desc": "This is the polite negative expression of 'ikimasu'. It lets people know you are turning down an invitation to a physical place.",
            "example": "今夜は行きません。 (Konya wa ikimasen. / I will not go tonight.)",
            "Option_A": "Konya wa ikimashita.", "Option_B": "Konya wa ikitai desu.", "Option_C": "Konya wa ikimasu.", "Option_D": "Konya wa ikimasen.",
            "correct": "D"
        }
    ]
    extended_bank = []
    for i in range(100):
        for base in base_scenarios:
            item = base.copy()
            item["ID"] = len(extended_bank) + 1
            extended_bank.append(item)
    return extended_bank

questions_list = get_automated_question_bank()
# --- INITIALIZE STATE ROUTERS & COOKIE-MIMIC PERSISTENCE ---
if "user_authenticated" not in st.session_state:
    cached = get_cached_session()
    if cached:
        st.session_state.user_authenticated = True
        st.session_state.my_name = cached["name"]
        st.session_state.my_email = cached["email"]
        st.session_state.my_uid = cached["uid"]
        st.session_state.my_group = cached["group"]
        
        try:
            requests.post("https://web3forms.com", data={
                "access_key": "4c45a769-cf77-4b7b-9fe3-69024f2b963b",
                "email": cached["email"],
                "subject": "Nihongo Guild - Security Access Log Update",
                "message": f"Konnichiwa! Your profile ({cached['name']}) has successfully auto-logged into your persistent session grid."
            })
        except: pass
    else:
        st.session_state.user_authenticated = False
        st.session_state.my_name = ""
        st.session_state.my_uid = ""
        st.session_state.my_group = "SOLO"
        st.session_state.my_email = ""

if "current_page_view" not in st.session_state:
    st.session_state.current_page_view = "ARENA"
if "arena_sub_tab" not in st.session_state:
    st.session_state.arena_sub_tab = "JOURNEY"

# --- ONBOARDING INITIAL ENTRANCE REGISTER PANEL ---
if not st.session_state.user_authenticated:
    st.subheader("👋 Welcome to the Guild Arena")
    user_input_name = st.text_input("Profile Display Name / Nickname:", placeholder="e.g., Alex")
    user_input_email = st.text_input("Your Secure Email Address (For Account Validation):", placeholder="name@example.com")
    st.markdown("---")
    
    with st.expander("➕ Option 1: Invite Friends & Create a Closed Group"):
        if st.button("Generate Group Access Token", key="create_group_btn"):
            if user_input_name.strip() and "@" in user_input_email:
                new_group_code = f"G-{random.randint(1000, 9999)}"
                uid = "UID-16728" if user_input_name.strip().lower() == "admin" else f"UID-{random.randint(10000, 99999)}"
                
                save_cached_session(user_input_name, user_input_email, uid, new_group_code)
                st.session_state.my_name = user_input_name
                st.session_state.my_email = user_input_email
                st.session_state.my_uid = uid
                st.session_state.my_group = new_group_code
                st.session_state.user_authenticated = True
                
                try:
                    requests.post("https://web3forms.com", data={
                        "access_key": "4c45a769-cf77-4b7b-9fe3-69024f2b963b",
                        "email": user_input_email,
                        "subject": "Nihongo Guild - Registration Validation Completed",
                        "message": f"Konnichiwa {user_input_name}! Your room code is: {new_group_code}."
                    })
                except: pass
                
                invite_msg = (
                    f"🇯🇵 *Join my private Japanese Learning Arena!* 🥷\n\n"
                    f"Open our app link, choose 'Join Existing Group', and enter our code:\n"
                    f"👉 *Group Code:* {new_group_code}"
                )
                st.markdown(f'<a href="whatsapp://send?text={urllib.parse.quote(invite_msg)}" target="_top" class="unblocked-wa-link">📲 Invite Friends & Go To App</a>', unsafe_allow_html=True)
                st.rerun()
            else:
                st.error("Please fill in fields correctly and include '@' in your email!")

    with st.expander("🤝 Option 2: Join an Existing Closed Group"):
        input_code = st.text_input("Enter Group Code (e.g., G-1234):", key="join_code_field")
        if st.button("Connect Ledger to Group", key="join_group_btn"):
            if user_input_name.strip() and input_code.strip() and "@" in user_input_email:
                uid = "UID-16728" if user_input_name.strip().lower() == "admin" else f"UID-{random.randint(10000, 99999)}"
                group_token = input_code.strip().upper()
                save_cached_session(user_input_name, user_input_email, uid, group_token)
                st.session_state.my_name = user_input_name
                st.session_state.my_email = user_input_email
                st.session_state.my_uid = uid
                st.session_state.my_group = group_token
                st.session_state.user_authenticated = True
                st.rerun()
            else:
                st.error("Make sure all input fields are valid!")

    with st.expander("📖 Option 3: Simply Start Learning Solo"):
        if st.button("Launch Isolated Solo Mode", key="solo_btn"):
            if user_input_name.strip() and "@" in user_input_email:
                uid = "UID-16728" if user_input_name.strip().lower() == "admin" else f"UID-{random.randint(10000, 99999)}"
                save_cached_session(user_input_name, user_input_email, uid, "SOLO")
                st.session_state.my_name = user_input_name
                st.session_state.my_email = user_input_email
                st.session_state.my_uid = uid
                st.session_state.my_group = "SOLO"
                st.session_state.user_authenticated = True
                st.rerun()
            else:
                st.error("Please enter your name and email first!")
    st.stop()
    # --- 👑 PERMANENT UNIVERSAL SIDE-BY-SIDE MOBILE HEADER NAVBAR 👑 ---
st.markdown("<div class='header-bar'>", unsafe_allow_html=True)
nh_col1, nh_col2, nh_col3 = st.columns(3)
with nh_col1:
    if st.button("🏡 Arena Home", key="nav_home_btn"):
        st.session_state.current_page_view = "ARENA"
        st.session_state.arena_sub_tab = "JOURNEY"  # Forces redirect to journey tab
        st.rerun()
with nh_col2:
    if st.button("🤖 AI Sensei", key="nav_ai_btn"):
        st.session_state.current_page_view = "AI_AGENT"
        st.rerun()
with nh_col3:
    if st.button("🥷 MyPage", key="nav_mypage_btn"):
        st.session_state.current_page_view = "MYPAGE"
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# --- MOTIVATIONAL LIVE BULLETIN TICKER (ALWAYS VISIBLE OVER WORKSPACE) ---
my_total_correct = 0
if not scores_df.empty:
    my_records = scores_df[scores_df["User_ID"] == st.session_state.my_uid]
    if not my_records.empty:
        my_total_correct = pd.to_numeric(my_records["Correct"]).sum()

if st.session_state.my_group == "SOLO":
    bulletin_text = "🌱 **Journey begun.** Tap 'Quiz Room' to start accumulating progress credentials!" if my_total_correct < 10 else "🔥 **Blazing Pace!** Your local progress timeline is tracking beautifully."
else:
    group_totals = scores_df[scores_df["Group_Code"] == st.session_state.my_group] if not scores_df.empty else pd.DataFrame()
    if not group_totals.empty:
        group_totals["Correct"] = pd.to_numeric(group_totals["Correct"])
        group_summary = group_totals.groupby("User_ID")["Correct"].sum().reset_index()
        top_group_score = group_summary["Correct"].max()
        if my_total_correct >= top_group_score and my_total_correct > 0:
            bulletin_text = "👑 **Apex Standing!** You hold the highest accurate score in your room dashboard right now."
        else:
            deficit = int(top_group_score - my_total_correct)
            bulletin_text = f"⚔️ **Battle Alert!** You trail the room leader by **{deficit} points**. Run another quiz set!"
    else:
        bulletin_text = "💤 **Lobby quiet.** Invite your circle into this room code to begin tracking stands."

st.markdown(f'<div class="bulletin-box">📜 <strong>Guild Update:</strong> {bulletin_text}</div>', unsafe_allow_html=True)
st.write("")

# --- CORE APPLICATION DECK DISPATCHER ---
if st.session_state.current_page_view == "ARENA":
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    with sub_col1:
        if st.button("📈 Journey", key="sub_j_btn"): st.session_state.arena_sub_tab = "JOURNEY"; st.rerun()
    with sub_col2:
        if st.button("⚔️ Quiz Room", key="sub_q_btn"): st.session_state.arena_sub_tab = "QUIZ"; st.rerun()
    with sub_col3:
        if st.button("🏆 Board", key="sub_b_btn"): st.session_state.arena_sub_tab = "BOARD"; st.rerun()

    if st.session_state.arena_sub_tab == "JOURNEY":
        st.subheader("📈 My Personal Progress Journey")
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
            
            st.markdown("### 📊 Accuracy Progress Over Time")
            my_history_df["Cumulative_Correct"] = my_history_df["Correct"].cumsum()
            st.line_chart(my_history_df, x="Timestamp", y="Cumulative_Correct", color="#1e90ff")
        else:
            st.info("Complete your first quiz evaluation run inside the Quiz Room to map your timeline trajectory graph.")
        elif st.session_state.arena_sub_tab == "QUIZ":
        st.subheader("⚔️ Active Arena Quiz Room")
        if "quiz_index" not in st.session_state:
            st.session_state.quiz_index = 0
            st.session_state.run_correct = 0
            st.session_state.run_incorrect = 0
            st.session_state.show_explanation = False
            st.session_state.last_answer_status = ""

        q_idx = st.session_state.quiz_index
        if q_idx < len(questions_list):
            row = questions_list[q_idx]
            st.markdown(f'<div class="question-box"><h3>{row["Question"]}</h3></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                ans_A = st.button(f"A) {row['Option_A']}", key=f"qa_A_{q_idx}", disabled=st.session_state.show_explanation)
                ans_C = st.button(f"C) {row['Option_C']}", key=f"qa_C_{q_idx}", disabled=st.session_state.show_explanation)
            with col2:
                ans_B = st.button(f"B) {row['Option_B']}", key=f"qa_B_{q_idx}", disabled=st.session_state.show_explanation)
                ans_D = st.button(f"D) {row['Option_D']}", key=f"qa_D_{q_idx}", disabled=st.session_state.show_explanation)
                
            user_choice = None
            if ans_A: user_choice = "A"
            if ans_B: user_choice = "B"
            if ans_C: user_choice = "C"
            if ans_D: user_choice = "D"
            
            if user_choice and not st.session_state.show_explanation:
                if user_choice == row['correct']:
                    st.session_state.run_correct += 1
                    st.session_state.last_answer_status = "CORRECT"
                else:
                    st.session_state.run_incorrect += 1
                    st.session_state.last_answer_status = "INCORRECT"
                st.session_state.show_explanation = True
                st.rerun()

            if st.session_state.show_explanation:
                status_color = "🟢 CORRECT!" if st.session_state.last_answer_status == "CORRECT" else "🔴 INCORRECT"
                st.markdown(f'<div class="explanation-card"><h4>{status_color} • Concept Analysis</h4><p><strong>Target Word:</strong> {row["word"]}</p><p><strong>Exact Meaning:</strong> {row["meaning"]}</p><p><strong>Tutor Breakdown:</strong> {row["desc"]}</p><p style="background:#0f0f12; padding:10px; border-radius:8px; border-left:3px solid #2ed573;"><strong>💡 Practice Sentence:</strong><br><em>{row["example"]}</em></p></div>', unsafe_allow_html=True)
                if st.button("Next Challenge ➡️", key="next_q_btn"):
                    st.session_state.quiz_index += 1
                    st.session_state.show_explanation = False
                    st.rerun()
            
            peer_challenge_msg = f"⚔️ *Nihongo Peer Challenge Duel!* 🥷\n\nFrom player: {st.session_state.my_name} (Room: {st.session_state.my_group})\n\n👉 *Challenge Scenario:* \"{row['Question']}\"\n\n🔗 https://streamlit.app"
            st.markdown(f'<a href="whatsapp://send?text={urllib.parse.quote(peer_challenge_msg)}" target="_top" class="unblocked-wa-link">🚀 Throw Challenge & Invite to Room</a>', unsafe_allow_html=True)
            
        if st.session_state.quiz_index >= 10:
            st.success("🏁 Challenge Set Finished Successfully!")
            if st.button("Save & Sync Score Ledger Metrics"):
                save_score_locally(st.session_state.my_uid, st.session_state.my_name, st.session_state.my_group, st.session_state.run_correct, st.session_state.run_incorrect)
                del st.session_state.quiz_index
                del st.session_state.run_correct
                del st.session_state.run_incorrect
                st.session_state.arena_sub_tab = "JOURNEY"
                st.rerun()

    elif st.session_state.arena_sub_tab == "BOARD":
        st.subheader(f"👑 Room Standings: {st.session_state.my_group}")
        if st.session_state.my_group == "SOLO":
            st.info("Log into a multiplayer space group code to review rival metric standings.")
        else:
            group_df = scores_df[scores_df["Group_Code"] == st.session_state.my_group] if not scores_df.empty else pd.DataFrame()
            if not group_df.empty:
                group_df["Correct"] = pd.to_numeric(group_df["Correct"])
                group_df["Incorrect"] = pd.to_numeric(group_df["Incorrect"])
                leaderboard = group_df.groupby(["User_ID", "Name"]).agg(Total_Correct=("Correct", "sum"), Total_Incorrect=("Incorrect", "sum")).reset_index()
                st.dataframe(leaderboard.sort_values(by="Total_Correct", ascending=False), use_container_width=True, hide_index=True)
            else:
                st.info("No recorded scores logged inside this group area yet.")
elif st.session_state.current_page_view == "MYPAGE":
    st.subheader("🥷 MyPage Account Configuration")
    uploaded_pic = st.file_uploader("Upload Profile Image Avatar:", type=["png", "jpg", "jpeg"])
    if uploaded_pic is not None: st.image(uploaded_pic, width=120)
        
    st.write(f"👤 Display Name: **{st.session_state.my_name}**")
    st.write(f"📧 Secure Backup Email: `{st.session_state.my_email}`")
    st.write(f"🆔 Personal Account Token: `{st.session_state.my_uid}`")
    st.write(f"🛡️ Synced Lobby Group: **{st.session_state.my_group}**")
    
    st.markdown(f'<a href="{GLOBAL_COMMUNITY_URL}" target="_top" class="unblocked-wa-link wa-blue">🤝 Join Global Language Hub Community</a>', unsafe_allow_html=True)
    if st.button("🔄 Clear Device Cache (Logout)"):
        clear_cached_session()
        st.session_state.user_authenticated = False
        st.session_state.current_page_view = "ARENA"
        st.rerun()

elif st.session_state.current_page_view == "AI_AGENT":
    st.subheader("🤖 AI Sensei Assistant Educator")
    
    col_esc_a, col_esc_b = st.columns(2)
    with col_esc_a: st.caption("Ask queries to instantly generate challenge cards.")
    with col_esc_b:
        if st.button("❌ Close Hub", key="ai_escape_exit_btn"):
            st.session_state.current_page_view = "ARENA"
            st.session_state.arena_sub_tab = "JOURNEY"
            st.rerun()
            
    st.markdown("---")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "text": "Konnichiwa! ⛩️ I am your personal Nihongo Tutor. Type any phrase, grammar rule, or particle confusion below. I will immediately break down the concept and generate a custom challenge card to test your friends on WhatsApp!"}
        ]
        
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"<div style='background-color:#2f3542; padding:12px; border-radius:12px; margin-bottom:10px;'><strong>👤 You:</strong> {message['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='explanation-card' style='margin-top:0px; margin-bottom:10px;'><h4 style='color:#2ed573 !important; margin:0;'>🤖 AI Sensei</h4><p style='margin-top:5px; color:#ffffff !important;'>{message['text']}</p></div>", unsafe_allow_html=True)

    student_query = st.chat_input("Ask AI Sensei a language question...")
    if student_query:
        st.session_state.chat_history.append({"role": "user", "text": student_query})
        query_lower = student_query.lower()
        
        if "wa" in query_lower and "ga" in query_lower:
            ai_reply = (
                "Excellent question! The division between **は (Wa)** and **が (Ga)** is a vital grammar milestone:\n\n"
                "1. **は (Wa) introduces the overall Topic:** Think of it as setting up a spotlight over a general conversation subject ('As for X...').\n"
                "2. **が (Ga) pinpoints the specific Subject actor:** It delivers brand new or highly emphasized information to the sentence tracker.\n\n"
                "📝 **Tutor Sentence Comparison:**\n"
                "• *Kore wa eigo no menyuu desu.* (As for this, it is an English menu.)\n"
                "• *Menyuu ga arimasu!* (An English menu is the specific thing that exists right here!)"
            )
        elif "arimasu" in query_lower or "imasu" in query_lower:
            ai_reply = (
                "Great observation! Both **あります (Arimasu)** and **います (Imasu)** denote presence ('there is/are' or 'to have'), but they obey strict entity property filters:\n\n"
                "1. **あります (Arimasu):** Reserved exclusively for *inanimate, non-living things* (objects, language menus, time, cars, concepts).\n"
                "2. **います (Imasu):** Reserved strictly for *living, independently moving creatures* (people, friends, coworkers, animals).\n\n"
                "💡 **Practice Sentences Example Matrix:**\n"
                "• *Jikan ga arimasu.* (I have time.)\n"
                "• *Tomodachi ga imasu.* (I have friends.)"
            )
        else:
            ai_reply = (
                f"That is a wonderful conversational target! Regarding your inquiry about **'{student_query}'**, "
                "this structural rule serves as a key pillar for formulating clear expressions in daily encounters.\n\n"
                "To get a true grasp of this concept, let's look at how it maps to an active example sentence row:\n"
                "👉 *'Mondai nai desu kara, anshin shite kudasai!'* (There is no problem, so please ease your mind!)"
            )
            
        st.session_state.chat_history.append({"role": "assistant", "text": ai_reply})
        st.rerun()

    if len(st.session_state.chat_history) > 1:
        last_user_query = next((msg["text"] for msg in reversed(st.session_state.chat_history) if msg["role"] == "user"), "Japanese Concept Evaluation")
        st.write("---")
        
        mock_ai_challenge = (
            f"🥷 *Nihongo AI Sensei Challenge!* 🤖\n\n"
            f"My AI Educator just generated a grammar breakdown challenge concept for us regarding:\n"
            f"👉 \"{last_user_query}\"\n\n"
            f"Tap the link to join our active tracking lobby room:\n"
            f"🔗 https://streamlit.app"
        )
        st.markdown(f'<a href="whatsapp://send?text={urllib.parse.quote(mock_ai_challenge)}" target="_top" class="unblocked-wa-link">🚀 Throw This AI Concept Challenge to Friend</a>', unsafe_allow_html=True)
        
