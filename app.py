# app.py
import streamlit as st
from llm_wrappers import get_response_openai

# Set a max API usage per session
MAX_USES = 5

# Initialize call counter
if "api_uses" not in st.session_state:
    st.session_state.api_uses = 0

# Check limit
if st.session_state.api_uses >= MAX_USES:
    st.warning("⚠️ You’ve reached your usage limit for this session.")
    st.stop()

st.set_page_config(page_title="BestAI", layout="wide")
st.title("🤖 BestAI — Which AI Answers Better?")

# Prompt input
prompt = st.text_area("Enter your question or prompt:", height=150)

# Show remaining uses
remaining = MAX_USES - st.session_state.api_uses
if remaining > 0:
    st.info(f"🧠 You have {remaining} uses remaining in this session.")
else:
    st.warning("⚠️ You’ve reached your usage limit for this session.")
    st.stop()

# Model selection (we'll start with GPT-3.5 vs GPT-4)
model_options = ["gpt-4o-mini", "gpt-4.1-nano"]
model1 = st.selectbox("Model A", model_options, index=0)
model2 = st.selectbox("Model B", model_options, index=1)

if st.button("Run Duel"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            response1 = get_response_openai(prompt, model1)
            response2 = get_response_openai(prompt, model2)

            # Count this usage
            st.session_state.api_uses += 1
            st.info(f"🧠 You have {MAX_USES - st.session_state.api_uses} uses remaining in this session.")

        # Display responses side-by-side
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"{model1} says:")
            st.markdown(response1)
        with col2:
            st.subheader(f"{model2} says:")
            st.markdown(response2)

        # Voting
        winner = st.radio("Which answer is better?", [model1, model2], horizontal=True)
        if st.button("Vote"):
            st.success(f"Thanks! You voted for **{winner}** 🎉")
            # Optional: store vote to file/db later