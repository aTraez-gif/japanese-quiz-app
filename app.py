import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import random

# --- NATIVE MOBILE APP THEMING ---
st.set_page_config(page_title="Nihongo Arena", page_icon="🥷", layout="centered")

# Advanced CSS injection to completely override the default "Form" look
st.markdown("""
    <style>
    /* Force mobile native app sizing */
    .main .block-container { max-width: 480px; padding-top: 1rem; background-color: #0f0f12; }
    body { background-color: #0f0f12; color: #ffffff; }
    
    /* Global Card styling */
    .chat-card { padding: 14px; border-radius: 16px; background: #1a1a24; border-left: 6px solid #8a2be2; margin-bottom: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .aura-badge { padding: 3px 9px; border-radius: 20px; font-weight: bold; background: linear-gradient(45deg, #ff007f, #7f00ff); color: white; font-size: 11px; float: right;}
    .gacha-card { padding: 25px; border-radius: 24px; background: linear-gradient(145deg, #1e1e2f, #11111a); border: 2px solid #ffd700; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
    
    /* Beautiful Trivia UI components */
    .question-box { background: #1e1e2e; padding: 18px; border-radius: 16px; margin-bottom: 15px; border: 1px solid #2d2d44; text-align: center; }
    
    /* Make all Streamlit buttons look like large native mobile action tiles */
    div.stButton > button { 
        width: 100% !important; 
        background: linear-gradient(135deg, #6c5ce7, #a29bfe) !important; 
        color: white !important; 
        font-weight: 700 !important; 
        padding: 14px !important; 
        border-radius: 14px !important; 
        border: none !important;
        transition: transform 0.1s ease;
    }
    div.stButton > button:active { transform: scale(0.97); }
    </style>
""", unsafe_allow_html=True)

st.title("🥷 Nihongo Guild Arena")

# --- DATA CONNECTIONS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(sheet_name, fallback_cols):
    try: return conn.read(worksheet=sheet_name, ttl="0m")
    except: return pd.DataFrame(columns=fallback_cols)

scores_df = load_data("Sheet1", ["Timestamp", "Name", "Topic", "Correct", "Incorrect", "Aura_Earned"])
questions_df = load_data("Questions", ["ID", "Question", "Option_A", "Option_B", "Option_C", "Option_D", "Correct_Option"])
chat_df = load_data("Chat", ["Timestamp", "User", "Message", "Aura_Bonus"])

if not scores_df.empty:
    scores_df["Correct"] = pd.to_numeric(scores_df["Correct"]).fillna(0)
    scores_df["Incorrect"] = pd.to_numeric(scores_df["Incorrect"]).fillna(0)

# Global Session Identity
current_user = st.sidebar.selectbox("🎯 Active Warrior:", ["Alex", "Jordan", "Taylor", "Sam", "Morgan", "Jamie"])

tab1, tab2, tab3, tab4 = st.tabs(["🏆 Leaderboard", "⚔️ Live Arena", "💬 Comms", "⛩️ Fortune"])

# --- TAB 1: SCREEN RANKINGS ---
with tab1:
    st.subheader("👑 Guild Hierarchy")
    all_users = ["Alex", "Jordan", "Taylor", "Sam", "Morgan", "Jamie"]
    base_stats = []
    
    for u in all_users:
        u_scores = scores_df[scores_df["Name"] == u] if not scores_df.empty else pd.DataFrame()
        u_chats = chat_df[chat_df["User"] == u] if not chat_df.empty else pd.DataFrame()
        
        correct = u_scores["Correct"].sum() if not u_scores.empty else 0
        incorrect = u_scores["Incorrect"].sum() if not u_scores.empty else 0
        quiz_aura = (correct * 50) - (incorrect * 20)
        chat_aura = len(u_chats) * 10
        total_aura = 1000 + quiz_aura + chat_aura
        
        if total_aura > 1200: tier = "👑 Shogun"
        elif total_aura > 1050: tier = "⚔️ Samurai"
        elif total_aura >= 1000: tier = "🌾 Ronin"
        else: tier = "🤡 Gaki"
            
        base_stats.append({"Warrior": u, "Aura Level": total_aura, "Rank": tier})
        
    st.dataframe(pd.DataFrame(base_stats).sort_values(by="Aura Level", ascending=False), use_container_width=True, hide_index=True)

