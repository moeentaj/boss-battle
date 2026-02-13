import streamlit as st
from openai import OpenAI

# 1. Setup API Client (Secrets stored in Streamlit Cloud)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- SESSION STATE ---
if "hp" not in st.session_state:
    st.session_state.hp = 100
if "current_question" not in st.session_state:
    st.session_state.current_question = "Explain the difference between a list and a tuple."
if "battle_log" not in st.session_state:
    st.session_state.battle_log = []

# --- AI FUNCTIONS ---
def generate_new_question():
    """Ask the AI to provide a random challenge based on the course topic."""
    prompt = "You are a Python instructor. Generate one short, challenging technical question for a student."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def evaluate_answer(question, answer):
    """Ask the AI to grade the answer and return damage points."""
    prompt = f"""
    Question: {question}
    Student Answer: {answer}
    
    You are a game engine. Evaluate this answer. 
    Return exactly in this format:
    Score: [0-40]
    Feedback: [Short 1-sentence response]
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

# --- UI ---
st.title("⚔️ AI Boss Battle")

if st.session_state.hp > 0:
    st.progress(st.session_state.hp / 100)
    st.write(f"### Boss Challenge: \n {st.session_state.current_question}")
    
    user_input = st.text_area("Your Answer:", placeholder="Type your explanation or code here...")
    
    if st.button("Attack!"):
        with st.spinner("The Boss is evaluating your move..."):
            result = evaluate_answer(st.session_state.current_question, user_input)
            
            # Parse the AI response (Simple parsing for demo)
            try:
                damage = int(result.split("Score:")[1].split("\n")[0].strip())
                feedback = result.split("Feedback:")[1].strip()
                
                st.session_state.hp -= damage
                st.session_state.battle_log.insert(0, f"💥 {feedback} (-{damage} HP)")
                
                # If boss is still alive, give a new question for the next round
                if st.session_state.hp > 0:
                    st.session_state.current_question = generate_new_question()
                st.rerun()
            except:
                st.error("The Boss is confused by your energy. Try again!")

else:
    st.balloons()
    st.success("The Boss has been defeated! You are a Master.")
    if st.button("Restart Journey"):
        st.session_state.hp = 100
        st.session_state.current_question = generate_new_question()
        st.session_state.battle_log = []
        st.rerun()

# Log Display
for entry in st.session_state.battle_log[:3]:
    st.write(entry)
