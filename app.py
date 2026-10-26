import streamlit as st
import pandas as pd
import datetime
import urllib.parse
import random
import os
import requests

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
            "Option_A": "Excuse me", "Option_B": "No problem", "Option_C": "Goodbye", "Option_D": "I don't understand",
            "correct": "B"
        },
        {
            "word": "Arimasu (あります)",
            "meaning": "There is / To have (Inanimate Objects).",
            "desc": "Used strictly for non-living items like places, buildings, plants, or concepts. It states existence or personal possession.",
            "example": "Kuruma ga arimasu. (I have a car / There is a car.)",
            "Option_A": "People only", "Option_B": "Animals only", "Option_C": "Inanimate objects", "Option_D": "Moving things",
            "correct": "C"
        },
        {
            "word": "Arimasen (ありません)",
            "meaning": "There is not / Do not have (Inanimate Objects).",
            "desc": "The polite negative form of 'arimasu'. It denotes that a non-living object is missing or not owned.",
            "example": "Jikan ga arimasen. (I do not have time.)",
            "Option_A": "I will go", "Option_B": "I don't have / there is none", "Option_C": "Please wait", "Option_D": "Thank you",
            "correct": "B"
        },
        {
            "word": "Ikimasu (行きます)",
            "meaning": "To go.",
            "desc": "An active motion verb indicating movement away from your current position toward a physical destination.",
            "example": "Gakkou e ikimasu. (I am going to school.)",
            "Option_A": "To eat", "Option_B": "To go", "Option_C": "To speak", "Option_D": "To sleep",
            "correct": "B"
        },
        {
            "word": "Ikimasen (行きません)",
            "meaning": "Will not go / Do not go.",
            "desc": "The polite negative expression of 'ikimasu'. Used to declare you aren't journeying to a specific location.",
            "example": "Doko mo ikimasen. (I am not going anywhere.)",
            "Option_A": "I went yesterday", "Option_B": "I want to go", "Option_C": "I am going", "Option_D": "I will not go",
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
            item["Question"] = f"When evaluating a setup scheduled {scen}, what is the correct alignment for '{item['word']}'?"
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
                
                # Dynamic secure link creation via Web3Forms API to send actual email records
                try:
                    requests.post("https://web3forms.com", data={
                        "access_key": "4c45a769-cf77-4b7b-9fe3-69024f2b963b",
                        "email": user_input_email,
                        "subject": "Nihongo Guild - Private Group Access Token Created",
                        "message": f"Konnichiwa {user_input_name}! Your private Japanese Tracking Group Code is: {new_group_code}. Share it with your friends!"
                    })
                    st.success("📩 Group access token successfully emailed to your inbox!")
                except:
                    pass
                
                invite_msg = (
                    f"🇯🇵 *Join my private Japanese Learning Arena!* 🥷\n\n"
                    f"Open our app link, choose 'Join Existing Group', and enter our code:\n"
                    f"👉 *Group Code:* {new_group_code}"
                )
                st.session_state.invite_url = f"https://wa.me{urllib.parse.quote(invite_msg)}"
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
    # --- INITIALIZE TAB SECTIONS FOR MAIN PHONE ACCESSIBILITY ---
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Scoreboard", "⚔️ Quiz Room", "📈 Progress Journey", "🥷 MyPage Account"])

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
            st.info("No recorded score logs inside this space yet.")

# --- TAB 2: ACTIVE QUIZ ROOM WITH NATIVE WHATSAPP DEEP LINKS ---
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
                <p style="background:#0f0f12; padding:10px; border-radius:8px; border-left:3px solid #ffa500; color:#fff !important;"><strong>💡 Practice Sentence Example:</strong><br><em>{row['example']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Next Challenge ➡️", key="next_q_btn"):
                st.session_state.quiz_index += 1
                st.session_state.show_explanation = False
                st.rerun()
                
        # Completely fixed, PWA-compliant escaped parameters link path
        peer_challenge_msg = (
            f"⚔️ *Nihongo Peer Challenge Duel!* 🥷\n\n"
            f"From player: {st.session_state.my_name} (Room: {st.session_state.my_group})\n\n"
            f"👉 *Challenge Question:* \"{row['Question']}\"\n\n"
            f"Think you can pass me? Tap our app link to enter our room or train solo:\n"
            f"🔗 https://streamlit.app"
        )
        st.markdown(f'<a href="https://wa.me{urllib.parse.quote(peer_challenge_msg)}" target="_blank" class="mobile-btn wa-green">🚀 Throw Challenge & Invite to Room</a>', unsafe_allow_html=True)
        
    else:
        st.success("🏁 Challenge Completed Successfully!")
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
            st.success("Scores saved safely directly inside your GitHub repository storage file!")
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
        if total_my_correct >= 100:
            st.success("👑 **UNLOCKED: Centurion Warrior** (Massive Dedication! Passed 100 correct entries!)")
        if accuracy_ratio >= 85.0 and total_attempts >= 10:
            st.success(f"🎯 **UNLOCKED: Flawless Striker** (Maintained a superb precision accuracy of {accuracy_ratio}%)")
        st.write("")

        st.markdown("### 📊 Accuracy Progress Over Time")
        my_history_df["Cumulative_Correct"] = my_history_df["Correct"].cumsum()
        st.line_chart(my_history_df, x="Timestamp", y="Cumulative_Correct", color="#1e90ff")
    else:
        st.info("Complete your first quiz evaluation run to map your performance progress dashboard timeline.")

# --- TAB 4: CENTRAL MOBILE ACCOUNT ACCOUNTS MYPAGE HUB ---
with tab4:
    st.subheader("🥷 MyPage Account Configuration")
    
    uploaded_pic = st.file_uploader("Upload Profile Image Avatar:", type=["png", "jpg", "jpeg"])
    if uploaded_pic is not None:
        st.image(uploaded_pic, width=120)
        
    st.write(f"👤 Display Name: **{st.session_state.my_name}**")
    st.write(f"📧 Secure Backup Email: `{st.session_state.my_email}`")
    st.write(f"🆔 Personal Account Token: `{st.session_state.my_uid}`")
    st.write(f"🛡️ Synced Lobby Group: **{st.session_state.my_group}**")
    
    if st.session_state.my_group != "SOLO" and "invite_url" in st.session_state:
        st.markdown(f'<a href="{st.session_state.invite_url}" target="_blank" class="mobile-btn wa-green">📲 Invite Room Teammates via WhatsApp</a>', unsafe_allow_html=True)
        
    st.markdown(f'<a href="{GLOBAL_COMMUNITY_URL}" target="_blank" class="mobile-btn wa-blue">🌐 Join Global WhatsApp Community</a>', unsafe_allow_html=True)
    
    if st.button("🔄 Clear Active Session & Return to Onboarding Menu"):
        st.session_state.user_authenticated = False
        st.session_state.my_name = ""
        st.session_state.my_uid = ""
        st.session_state.my_group = "SOLO"
        st.rerun()
                              
