import streamlit as st

# --- CONFIGURATION ---
BOSS_NAME = "The Syntax Sentinel"
MAX_HP = 100

# --- SESSION STATE INITIALIZATION ---
# This ensures the game doesn't restart every time the user clicks a button
if "hp" not in st.session_state:
    st.session_state.hp = MAX_HP
if "log" not in st.session_state:
    st.session_state.log = ["A wild Syntax Sentinel appears!"]

# --- UI LAYOUT ---
st.title("⚔️ Course Boss Battle")

# Sidebar for Stats
st.sidebar.header("Student Stats")
st.sidebar.metric("Your Knowledge", "100%")

# Boss Visuals (Using a simple placeholder or text for now)
st.header(BOSS_NAME)
hp_percent = st.session_state.hp / MAX_HP

# Dynamic Health Bar
bar_color = "green" if hp_percent > 0.5 else "orange" if hp_percent > 0.2 else "red"
st.progress(hp_percent)
st.subheader(f"Boss HP: {st.session_state.hp} / {MAX_HP}")

# --- BATTLE LOGIC ---
if st.session_state.hp > 0:
    # 1. The Question Area
    st.write("### The Sentinel challenges you!")
    st.info("What is the correct way to define a function in Python?")
    
    # 2. Input
    answer = st.text_input("Type your code answer:", key="user_answer")
    
    if st.button("Cast Spell (Submit)"):
        # Simple Logic Check
        if "def" in answer.lower() and ":" in answer:
            damage = 25
            st.session_state.hp -= damage
            st.session_state.log.insert(0, f"✅ CRITICAL HIT! You dealt {damage} damage.")
        else:
            st.session_state.log.insert(0, "❌ BLOCKED! The Sentinel parried your weak syntax.")
        st.rerun()

else:
    st.balloons()
    st.success(f"VICTORY! You have defeated {BOSS_NAME}!")
    if st.button("Reset Battle"):
        st.session_state.hp = MAX_HP
        st.session_state.log = ["The Sentinel has respawned..."]
        st.rerun()

# --- BATTLE LOG ---
st.write("---")
st.write("### Battle History")
for entry in st.session_state.log[:5]: # Show last 5 actions
    st.text(entry)
