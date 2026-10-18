import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import random

# --- PAGE SETUP ---
st.set_page_config(page_title="Nihongo Guild 🇯🇵", page_icon="🥷", layout="centered")

# Custom UI styling for a gamified mobile aesthetic
st.markdown("""
    <style>
    .main .block-container { max-width: 500px; padding-top: 1rem; }
    div.stButton > button:first-child { width: 100%; border-radius: 12px; font-weight: bold; }
    .chat-card { padding: 12px; border-radius: 12px; background-color: #1e1e24; border-left: 5px solid #6c5ce7; margin-bottom: 10px; color: #ffffff;}
    .aura-badge { padding: 4px 8px; border-radius: 20px; font-weight: bold; background: linear-gradient(45deg, #ff007f, #7f00ff); color: white; font-size: 12px; }
    .gacha-card { padding: 15px; border-radius: 12px; background: linear-gradient(135deg, #111, #222); border: 2px solid #ffd700; text-align: center; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("🥷 Nihongo Guild Arena")
st.caption("The Private Japanese Challenge Hub for You & Your 5 Friends")

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Helper function to grab spreadsheet data safely
def load_data(sheet_name, fallback_cols):
    try:
        return conn.read(worksheet=sheet_name, ttl="0m")
    except:
        return pd.DataFrame(columns=fallback_cols)

scores_df = load_data("Sheet1", ["Timestamp", "Name", "Topic", "Correct", "Incorrect", "Aura_Earned"])
questions_df = load_data("Questions", ["ID", "Question", "Option_A", "Option_B", "Option_C", "Option_D", "Correct_Option"])
chat_df = load_data("Chat", ["Timestamp", "User", "Message", "Aura_Bonus"])

# Ensure data types are uniform
if not scores_df.empty:
    scores_df["Correct"] = pd.to_numeric(scores_df["Correct"]).fillna(0)
    scores_df["Incorrect"] = pd.to_numeric(scores_df["Incorrect"]).fillna(0)
    scores_df["Aura_Earned"] = pd.to_numeric(scores_df["Aura_Earned"]).fillna(0)

# --- GLOBAL APP STATE USER SELECTOR ---
current_user = st.sidebar.selectbox("🎯 Identify Yourself, Warrior:", ["Alex", "Jordan", "Taylor", "Sam", "Morgan", "Jamie"])

# --- NAVIGATION TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Arena Rankings", "📝 Speed Quiz", "💬 Chat & Feed", "⛩️ Daily Gacha Fortunes"])

# --- TAB 1: ARENA RANKINGS (COMPETITIVE LEADERBOARD & AURA STATS) ---
with tab1:
    st.subheader("👑 Current Guild Hierarchy")
    
    # Calculate Leaderboard Metrics with Dynamic Aura Points
    all_users = ["Alex", "Jordan", "Taylor", "Sam", "Morgan", "Jamie"]
    base_stats = []
    
    for u in all_users:
        u_scores = scores_df[scores_df["Name"] == u] if not scores_df.empty else pd.DataFrame()
        u_chats = chat_df[chat_df["User"] == u] if not chat_df.empty else pd.DataFrame()
        
        correct = u_scores["Correct"].sum() if not u_scores.empty else 0
        incorrect = u_scores["Incorrect"].sum() if not u_scores.empty else 0
        
        # Calculate Aura Logic dynamically
        quiz_aura = (correct * 50) - (incorrect * 20)
        chat_aura = len(u_chats) * 10
        total_aura = 1000 + quiz_aura + chat_aura # Start out at baseline 1000 Aura
        
        # Tier Title generation based on standing Aura points
        if total_aura > 1200: tier = "👑 Shogun (Godly Aura)"
        elif total_aura > 1050: tier = "⚔️ Samurai (High Aura)"
        elif total_aura >= 1000: tier = "🌾 Ronin (Neutral Aura)"
        else: tier = "🤡 Gaki (Negative Aura Loss)"
            
        base_stats.append({"Warrior": u, "Aura Level": total_aura, "Status Tier": tier, "Correct": correct, "Fails": incorrect})
        
    leaderboard_df = pd.DataFrame(base_stats).sort_values(by="Aura Level", ascending=False)
    st.dataframe(leaderboard_df, use_container_width=True, hide_index=True)
    
    st.markdown("### 📊 Guild Power Grid")
    st.bar_chart(leaderboard_df, x="Warrior", y="Aura Level", color="#7f00ff")


# --- TAB 2: SPEED QUIZ (AUTOMATED GRADING & AURA SHIFTS) ---
with tab2:
    st.subheader("⚔️ Instant Battle Assessment")
    
    if questions_df.empty:
        st.info("The question scroll is empty. Fill the 'Questions' sheet tab to fight!")
    else:
        with st.form("quiz_battle"):
            answers = {}
            for _, row in questions_df.iterrows():
                st.write(f"**Q{row['ID']}: {row['Question']}**")
                opts = [f"A) {row['Option_A']}", f"B) {row['Option_B']}", f"C) {row['Option_C']}", f"D) {row['Option_D']}"]
                answers[row['ID']] = st.radio("Choose:", opts, key=f"quest_{row['ID']}", label_visibility="collapsed")
                st.write("---")
                
            if st.form_submit_button("Lock In Answers"):
                r_count, w_count = 0, 0
                for _, row in questions_df.iterrows():
                    user_letter = answers[row['ID']][0] # Captures just 'A', 'B', 'C', or 'D'
                    if user_letter == str(row['Correct_Option']).strip().upper():
                        r_count += 1
                    else:
                        w_count += 1
                        
                net_aura = (r_count * 50) - (w_count * 20)
                
                new_score = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Name": current_user,
                    "Topic": "Guild Automated Battle",
                    "Correct": int(r_count),
                    "Incorrect": int(w_count),
                    "Aura_Earned": int(net_aura)
                }])
                
                conn.update(worksheet="Sheet1", data=pd.concat([scores_df, new_score], ignore_index=True))
                
                if net_aura >= 0:
                    st.balloons()
                    st.success(f"✨ Massive W! Got {r_count} right. Earned +{net_aura} Aura Points!")
                else:
                    st.error(f"💀 Outplayed. Defeated on {w_count} questions. Lost {net_aura} Aura!")
                st.rerun()


# --- TAB 3: CLOSED GROUP INTERACTIVE CHAT (PERSISTENT MEMORY) ---
with tab3:
    st.subheader("💬 Guild Command Comms")
    
    # Send message section
    with st.form("chat_box", clear_on_submit=True):
        msg_text = st.text_input(f"Broadcast a system update as [{current_user}]:", placeholder="Type language advice or trash talk here...")
        if st.form_submit_button("Transmit"):
            if msg_text.strip():
                new_msg = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                    "User": current_user,
                    "Message": msg_text,
                    "Aura_Bonus": 10
                }])
                conn.update(worksheet="Chat", data=pd.concat([chat_df, new_msg], ignore_index=True))
                st.toast("Message synced to sheet data!")
                st.rerun()

    # Dynamic scroll feed
    st.write("### 📜 Recent Transmission Scrolls")
    if not chat_df.empty:
        reversed_chat = chat_df.iloc[::-1] # Pull newest texts to top
        for _, post in reversed_chat.head(15).iterrows():
            st.markdown(f"""
            <div class="chat-card">
                <strong>🥷 {post['User']}</strong> 
                <span class="aura-badge">+10 Aura</span>
                <span style='font-size:11px; color:#a4b0be; float:right;'>{post['Timestamp']}</span>
                <p style='margin-top:8px; margin-bottom:0px; font-size:15px;'>{post['Message']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Transmission wire dead. Write the first broadcast message!")


# --- TAB 4: FUN GACHA MECHANICS (DAILY LUCK FORTUNES) ---
with tab4:
    st.subheader("⛩️ The Omikuji Shrine")
    st.write("Draw a single random fortune card once a day to fluctuate your aura status!")
    
    if st.button("🔮 Pull Fortune Scroll"):
        fortunes = [
            {"luck": "✨ Great Luck (Dai-Kichi)", "points": 100, "desc": "You pronounced 'Mondai nai desu' flawlessly in front of natives. +100 Aura!"},
            {"luck": "✨ Small Luck (Sho-Kichi)", "points": 30, "desc": "You successfully recalled what 'arimasen' is used for. +30 Aura!"},
            {"luck": "💨 Future Blessing (Sue-Kichi)", "points": 10, "desc": "You read an entire hiragana block without stuttering. +10 Aura."},
            {"luck": "💀 Bad Luck (Kyo)", "points": -50, "desc": "You used 'arimasu' to talk about your cat instead of your keys. Major structural error. -50 Aura!"},
            {"luck": "🤮 Absolute Curse (Dai-Kyo)", "points": -120, "desc": "You completely forgot what 'ikimasu' means mid-sentence. Total mental collapse. -120 Aura!"}
        ]
        
        rolled = random.choice(fortunes)
        
        st.markdown(f"""
        <div class="gacha-card">
            <h2>{rolled['luck']}</h2>
            <p style='font-size: 16px; font-style: italic;'>"{rolled['desc']}"</p>
            <h3 style='color: #ff4757;'>Aura Impact: {rolled['points']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Log this fortune event as a score modifier row
        gacha_log = pd.DataFrame([{
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Name": current_user,
            "Topic": f"Omikuji: {rolled['luck']}",
            "Correct": 0,
            "Incorrect": 0,
            "Aura_Earned": int(rolled['points'])
        }])
        conn.update(worksheet="Sheet1", data=pd.concat([scores_df, gacha_log], ignore_index=True))
        st.toast("Fortune synced to ledger rankings!")
