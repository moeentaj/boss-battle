import streamlit as st
from groq import Groq
import random

# --- 1. CONFIGURATION ---
TOPIC = "AI for Entrepreneurs"
TOTAL_QUESTIONS = 5

if "GROQ_API_KEY" not in st.secrets:
    st.error("Please add GROQ_API_KEY to your Secrets!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. SESSION STATE ---
if "hp" not in st.session_state:
    st.session_state.hp = 100
if "count" not in st.session_state:
    st.session_state.count = 1
if "battle_log" not in st.session_state:
    st.session_state.battle_log = ["🚀 Welcome, Entrepreneur! Defeat the Sentinel to prove your AI readiness."]
if "current_q" not in st.session_state:
    # Initial Question Prompt
    st.session_state.current_q = "How can an entrepreneur use a Large Language Model (LLM) to save 10 hours of work per week?"

# --- 3. AI LOGIC ---
def get_ai_response(prompt):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": f"You are an expert consultant for the course '{TOPIC}'."}, 
                  {"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    return chat_completion.choices[0].message.content

def handle_attack(user_answer):
    # Evaluate Answer
    eval_prompt = f"""
    Topic: {TOPIC}
    Question: {st.session_state.current_q}
    Student Answer: {user_answer}
    
    Task: Grade the answer 0-10 based on business accuracy.
    Return ONLY the number.
    """
    score_str = get_ai_response(eval_prompt)
    score = int(''.join(filter(str.isdigit, score_str))) if any(c.isdigit() for c in score_str) else 0
    
    damage = score * 2
    st.session_state.hp -= damage
    st.session_state.battle_log.insert(0, f"Round {st.session_state.count}: Hit for {damage} damage!")
    
    # Check if we should generate a new question
    if st.session_state.count < TOTAL_QUESTIONS:
        st.session_state.count += 1
        new_q_prompt = f"Generate a unique question for an entrepreneur about {TOPIC}. Keep it practical (e.g., about ROI, tools, or automation)."
        st.session_state.current_q = get_ai_response(new_q_prompt)
    else:
        st.session_state.count = 6 # Mark as finished

# --- 4. UI ---
st.title("💼 AI for Entrepreneurs: Boss Battle")

# HUD
col1, col2 = st.columns([1, 2])
with col1:
    st.metric("Question", f"{min(st.session_state.count, 5)} / {TOTAL_QUESTIONS}")
with col2:
    st.progress(st.session_state.hp / 100, text=f"Sentinel Integrity: {st.session_state.hp}%")

# Main Logic
if st.session_state.count <= TOTAL_QUESTIONS:
    st.write(f"### Q{st.session_state.count}: {st.session_state.current_q}")
    
    with st.form("attack_form"):
        ans = st.text_input("Your Strategic Move:")
        if st.form_submit_button("🚀 ATTACK") and ans:
            handle_attack(ans)
            st.rerun()
else:
    # --- END GAME SCENE ---
    st.balloons()
    st.success("🏁 ASSESSMENT COMPLETE")
    final_score = 100 - st.session_state.hp
    st.subheader(f"Entrepreneurial AI Score: {final_score}%")
    
    if final_score > 70:
        st.write("You are ready to automate your business! 🚀")
    else:
        st.write("Keep studying! The AI revolution waits for no one. 📚")
        
    if st.button("Reset Assessment"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# History Log
st.write("---")
for entry in st.session_state.battle_log[:5]:
    st.text(entry)
