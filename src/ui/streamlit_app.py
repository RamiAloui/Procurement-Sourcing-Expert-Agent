"""Streamlit chat interface for procurement agent."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from src.agent.agent import stream_agent
from langchain_core.messages import HumanMessage, AIMessage


st.set_page_config(
    page_title="Procurement Agent",
    page_icon="💼",
    layout="centered"
)

st.title("Procurement & Sourcing Expert Agent")

st.markdown("""
<style>
.loading-dots {
    display: inline-block;
}
.loading-dots::after {
    content: '...';
    animation: dots 1.5s steps(4, end) infinite;
}
@keyframes dots {
    0%, 20% { content: '.'; }
    40% { content: '..'; }
    60%, 100% { content: '...'; }
}

/* Shimmer animation for tool status */
.tool-status {
    background: linear-gradient(
        90deg,
        #888 0%,
        #fff 50%,
        #888 100%
    );
    background-size: 200% 100%;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 2s ease-in-out infinite;
    display: inline-block;
}

@keyframes shimmer {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize streaming flag
if "is_streaming" not in st.session_state:
    st.session_state.is_streaming = False

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=False)

# User input
if prompt := st.chat_input("Ask about procurement data..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.is_streaming = True
    st.rerun()
    
# Stream agent response if flag is set
if st.session_state.is_streaming:
    # Get the last user message
    prompt = st.session_state.messages[-1]["content"]
    
    try:
        with st.chat_message("assistant"):
            status_placeholder = st.empty()
            response_placeholder = st.empty()
            full_response = ""
            has_started_response = False
            
            # Show initial loading indicator with animation
            status_placeholder.markdown('<span class="loading-dots"></span>', unsafe_allow_html=True)
            
            # Convert session history to LangChain message format
            history = []
            for msg in st.session_state.messages[:-1]:
                if msg["role"] == "user":
                    history.append(HumanMessage(content=msg["content"]))
                else:
                    history.append(AIMessage(content=msg["content"]))
            
            # Stream both status updates and tokens with conversation history
            for chunk_type, content in stream_agent(prompt, history):
                if chunk_type == 'status':
                    # Show agent progress with shimmer animation
                    if not has_started_response:
                        status_placeholder.markdown(
                            f'<span class="tool-status">{content}...</span>',
                            unsafe_allow_html=True
                        )
                
                elif chunk_type == 'token':
                    # Clear status when response starts
                    if not has_started_response:
                        status_placeholder.empty()
                        has_started_response = True
                    
                    # Accumulate and display tokens
                    full_response += content
                    response_placeholder.markdown(full_response, unsafe_allow_html=False)
        
        # Add complete response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.is_streaming = False
        st.rerun()
    
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        st.session_state.is_streaming = False
        st.rerun()
