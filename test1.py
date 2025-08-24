import streamlit as st
import ollama
import time

# Page configuration - Mobile responsive
st.set_page_config(
    page_title="SIFRA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile responsiveness
st.markdown("""
<style>
    /* Main background - Black */
    .stApp {
        background-color: #0A0A0A;
        color: #FFFFFF;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-box {
            padding: 15px !important;
            margin: 10px 0 !important;
            border-radius: 15px !important;
        }
        
        .user-bubble, .ai-bubble {
            max-width: 90% !important;
            padding: 12px 15px !important;
            font-size: 14px !important;
        }
        
        .stButton button {
            padding: 10px 15px !important;
            font-size: 14px !important;
        }
        
        .stTextArea textarea {
            height: 100px !important;
            font-size: 16px !important; /* iOS zoom prevention */
        }
        
        h1 {
            font-size: 24px !important;
        }
        
        h2 {
            font-size: 20px !important;
        }
        
        h3 {
            font-size: 18px !important;
        }
        
        .sidebar .sidebar-content {
            width: 280px !important;
        }
    }
    
    /* Sidebar for mobile */
    @media (max-width: 768px) {
        .css-1d391kg {
            width: 280px !important;
            transform: translateX(-281px);
        }
        
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 280px !important;
            max-width: 280px !important;
            transform: translateX(0);
        }
    }
    
    /* Prevent zoom on iOS input focus */
    @media screen and (max-width: 768px) {
        .stTextArea textarea {
            font-size: 16px !important;
        }
    }
    
    /* Touch-friendly buttons for mobile */
    .stButton button {
        min-height: 44px; /* Minimum touch target size */
    }
    
    /* Main content box with blue shadow */
    .main-box {
        background: rgba(10, 10, 10, 0.8);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid #00B4D8;
        box-shadow: 0 0 20px rgba(0, 180, 216, 0.4);
        backdrop-filter: blur(10px);
    }
    
    /* Buttons with animation */
    .stButton button {
        background: linear-gradient(45deg, #0077B6, #00B4D8);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 180, 216, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: all 0.5s ease;
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 180, 216, 0.5);
        background: linear-gradient(45deg, #00B4D8, #0077B6);
    }
    
    /* Text area */
    .stTextArea textarea {
        background: rgba(26, 26, 46, 0.7) !important;
        color: #00B4D8 !important;
        border: 2px solid #0077B6 !important;
        border-radius: 15px !important;
        padding: 15px !important;
        font-weight: 500;
    }
    
    .stTextArea textarea:focus {
        border: 2px solid #00B4D8 !important;
        box-shadow: 0 0 10px rgba(0, 180, 216, 0.5) !important;
    }
    
    /* Chat bubbles */
    .user-bubble {
        background: linear-gradient(135deg, #0077B6, #03045E);
        color: #FFFFFF;
        padding: 15px 20px;
        border-radius: 18px 18px 0 18px;
        margin: 15px 0;
        max-width: 75%;
        margin-left: auto;
        animation: slideInRight 0.5s ease;
        box-shadow: 0 5px 15px rgba(0, 119, 182, 0.4);
        border: 1px solid #00B4D8;
    }
    
    .ai-bubble {
        background: linear-gradient(135deg, #03045E, #0077B6);
        color: #FFFFFF;
        padding: 15px 20px;
        border-radius: 18px 18px 18px 0;
        margin: 15px 0;
        max-width: 75%;
        margin-right: auto;
        animation: slideInLeft 0.5s ease;
        box-shadow: 0 5px 15px rgba(0, 119, 182, 0.4);
        border: 1px solid #00B4D8;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from { 
            transform: translateX(50px); 
            opacity: 0; 
        }
        to { 
            transform: translateX(0); 
            opacity: 1; 
        }
    }
    
    @keyframes slideInLeft {
        from { 
            transform: translateX(-50px); 
            opacity: 0; 
        }
        to { 
            transform: translateX(0); 
            opacity: 1; 
        }
    }
    
    /* Headers with blue gradient text */
    h1, h2, h3 {
        background: linear-gradient(45deg, #00B4D8, #0077B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(0, 180, 216, 0.3);
    }
    
    /* Divider */
    hr {
        background: linear-gradient(90deg, transparent, #00B4D8, transparent);
        height: 2px;
        border: none;
        margin: 25px 0;
    }
    
    /* Stats boxes */
    .stats-box {
        background: rgba(26, 26, 46, 0.7);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #0077B6;
        box-shadow: 0 0 15px rgba(0, 119, 182, 0.3);
    }
    
    /* Mobile menu button */
    .mobile-menu-btn {
        display: none;
    }
    
    @media (max-width: 768px) {
        .mobile-menu-btn {
            display: block;
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 1000;
            background: #0077B6;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 10px rgba(0, 180, 216, 0.4);
        }
    }
</style>
""", unsafe_allow_html=True)

# Set the Model
desireModel = 'llama3.1:8b'

# Mobile menu button (only visible on mobile)
st.markdown("""
<div class="mobile-menu-btn">
    <button onclick="toggleSidebar()">☰</button>
</div>

<script>
function toggleSidebar() {
    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
    const isExpanded = sidebar.getAttribute('aria-expanded') === 'true';
    sidebar.setAttribute('aria-expanded', !isExpanded);
}
</script>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🌌 SIFRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Animated history button
    if st.button("📜 **Chat History**", use_container_width=True, key="history_btn"):
        st.session_state.show_history = not st.session_state.show_history
        st.rerun()
    
    st.markdown("---")
    
    # Stats with custom boxes
    st.markdown("### 📊 Chat Stats")
    st.markdown(f"<div class='stats-box'><b>Messages:</b> {len(st.session_state.get('chat_history', []))}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ **Clear Chat**", use_container_width=True, key="clear_btn"):
        st.session_state.chat_history = []
        st.session_state.show_history = False
        st.success("Chat history cleared! ✨")
        time.sleep(0.5)
        st.rerun()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_history' not in st.session_state:
    st.session_state.show_history = False

def generate_response(questionToAsk):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": questionToAsk})
    
    # Show typing animation
    with st.spinner("🤖 Sifra is Thinking..."):
        time.sleep(0.8)
        response = ollama.chat(model=desireModel, messages=[
            {
                'role': 'user',
                'content': questionToAsk,
            },
        ])
    
    # Add AI response to history
    ai_response = response['message']['content']
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    
    return ai_response

# Main content - Responsive columns
col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    st.markdown("<h1 style='text-align: center;'>🔮 SIFRA </h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00B4D8;'>Sifra Your personal AI Assiatant</p>", unsafe_allow_html=True)

    # Main chat container with blue shadow
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)

    # Show history if enabled
    if st.session_state.show_history and st.session_state.chat_history:
        st.markdown("### 📖 Conversation History")
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(f"<div class='user-bubble'><b>👤 You:</b> {message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ai-bubble'><b>🤖 Sifra:</b> {message['content']}</div>", unsafe_allow_html=True)

    # Show latest messages if not viewing full history
    if not st.session_state.show_history and st.session_state.chat_history:
        st.markdown("### 💬 Recent Conversation")
        # Show last 2 exchanges
        recent_messages = st.session_state.chat_history[-4:] if len(st.session_state.chat_history) > 4 else st.session_state.chat_history
        
        for message in recent_messages:
            if message["role"] == "user":
                st.markdown(f"<div class='user-bubble'><b>👤 You:</b> {message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ai-bubble'><b>🤖 Sifra:</b> {message['content']}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Chat input
    st.markdown("### 💭 Your Message")
    with st.form("chat_form", clear_on_submit=True):
        text = st.text_area(
            "",
            placeholder="Type your message here...",
            height=120,
            key="input_text",
            help="Ask anything you'd like to know"
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            submitted = st.form_submit_button("🚀 Send Message", use_container_width=True)
        with col2:
            if st.form_submit_button("🗑️ Clear", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

    if submitted and text.strip():
        response_text = generate_response(text)
        st.session_state.show_history = False
        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #00B4D8;'>✨Designed by AQSA CHANNA</p>", unsafe_allow_html=True)
