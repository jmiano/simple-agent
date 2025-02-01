import os
import streamlit as st
from dotenv import load_dotenv
from agent import Agent

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Simple Agent",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("Please set OPENAI_API_KEY in your .env file")
        st.stop()
    st.session_state.agent = Agent(openai_api_key=openai_api_key)

# App title
st.title("🤖 Simple Agent")
st.markdown("""
This is a ReAct-based agent that can help you with:
- Searching the internet for information
- Performing mathematical calculations
""")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.run(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    st.markdown("### About")
    st.markdown("""
    This agent uses:
    - OpenAI's GPT-4o
    - ReAct framework for reasoning
    - Google Search for information
    - Calculator for math operations
    """)
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun() 