# --- TAB 2: MOBILIZED GAMEPLAY (NO FORM CIRCLES!) ---
with tab2:
    st.subheader("⚔️ Active Challenge Tile")
    
    if questions_df.empty:
        st.info("The arena scrolls are empty! Fill your Questions tab.")
    else:
        # Track which question the user is on inside temporary state memory
        if "q_index" not in st.session_state:
            st.session_state.q_index = 0
            st.session_state.temp_correct = 0
            st.session_state.temp_incorrect = 0

        q_idx = st.session_state.q_index

        if q_idx < len(questions_df):
            row = questions_df.iloc[q_idx]
            
            # Custom styled layout card for the query block
            st.markdown(f"""
            <div class="question-box">
                <span style="color:#8a2be2; font-weight:bold; font-size:14px;">QUESTION {q_idx + 1} OF {len(questions_df)}</span>
                <h3 style="margin-top:5px; color:white;">{row['Question']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Render choices as clean, square mobile tiles (2x2 layout matrix)
            col1, col2 = st.columns(2)
            with col1:
                ans_A = st.button(f"A) {row['Option_A']}", key=f"btn_A_{q_idx}")
                ans_C = st.button(f"C) {row['Option_C']}", key=f"btn_C_{q_idx}")
            with col2:
                ans_B = st.button(f"B) {row['Option_B']}", key=f"btn_B_{q_idx}")
                ans_D = st.button(f"D) {row['Option_D']}", key=f"btn_D_{q_idx}")
                
            # Evaluation engine when any block tile is pressed
            choice_made = None
            if ans_A: choice_made = "A"
            if ans_B: choice_made = "B"
            if ans_C: choice_made = "C"
            if ans_D: choice_made = "D"
            
            if choice_made:
                correct_letter = str(row['Correct_Option']).strip().upper()
                if choice_made == correct_letter:
                    st.session_state.temp_correct += 1
                    st.toast("🎯 Direct Hit! Correct.", icon="✅")
                else:
                    st.session_state.temp_incorrect += 1
                    st.toast(f"💥 Deflected! Correct answer was {correct_letter}.", icon="❌")
                
                # Advance layout matrix instantly to next question
                st.session_state.q_index += 1
                st.rerun()
        else:
            # End of quiz assessment screen
            st.balloons()
            st.markdown("<div class='question-box'><h3>🏆 Arena Match Finished!</h3></div>", unsafe_allow_html=True)
            st.write(f"🟢 **Answers Right:** {st.session_state.temp_correct}")
            st.write(f"🔴 **Answers Missed:** {st.session_state.temp_incorrect}")
            
            if st.button("Save & Submit Results to Ledger"):
                net_aura = (st.session_state.temp_correct * 50) - (st.session_state.temp_incorrect * 20)
                new_score = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Name": current_user,
                    "Topic": "Speed Arena Run",
                    "Correct": int(st.session_state.temp_correct),
                    "Incorrect": int(st.session_state.temp_incorrect),
                    "Aura_Earned": int(net_aura)
                }])
                conn.update(worksheet="Sheet1", data=pd.concat([scores_df, new_score], ignore_index=True))
                
                # Wipe temporary runtime variables clean for next pass
                del st.session_state.q_index
                st.success("Ledger Sync Complete!")
                st.rerun()

# --- TAB 3: LIVE PERSISTENT WIRE FEED ---
with tab3:
    st.subheader("💬 Guild Comms Wire")
    with st.form("chat_box", clear_on_submit=True):
        msg_text = st.text_input("Broadcast to crew:", placeholder="Talk trash or share study insights...")
        if st.form_submit_button("Send"):
            if msg_text.strip():
                new_msg = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                    "User": current_user,
                    "Message": msg_text,
                    "Aura_Bonus": 10
                }])
                conn.update(worksheet="Chat", data=pd.concat([chat_df, new_msg], ignore_index=True))
                st.rerun()

    if not chat_df.empty:
        for _, post in chat_df.iloc[::-1].head(10).iterrows():
            st.markdown(f"""
            <div class="chat-card">
                <span class="aura-badge">+10 Aura</span>
                <strong>🥷 {post['User']}</strong> <span style='font-size:11px; color:#aaa; margin-left:8px;'>{post['Timestamp']}</span>
                <p style='margin-top:6px; margin-bottom:0px;'>{post['Message']}</p>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 4: LUCKY FORTUNE GENERATION ---
with tab4:
    st.subheader("⛩️ The Omikuji Shrine")
    if st.button("🔮 Pull Random Fortune Card"):
        fortunes = [
            {"luck": "✨ Great Luck", "p": 100, "d": "Flawless pronunciation of 'Mondai nai desu'. +100 Aura!"},
            {"luck": "💀 Bad Luck", "p": -50, "d": "Used 'arimasu' for a breathing cat. Structural fail. -50 Aura!"}
        ]
        rolled = random.choice(fortunes)
        st.markdown(f"""
        <div class="gacha-card">
            <h2>{rolled['luck']}</h2>
            <p>"{rolled['d']}"</p>
            <h3 style='color:#6c5ce7;'>Aura: {rolled['p']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        gacha_log = pd.DataFrame([{
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Name": current_user, "Topic": f"Omikuji: {rolled['luck']}", "Correct": 0, "Incorrect": 0, "Aura_Earned": int(rolled['p'])
        }])
        conn.update(worksheet="Sheet1", data=pd.concat([scores_df, gacha_log], ignore_index=True))
