import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="Japanese Quiz Crew", page_icon="🇯🇵", layout="centered")

st.markdown("""
    <style>
    .main .block-container { max-width: 500px; padding-top: 1.5rem; }
    div.stButton > button:first-child { width: 100%; border-radius: 8px; }
    .chat-card { padding: 10px; border-radius: 8px; background-color: #f0f2f6; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("🇯🇵 Japanese Quiz Crew")

# --- GOOGLE SHEET CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch data from different tabs safely
try:
    scores_df = conn.read(worksheet="Sheet1", ttl="0m") # Main tracking tab
except:
    scores_df = pd.DataFrame(columns=["Timestamp", "Name", "Topic", "Correct", "Incorrect"])

try:
    questions_df = conn.read(worksheet="Questions", ttl="5m") # Question bank
except:
    questions_df = pd.DataFrame(columns=["ID", "Question", "Option_A", "Option_B", "Option_C", "Option_D", "Correct_Option"])

# --- NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs(["🏆 Leaderboard", "📝 Take Interactive Quiz", "💬 Group Chat & Experience"])

# --- TAB 1: LEADERBOARD ---
with tab1:
    st.subheader("Leaderboard & Stats")
    if not scores_df.empty and len(scores_df) > 0:
        scores_df["Correct"] = pd.to_numeric(scores_df["Correct"])
        scores_df["Incorrect"] = pd.to_numeric(scores_df["Incorrect"])
        
        leaderboard = scores_df.groupby("Name").agg(
            Total_Correct=("Correct", "sum"),
            Total_Incorrect=("Incorrect", "sum")
        ).reset_index()
        
        leaderboard["Accuracy %"] = (leaderboard["Total_Correct"] / (leaderboard["Total_Correct"] + leaderboard["Total_Incorrect"]) * 100).round(1)
        leaderboard = leaderboard.sort_values(by="Total_Correct", ascending=False)
        
        st.dataframe(leaderboard, use_container_width=True, hide_index=True)
        st.bar_chart(leaderboard, x="Name", y=["Total_Correct", "Total_Incorrect"], color=["#2ecc71", "#e74c3c"])
    else:
        st.info("No quiz scores captured yet!")

# --- TAB 2: AUTOMATED QUIZ ---
with tab2:
    st.subheader("Daily Interactive Quiz")
    
    if questions_df.empty or len(questions_df) == 0:
        st.warning("Add some questions to your 'Questions' sheet tab first!")
    else:
        friend_name = st.selectbox("Who is taking the quiz?", ["Alex", "Jordan", "Taylor", "Sam", "Morgan", "Jamie"], key="quiz_user")
        
        # Simple setup: Run through the questions
        with st.form("interactive_quiz"):
            user_answers = {}
            for idx, row in questions_df.iterrows():
                st.write(f"**Q{row['ID']}: {row['Question']}**")
                options = [f"A) {row['Option_A']}", f"B) {row['Option_B']}", f"C) {row['Option_C']}", f"D) {row['Option_D']}"]
                choice = st.radio("Select your answer:", options, key=f"q_{row['ID']}", label_visibility="collapsed")
                user_answers[row['ID']] = choice[0] # Grab just the letter ('A', 'B', etc.)
                st.write("---")
                
            submit_quiz = st.form_submit_button("Submit & Grade Answers")
            
            if submit_quiz:
                correct_count = 0
                incorrect_count = 0
                
                for idx, row in questions_df.iterrows():
                    if user_answers[row['ID']] == str(row['Correct_Option']).strip():
                        correct_count += 1
                    else:
                        incorrect_count += 1
                
                # Write the calculated score back to Sheet1
                new_score = pd.DataFrame([{
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Name": friend_name,
                    "Topic": "Automated Mixed Quiz",
                    "Correct": int(correct_count),
                    "Incorrect": int(incorrect_count)
                }])
                
                # Save data back to the primary Sheet1 tab
                try:
                    updated_scores = pd.concat([scores_df, new_score], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_scores)
                    st.success(f"🎉 Graded! You got {correct_count} Right and {incorrect_count} Wrong. Scoreboard updated!")
                except Exception as e:
                    st.error("Could not save score. Ensure your Google Sheet sharing is set to Editor.")

# --- TAB 3: SOCIAL COMMUNITY FEED ---
with tab3:
    st.subheader("💬 Crew Chat & Language Tips")
    
    # Quick text submission form
    with st.form("chat_form", clear_on_submit=True):
        chat_user = st.selectbox("Posting as:", ["Alex", "Jordan", "Taylor", "Sam", "Morgan", "Jamie"], key="chat_user_select")
        message = st.text_area("Share an experience, a mnemonic hook, or a hard Japanese phrase:", placeholder="Example: Today I learned that 'Mondai' literally breaks down into Gate + Mouth!")
        submit_chat = st.form_submit_button("Post to Crew")
        
        if submit_chat and message.strip() != "":
            # For simplicity, we can log chat logs dynamically right into the app's internal cache 
            # Or you can add a 'Chat' sheet tab to your spreadsheet to track it.
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            
            st.session_state.chat_history.insert(0, {
                "time": datetime.datetime.now().strftime("%H:%M"),
                "user": chat_user,
                "msg": message
            })
            st.toast("Posted to feed!")

    # Display the feed
    st.write("### Recent Updates")
    if "chat_history" in st.session_state and st.session_state.chat_history:
        for post in st.session_state.chat_history:
            st.markdown(f"""
            <div class="chat-card">
                <strong>💡 {post['user']}</strong> <span style='font-size:11px; color:gray;'>at {post['time']}</span><br>
                <p style='margin-top:5px; margin-bottom:0px;'>{post['msg']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No updates posted yet. Be the first to share your learning experience today!")
