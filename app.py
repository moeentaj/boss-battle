import streamlit as st
from groq import Groq
import random

# --- 1. INITIALIZATION ---
# Get your FREE API key from https://console.groq.com/
if "GROQ_API_KEY" not in st.secrets:
    st.error("Please add GROQ_API_KEY to your Streamlit Secrets!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize Game State
if "hp" not in st.session_state:
    st.session_state.hp = 100
if "current_q" not in st.session_state:
    st.session_state.current_q = "What is the difference between a list and a tuple in Python?"
if "battle_log" not in st.session_state:
    st.session_state.battle_log = ["⚔️ A new challenger appears!"]

# --- 2. GAME LOGIC FUNCTIONS ---
def get_ai_response(prompt):
    """Fetch response from Open Source Llama 3 model."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def process_attack(user_answer):
    """Evaluate answer and calculate damage with Crit/Miss logic."""
    eval_prompt = f"""
    Question: {st.session_state.current_q}
    Student Answer: {user_answer}
    
    You are a game engine. Rate the answer quality from 0 to 10.
    Return ONLY the number.
    """
    quality_score = get_ai_response(eval_prompt)
    
    # Try to parse the score, default to 0 if AI rambles
    try:
        score = int(''.join(filter(str.isdigit, quality_score)))
    except:
        score = 0

    # Base Damage calculation
    base_damage = score * 3 
    
    # RNG Logic: Crit & Miss
    roll = random.random() # 0.0 to 1.0
    
    if score == 0:
        outcome = "❌ MISS! Your answer was incorrect."
        final_damage = 0
    elif roll < 0.15: # 15% Crit Chance
        outcome = "✨ CRITICAL HIT! Double damage dealt!"
        final_damage = base_damage * 2
    elif roll > 0.95: # 5% Random Miss Chance
        outcome = "🛡️ DEFLECTED! The boss parried your move."
        final_damage = 0
    else:
        outcome = "✅ HIT! Good explanation."
        final_damage = base_damage

    # Update State
    st.session_state.hp = max(0, st.session_state.hp - final_damage)
    st.session_state.battle_log.insert(0, f"{outcome} (-{final_damage} HP)")
    
    # Get new question if boss is alive
    if st.session_state.hp > 0:
        st.session_state.current_q = get_ai_response("Generate a short, unique Python interview question.")

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="AI Boss Battle", page_icon="🛡️")

# HUD (Heads-up Display)
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("### ❤️ HP")
with col2:
    hp_color = "green" if st.session_state.hp > 50 else "orange" if st.session_state.hp > 20 else "red"
    st.progress(st.session_state.hp / 100, text=f"{st.session_state.hp}% Remaining")

# Main Battle Scene
if st.session_state.hp > 0:
    st.info(f"**The Sentinel's Challenge:**\n\n{st.session_state.current_q}")
    
    with st.form("attack_form", clear_on_submit=True):
        user_input = st.text_input("Your Answer:", placeholder="Type your knowledge here...")
        submit = st.form_submit_button("🚀 LAUNCH ATTACK")
        
        if submit and user_input:
            with st.spinner("Calculating trajectory..."):
                process_attack(user_input)
                st.rerun()
else:
    st.balloons()
    st.success("🏆 VICTORY! You have mastered the module.")
    if st.button("🔄 Restart Battle"):
        st.session_state.hp = 100
        st.session_state.battle_log = ["⚔️ The Sentinel returns..."]
        st.rerun()

# 4. PERSISTENT BATTLE LOG (Now visible below)
st.write("---")
st.subheader("📜 Battle History")
for entry in st.session_state.battle_log[:5]:
    if "❌" in entry or "🛡️" in entry:
        st.error(entry)
    elif "✨" in entry:
        st.warning(entry) # Golden/Yellow for crits
    else:
        st.success(entry)
