import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="Japanese Quiz Crew", page_icon="🇯🇵", layout="centered")

# Custom CSS for a clean mobile-native look
st.markdown("""
    <style>
    .main .block-container { max-width: 500px; padding-top: 2rem; }
    div.stButton > button:first-child { width: 100%; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("🇯🇵 Japanese Quiz Crew")
st.caption("Track scores with your 5 friends!")

# --- GOOGLE SHEET CONNECTION ---
# This establishes the live link to your spreadsheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Read existing data from the sheet
try:
    df = conn.read(ttl="0m") # ttl="0m" ensures it pulls fresh data instantly
except Exception:
    # If the sheet is completely empty except headers, handle it gracefully
    df = pd.DataFrame(columns=["Timestamp", "Name", "Topic", "Correct", "Incorrect"])

# --- NAVIGATION TABS ---
tab1, tab2 = st.tabs(["📊 Scoreboard & Stats", "📝 Log a Score"])

with tab1:
    st.subheader("🏆 Leaderboard")
    
    if not df.empty and len(df) > 0:
        # Convert numeric columns to avoid formatting errors
        df["Correct"] = pd.to_numeric(df["Correct"])
        df["Incorrect"] = pd.to_numeric(df["Incorrect"])
        
        # Calculate totals per friend
        leaderboard = df.groupby("Name").agg(
            Total_Correct=("Correct", "sum"),
            Total_Incorrect=("Incorrect", "sum")
        ).reset_index()
        
        # Calculate accuracy percentage
        leaderboard["Accuracy %"] = (leaderboard["Total_Correct"] / (leaderboard["Total_Correct"] + leaderboard["Total_Incorrect"]) * 100).round(1)
        leaderboard = leaderboard.sort_values(by="Total_Correct", ascending=False)
        
        # Display scoreboard
        st.dataframe(leaderboard, use_container_width=True, hide_index=True)
        
        # Performance Chart
        st.subheader("📈 Performance Breakdown")
        st.bar_chart(leaderboard, x="Name", y=["Total_Correct", "Total_Incorrect"], color=["#2ecc71", "#e74c3c"])
    else:
        st.info("No scores logged yet! Go to the 'Log a Score' tab to start.")

with tab2:
    st.subheader("Log Your Quiz Results")
    
    with st.form("score_form", clear_on_submit=True):
        friend_name = st.selectbox("Who are you?", ["Alex", "Jordan", "Taylor", "Sam", "Morgan", "Jamie"])
        topic = st.selectbox("Quiz Topic", ["Mondai Nai", "Arimasu / Arimasen", "Ikimasu / Ikimasen"])
        
        col1, col2 = st.columns(2)
        with col1:
            correct = st.number_input("Correct Answers", min_value=0, max_value=25, value=0, step=1)
        with col2:
            incorrect = st.number_input("Incorrect Answers", min_value=0, max_value=25, value=0, step=1)
            
        submitted = st.form_submit_button("Submit Score")
        
        if submitted:
            new_row = pd.DataFrame([{
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Name": friend_name,
                "Topic": topic,
                "Correct": int(correct),
                "Incorrect": int(incorrect)
            }])
            
            # Combine old data with new row
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            # Update the Google Sheet
            conn.update(data=updated_df)
            st.success(f"Score logged successfully for {friend_name}!")
            st.invalidate_pages() # Refresh the page data
