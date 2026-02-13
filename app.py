import streamlit as st
from groq import Groq

# 1. Setup Groq Client (Open Source Infrastructure)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "hp" not in st.session_state:
    st.session_state.hp = 100
if "current_q" not in st.session_state:
    st.session_state.current_q = "Explain why open source is important for AI."

# --- GAME ENGINE FUNCTIONS ---
def get_ai_response(prompt):
    # We use Llama 3 8B - a powerful, fast, open-source model
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant", # Extremely fast open-source model
    )
    return chat_completion.choices[0].message.content

# --- UI ---
st.title("🛡️ Open Source Boss Battle")

if st.session_state.hp > 0:
    st.write(f"### Current Challenge: \n {st.session_state.current_q}")
    user_answer = st.text_input("Your Response:")

    if st.button("Attack!"):
        # Evaluation Prompt
        eval_prompt = f"""
        Question: {st.session_state.current_q}
        Answer: {user_answer}
        Grade this answer. Return exactly: 'Damage: [number 0-30], Feedback: [text]'
        """
        result = get_ai_response(eval_prompt)
        
        # Simple extraction
        try:
            damage = int(result.split("Damage:")[1].split(",")[0].strip())
            st.session_state.hp -= damage
            st.write(f"Boss took {damage} damage!")
            
            # Generate next question
            st.session_state.current_q = get_ai_response("Generate a new short coding question.")
            st.rerun()
        except:
            st.warning("The boss deflected your move. Try again!")

else:
    st.success("You won with Open Source power!")
