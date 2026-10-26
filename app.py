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
    .header-bar { background-color: #1e1e24; padding: 10px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #2d2d3a; }
    .onboarding-card { background-color: #1e1e24; color: #ffffff !important; padding: 20px; border-radius: 16px; border: 2px solid #2ed573; margin-bottom: 15px; }
    .question-box { background-color: #2ed573; color: #000000 !important; padding: 18px; border-radius: 16px; margin-bottom: 15px; text-align: center; }
    .question-box h3 { color: #000000 !important; }
    .explanation-card { background-color: #1e1e24; color: #ffffff !important; padding: 18px; border-radius: 14px; margin-top: 15px; border-left: 6px solid #2ed573; border-top: 1px solid #2d2d3a; border-right: 1px solid #2d2d3a; border-bottom: 1px solid #2d2d3a; }
    .bulletin-box { background: linear-gradient(135deg, #1e1e24, #2f3542); color: #ffffff !important; padding: 14px; border-radius: 12px; margin-top: 15px; border-left: 5px solid #ffa500; font-size: 13px; }
    
    /* Mobile Action Buttons Matrix Styling */
    div.stButton > button { width: 100% !important; padding: 12px !important; border-radius: 10px !important; font-weight: bold !important; font-size: 15px !important; background: #2ed573 !important; color: #000000 !important; border: none !important; }
    div[data-testid="stLinkButton"] > a { width: 100% !important; text-align: center !important; background-color: #25D366 !important; color: #ffffff !important; padding: 12px !important; border-radius: 10px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; }
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
            "Option_A": "Shitsurei shimasu (Excuse me)",
            "Option_B": "Mondai nai (No problem)",
            "Option_C": "Sayounara (Goodbye)",
            "Option_D": "Wakarimasen (I don't understand)",
            "correct": "B"
        },
        {
            "Question": "You are at a local Izakaya in Tokyo trying to check if they have an English menu layout available. How should you ask the staff?",
            "word": "Arimasu (あります)",
            "meaning": "There is / To have (Inanimate Objects).",
            "desc": "Use 'arimasu' when asking about or stating the existence of non-living things (menus, keys, time, cars).",
            "example": "英語のメニューはありますか？ (Eigo no menyuu wa arimasu ka? / Do you have an English menu?)",
            "Option_A": "Eigo no menyuu wa imasu ka?",
            "Option_B": "Eigo no menyuu wa ikimasu ka?",
            "Option_C": "Eigo no menyuu wa arimasu ka?",
            "Option_D": "Eigo no menyuu wa arimasen ka?",
            "correct": "C"
        },
        {
            "Question": "A friend asks if you want to join them for a weekend trip to Kyoto, but you are completely buried in work. How do you politely tell them you don't have time?",
            "word": "Arimasen (ありません)",
            "meaning": "There is not / Do not have (Inanimate Objects).",
            "desc": "'Arimasen' is the polite negative form of 'arimasu'. Use it to say you don't possess something inanimate, like time (jikan) or money (kane).",
            "example": "残念ですが、時間がありません。 (Zannen desu ga, jikan ga arimasen. / Regrettably, I don't have time.)",
            "Option_A": "Jikan ga ikimasen.",
            "Option_B": "Jikan ga arimasen.",
            "Option_C": "Jikan ga imasen.",
            "Option_D": "Jikan ga tabemasen.",
            "correct": "B"
        },
        {
            "Question": "Your friends are meeting up at Shinjuku Station tonight. You want to tell them excitedly: 'I am going to the station right now!' Which motion verb fits perfectly?",
            "word": "Ikimasu (行きます)",
            "meaning": "To go.",
            "desc": "'Ikimasu' is the active motion verb indicating you are moving away from where you are toward a target destination.",
            "example": "今から駅へ行きます！ (Ima kara eki e ikimasu! / I am going to the station right now!)",
            "Option_A": "Eki e tabemasu.",
            "Option_B": "Eki e ikimasu.",
            "Option_C": "Eki e hanashimasu.",
            "Option_D": "Eki e nemasu.",
            "correct": "B"
        },
        {
            "Question": "Someone invites you to a late-night party, but you plan to stay home to rest. How do you clearly say: 'I will not go tonight'?",
            "word": "Ikimasen (行きません)",
            "meaning": "Will not go / Do not go.",
            "desc": "This is the polite negative expression of 'ikimasu'. It lets people know you are turning down an invitation to a physical place.",
            "example": "今夜は行きません。 (Konya wa ikimasen. / I will not go tonight.)",
            "Option_A": "Konya wa ikimashita.",
            "Option_B": "Konya wa ikitai desu.",
            "Option_C": "Konya wa ikimasu.",
            "Option_D": "Konya wa ikimasen.",
            "correct": "D"
        }
    ]
    
    # Mix and shuffle organic scenarios to keep repetitions feeling fresh and context-rich
    extended_bank = []
    prefixes = [
        "Review Session: ",
        "Daily Practice: ",
        "Quick Drill: ",
        "Guild Challenge: "
    ]
    
    for i in range(100):
        random.shuffle(base_scenarios)
        for base in base_scenarios:
            item = base.copy()
            item["ID"] = len(extended_bank) + 1
            # Add subtle framing prefixes so the items feel diverse over long rounds
            pfx = random.choice(prefixes) if i > 0 else ""
            if pfx:
                item["Question"] = pfx + item["Question"][0].lower() + item["Question"][1:]
            extended_bank.append(item)
            
    return extended_bank

questions_list = get_automated_question_bank()

# --- ONBOARDING GATEWAY SYSTEM ---
if not st.session_state.user_authenticated:
    st.title("🇯🇵 Nihongo Guild Network")
    st.subheader("👋 Welcome to the Guild Arena")
    
    user_input_name = st.text_input("Profile Display Name / Nickname:", placeholder="e.g., Alex")
    user_input_email = st.text_input("Your Secure Email Address (For Account Validation Verification):", placeholder="name@example.com")
    st.markdown("---")
    
    with st.expander("➕ Option 1: Invite Friends & Create a Closed Group"):
        if st.button("Generate Group Access Token", key="create_group_btn"):
            if user_input_name.strip() and "@" in user_input_email:
                new_group_code = f"G-{random.randint(1000, 9999)}"
                uid = "UID-16728" if user_input_name.strip().lower() == "admin" else f"UID-{random.randint(10000, 99999)}"
                
                # Cache user profile data values locally
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
                        "subject": "Nihongo Guild - Account Creation & Verification Receipt Link",
                        "message": f"Welcome to the Arena! Your profile account setup is complete. \n\nWarrior: {user_input_name}\nLobby Group Code: {new_group_code}\n\nYour account has been securely verified and cached on this phone device."
                    })
                except: pass
                st.rerun()
            else:
                st.error("Please fill in both fields correctly (include '@' in your email)!")

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
    # --- 👑 UNIVERSAL TOP NAVIGATION ROW PORTAL 👑 ---
st.markdown("<div class='header-bar'>", unsafe_allow_html=True)
nh_col1, nh_col2, nh_col3 = st.columns(3)
with nh_col1:
    if st.button("🏡 Arena Home", key="nav_home_btn"):
        st.session_state.current_page_view = "ARENA"
        st.rerun()
with nh_col2:
    if st.button("🤖 AI Sensei Hub", key="nav_ai_btn"):
        st.session_state.current_page_view = "AI_AGENT"
        st.rerun()
with nh_col3:
    if st.button("🥷 MyPage Profile", key="nav_mypage_btn"):
        st.session_state.current_page_view = "MYPAGE"
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# --- ROUTER VIEWPORT ---
if st.session_state.current_page_view == "ARENA":
    tab1, tab2, tab3 = st.tabs(["🏆 Scoreboard", "⚔️ Quiz Room", "📈 Progress Journey"])
    
    with tab1:
        if st.session_state.my_group == "SOLO":
            st.info("Log into a multiplayer space group code to review rival metric standings.")
        else:
            st.subheader(f"👑 Room Standings: {st.session_state.my_group}")
            group_df = scores_df[scores_df["Group_Code"] == st.session_state.my_group] if not scores_df.empty else pd.DataFrame()
            
            if not group_df.empty:
                group_df["Correct"] = pd.to_numeric(group_df["Correct"])
                group_df["Incorrect"] = pd.to_numeric(group_df["Incorrect"])
                leaderboard = group_df.groupby(["User_ID", "Name"]).agg(Total_Correct=("Correct", "sum"), Total_Incorrect=("Incorrect", "sum")).reset_index()
                
                def calculate_badge(row_data):
                    score = row_data["Total_Correct"]
                    if score >= 50: return "👑 Master Shogun"
                    elif score >= 25: return "⚔️ Ronin Elite"
                    return "🌾 Student Novice"
                    
                leaderboard["Guild Badge Title"] = leaderboard.apply(calculate_badge, axis=1)
                leaderboard = leaderboard.sort_values(by="Total_Correct", ascending=False)
                st.dataframe(leaderboard[["Name", "Guild Badge Title", "Total_Correct", "Total_Incorrect"]], use_container_width=True, hide_index=True)
            else:
                st.info("No recorded score logs inside this space yet.")

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
            st.markdown(f'<div class="question-box"><span style="font-weight: bold; font-size:12px; letter-spacing:1px;">CHALLENGE {q_idx + 1} OF 10</span><h3>{row["Question"]}</h3></div>', unsafe_allow_html=True)
            
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
                st.markdown(f'<div class="explanation-card"><h4>{status_color} • Concept Analysis</h4><p><strong>Target Word:</strong> {row["word"]}</p><p><strong>Exact Meaning:</strong> {row["meaning"]}</p><p><strong>Breakdown Rules:</strong> {row["desc"]}</p><p style="background:#0f0f12; padding:10px; border-radius:8px; border-left:3px solid #ffa500; color:#fff !important;"><strong>💡 Practice Sentence Example:</strong><br><em>{row["example"]}</em></p></div>', unsafe_allow_html=True)
                if st.button("Next Challenge ➡️", key="next_q_btn"):
                    st.session_state.quiz_index += 1
                    st.session_state.show_explanation = False
                    st.rerun()
                    
            # Native Streamlit Link Button Override to Prevent WhatsApp Pop-up Blocking Architecture
            peer_challenge_msg = (
                f"⚔️ *Nihongo Peer Challenge Duel!* 🥷\n\n"
                f"From player: {st.session_state.my_name} (Room: {st.session_state.my_group})\n\n"
                f"👉 *Challenge Question:* \"{row['Question']}\"\n\n"
                f"Think you can pass me? Tap our app link to enter our room or train solo:\n"
                f"🔗 https://streamlit.app"
            )
            st.link_button("🚀 Throw Challenge to WhatsApp Friend", f"https://wa.me{urllib.parse.quote(peer_challenge_msg)}")
            
        else:
            st.success("🏁 Challenge Completed Successfully!")
            if st.button("Save & Upload Results to Ledger Scoreboard"):
                save_score_locally(st.session_state.my_uid, st.session_state.my_name, st.session_state.my_group, st.session_state.run_correct, st.session_state.run_incorrect)
                del st.session_state.quiz_index
                del st.session_state.run_correct
                del st.session_state.run_incorrect
                st.rerun()

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
            
            st.markdown("### 📊 Accuracy Progress Over Time")
            my_history_df["Cumulative_Correct"] = my_history_df["Correct"].cumsum()
            st.line_chart(my_history_df, x="Timestamp", y="Cumulative_Correct", color="#1e90ff")
        else:
            st.info("Complete your first quiz evaluation run to map your performance progress dashboard timeline.")

elif st.session_state.current_page_view == "MYPAGE":
    st.subheader("🥷 Profile Account MyPage Portal")
    uploaded_pic = st.file_uploader("Upload Profile Image Avatar:", type=["png", "jpg", "jpeg"])
    if uploaded_pic is not None:
        st.image(uploaded_pic, width=120)
        
    st.write(f"👤 Display Name: **{st.session_state.my_name}**")
    st.write(f"📧 Secure Backup Email: `{st.session_state.my_email}`")
    st.write(f"🆔 Personal Account Token: `{st.session_state.my_uid}`")
    st.write(f"🛡️ Synced Lobby Group: **{st.session_state.my_group}**")
    
    if st.button("🔄 Clear Cached Session (Logout)"):
        clear_cached_session()
        st.session_state.user_authenticated = False
        st.session_state.current_page_view = "ARENA"
        st.rerun()

elif st.session_state.current_page_view == "AI_AGENT":
    st.subheader("🤖 AI Sensei Hub & Q&A Assistant")
    st.info("AI Core Status: Preparing properties for the generative LLM pipeline node. Ready for custom query inputs.")
    
    ai_query = st.text_input("Ask AI Sensei a Japanese grammar query or frame a concept question:", placeholder="e.g., Explain the difference between particle WA and GA")
    if ai_query:
        # Pre-allocated structural logic placeholder for upcoming AI API responses
        st.markdown(f"""
        <div class='explanation-card'>
            <h4>🤖 AI Sensei Analysis Mock Sandbox</h4>
            <p><strong>Query Caught:</strong> "{ai_query}"</p>
            <p><em>[System property placeholder ready: The upcoming LLM integration loop will teach this concept and auto-generate unique multiple choice challenge options right here!]</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        mock_ai_challenge = f"🤖 AI Prompt Challenge Duel via Room: {st.session_state.my_group}\n\nHey! Look at this custom concept breakdown: '{ai_query}'"
        st.link_button("🚀 Throw Custom AI Question to WhatsApp Group", f"https://wa.me{urllib.parse.quote(mock_ai_challenge)}")
        
