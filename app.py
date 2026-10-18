import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="Nihongo Challenge Hub", page_icon="🇯🇵", layout="centered")

# Native mobile app layout styling
st.markdown("""
    <style>
    .main .block-container { max-width: 480px; padding-top: 1rem; }
    .chat-card { padding: 12px; border-radius: 12px; background-color: #f1f2f6; margin-bottom: 8px; border-left: 5px solid #2ed573; }
    .question-box { background: #f8f9fa; padding: 18px; border-radius: 16px; margin-bottom: 15px; border: 1px solid #ced4da; text-align: center; }
    div.stButton > button { 
        width: 100% !important; 
        background: #2ed573 !important; 
        color: white !important; 
        font-weight: bold !important; 
        padding: 12px !important; 
        border-radius: 10px !important; 
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇯🇵 Nihongo Challenge Hub")

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(sheet_name, fallback_cols):
    try: return conn.read(worksheet=sheet_name, ttl="0m")
    except: return pd.DataFrame(columns=fallback_cols)

scores_df = load_data("Sheet1", ["Timestamp", "User_ID", "Name", "Topic", "Correct", "Incorrect"])
questions_df = load_data("Questions", ["ID", "Question", "Option_A", "Option_B", "Option_C", "Option_D", "Correct_Option"])
chat_df = load_data("Chat", ["Timestamp", "User", "Message"])

# Map users to permanent Tracking IDs
USER_IDS = {
    "Alex": "UID-001",
    "Jordan": "UID-002",
    "Taylor": "UID-003",
    "Sam": "UID-004",
    "Morgan": "UID-005",
    "Jamie": "UID-006"
}

# --- GLOBAL USER SELECTOR ---
current_user = st.sidebar.selectbox("🎯 Select Your Name:", list(USER_IDS.keys()))
current_id = USER_IDS[current_user]
st.sidebar.info(f"Tracking ID: **{current_id}**")

tab1, tab2, tab3 = st.tabs(["🏆 Scoreboard & Logs", "⚔️ Take Quiz", "💬 Group Chat"])

# --- TAB 1: SCOREBOARD & DETAILED ANSWER LOGS ---
with tab1:
    st.subheader("📊 Group Standings")
    
    if not scores_df.empty and len(scores_df) > 0:
        scores_df["Correct"] = pd.to_numeric(scores_df["Correct"]).fillna(0)
        scores_df["Incorrect"] = pd.to_numeric(scores_df["Incorrect"]).fillna(0)
        
        # Aggregate totals per user
        leaderboard = scores_df.groupby(["User_ID", "Name"]).agg(
            Total_Correct=("Correct", "sum"),
            Total_Incorrect=("Incorrect", "sum")
        ).reset_index()
        
        leaderboard = leaderboard.sort_values(by="Total_Correct", ascending=False)
        st.dataframe(leaderboard, use_container_width=True, hide_index=True)
        
        # Transparent Review Feed: Look closely at everyone's answer breakdowns
        st.subheader("👀 All Attempt History")
        st.dataframe(scores_df, use_container_width=True, hide_index=True)
    else:
        st.info("No quiz submissions found yet.")

# --- TAB 2: INTERACTIVE ONE-BY-ONE QUIZ ---
with tab2:
    st.subheader("📝 Live Challenge")
    
    if questions_df.empty:
        st.warning("Please add questions to your Google Sheet 'Questions' tab first!")
    else:
        # Initialize quiz tracker session states
        if "q_index" not in st.session_state:
            st.session_state.q_index = 0
            st.session_state.temp_correct = 0
            st.session_state.temp_incorrect = 0

        q_idx = st.session_state.q_index

        if q_idx < len(questions_df):
            row = questions_df.iloc[q_idx]
            
            st.markdown(f"""
            <div class="question-box">
                <span style="color: #2ed573; font-weight: bold;">QUESTION {q_idx + 1} OF {len(questions_df)}</span>
                <h3>{row['Question']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # 2x2 Layout matrix for instant button tapping
            col1, col2 = st.columns(2)
            with col1:
                ans_A = st.button(f"A) {row['Option_A']}", key=f"btn_A_{q_idx}")
                ans_C = st.button(f"C) {row['Option_C']}", key=f"btn_C_{q_idx}")
            with col2:
                ans_B = st.button(f"B) {row['Option_B']}", key=f"btn_B_{q_idx}")
                ans_D = st.button(f"D) {row['Option_D']}", key=f"btn_D_{q_idx}")
                
            choice_made = None
            if ans_A: choice_made = "A"
            if ans_B: choice_made = "B"
            if ans_C: choice_made = "C"
            if ans_D: choice_made = "D"
            
            if choice_made:
                correct_letter = str(row['Correct_Option']).strip().upper()
                if choice_made == correct_letter:
                    st.session_state.temp_correct += 1
                    st.toast("Correct!", icon="✅")
                else:
                    st.session_state.temp_incorrect += 1
                    st.toast(f"Wrong! Answer was {correct_letter}", icon="❌")
                
                st.session_state.q_index += 1
                st.rerun()
        else:
            st.success("🏁 Challenge completed!")
            st.write(f"✅ Correct Answers: **{st.session_state.temp_correct}**")
            st.write(f"❌ Incorrect Answers: **{st.session_state.temp_incorrect}**")
            
            if st.button("Submit My Score to Group"):
                new_score = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "User_ID": current_id,
                    "Name": current_user,
                    "Topic": "Japanese Basics Quiz",
                    "Correct": int(st.session_state.temp_correct),
                    "Incorrect": int(st.session_state.temp_incorrect)
                }])
                
                conn.update(worksheet="Sheet1", data=pd.concat([scores_df, new_score], ignore_index=True))
                
                # Reset local quiz metrics
                del st.session_state.q_index
                st.success("Results broadcasted to the scoreboard log!")
                st.rerun()

# --- TAB 3: CLEAN GROUP CHAT ---
with tab3:
    st.subheader("💬 Group Chat")
    
    with st.form("chat_box", clear_on_submit=True):
        msg_text = st.text_input("Message the group:", placeholder="Type a chat...")
        if st.form_submit_button("Send"):
            if msg_text.strip():
                new_msg = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                    "User": f"{current_user} ({current_id})",
                    "Message": msg_text
                }])
                conn.update(worksheet="Chat", data=pd.concat([chat_df, new_msg], ignore_index=True))
                st.rerun()

    if not chat_df.empty:
        for _, post in chat_df.iloc[::-1].head(15).iterrows():
            st.markdown(f"""
            <div class="chat-card">
                <strong>{post['User']}</strong> <span style='font-size:11px; color:#777; float:right;'>{post['Timestamp']}</span>
                <p style='margin-top:4px; margin-bottom:0px;'>{post['Message']}</p>
            </div>
            """, unsafe_allow_html=True)
