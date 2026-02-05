
import streamlit as st
import sys
import os

# Add root directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.main_pipeline import HelixRAGPipeline

# Page Config
st.set_page_config(
    page_title="Helix HR Intelligence",
    page_icon="🧬",
    layout="wide"
)

# Premium Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 15px; border: 1px solid #e9ecef; margin-bottom: 10px; }
    .confidence-tag { font-size: 0.8rem; padding: 2px 8px; border-radius: 10px; font-weight: bold; }
    .high-conf { background-color: #d4edda; color: #155724; }
    .low-conf { background-color: #fff3cd; color: #856404; }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_pipeline():
    return HelixRAGPipeline()

# Initializing Session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/dusk/64/000000/dna-helix.png", width=64)
    st.title("Helix Hub")
    st.markdown("---")
    
    # Dynamic Provider Info
    from config.settings import LLM_PROVIDER
    provider_name = os.getenv("LLM_PROVIDER", LLM_PROVIDER).upper()
    st.info(f"Status: {provider_name} Connected")
    st.info("Data Sources: Employee Master, Leaves, Attendance, Policy PDF")
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Main Header
st.title("Helix HR Intelligence Bot 🧬")
st.caption("Enterprise RAG System | v1.2 | Grounded in Corporate Data")

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "confidence" in msg:
            conf_class = "high-conf" if msg["confidence"] > 0.8 else "low-conf"
            st.markdown(f'<span class="confidence-tag {conf_class}">Trust Score: {int(msg["confidence"]*100)}%</span>', unsafe_allow_html=True)
        if msg.get("warnings"):
            for w in msg["warnings"]:
                st.warning(f"⚠️ {w}")

# Input Logic
if prompt := st.chat_input("Ask about Policy, Attendance, or Employee Records..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Assistant Message
    with st.chat_message("assistant"):
        pipeline = get_pipeline()
        
        with st.spinner("Analyzing Helix Knowledge Base..."):
            result = pipeline.process_query(prompt)
        
        # Display Response
        st.markdown(result["response"])
        
        # Display Logic Indicators
        conf_class = "high-conf" if result["confidence"] > 0.8 else "low-conf"
        st.markdown(f'<span class="confidence-tag {conf_class}">Trust Score: {int(result["confidence"]*100)}%</span>', unsafe_allow_html=True)
        
        if result["warnings"]:
            for w in result["warnings"]:
                st.warning(f"⚠️ {w}")
        
        # Save to session
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result["response"],
            "confidence": result["confidence"],
            "warnings": result["warnings"]
        })
