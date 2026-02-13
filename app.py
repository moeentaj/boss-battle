import streamlit as st
from groq import Groq

# --- INITIALIZATION ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "hp" not in st.session_state:
    st.session_state.hp = 100
if "current_q" not in st.session_state:
    st.session_state.current_q = "Explain why open source is important for AI."

# --- UI HEADER ---
st.title("🛡️ Open Source Boss Battle")

# --- THE STATUS BAR (Percent & Icons) ---
# We use columns to put the Icon and the HP bar side-by-side
col1, col2 = st.columns([1, 4])

with col1:
    # Large Heart or Boss Icon
    st.markdown("### ❤️ HP") 

with col2:
    # Calculate percentage for display
    hp_percent = max(0, st.session_state.hp)
    # The 'text' parameter in st.progress shows the % right on the bar!
    st.progress(hp_percent / 100, text=f"{hp_percent}% Integrity Remaining")

# --- THE GAMEPLAY ---
st.write(f"### 🤖 The Sentinel asks: \n {st.session_state.current_q}")
user_answer = st.text_input("Enter your command:", placeholder="Type here...")

if st.button("⚔️ ATTACK"):
    if user_answer:
        with st.spinner("Analyzing energy..."):
            # Same AI Logic as before
            eval_prompt = f"Question: {st.session_state.current_q}\nAnswer: {user_answer}\nGrade this. Return: 'Damage: [0-30], Feedback: [text]'"
            
            # (Assuming get_ai_response logic from previous step)
            # ... update st.session_state.hp and st.session_state.current_q ...
            st.rerun()
    else:
        st.warning("You must enter a command to attack!", icon="⚠️")

# --- GAME OVER STATE ---
if st.session_state.hp <= 0:
    st.balloons()
    st.success("✨ VICTORY! The Sentinel has been deactivated.", icon="🏆")
    if st.button("🔄 Restart Simulation"):
        st.session_state.hp = 100
        st.rerun()
