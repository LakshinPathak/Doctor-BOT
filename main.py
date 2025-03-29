
import streamlit as st
from groq import Groq

# Your Groq API Key (REPLACE WITH YOUR ACTUAL API KEY)
GROQ_API_KEY = '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'

# Initialize Groq Client
@st.cache_resource
def init_groq_client():
    try:
        return Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        return None

# Dynamic System Prompt for Doctor Consultation
SYSTEM_PROMPT = """
You are an AI medical assistant specializing in doctor consultations and appointment management.
Your responsibilities include:
- Assisting patients in booking doctor appointments
- Providing general healthcare advice (but not diagnosing or prescribing)
- Offering guidance on symptoms and when to seek medical attention
- Helping with clinic hours, doctor availability, and consultation types
- Ensuring ethical AI interaction by advising users to consult professionals for critical health concerns

Your tone should be:
- Professional yet empathetic
- Clear and easy to understand
- Supportive and informative
"""

# Chat History Management
def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI medical assistant. How can I help you today?"}
        ]

# Generate LLM Response
def get_ai_response(user_input, chat_history):
    client = init_groq_client()
    if not client:
        return "Sorry, I'm having trouble connecting to the AI service."
    
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend([{ "role": msg["role"], "content": msg["content"] } for msg in chat_history[-5:]])
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            max_tokens=1000,
            temperature=0.4,
            top_p=0.9
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# Main Streamlit App
def main():
    st.set_page_config(page_title="AI Doctor Assistant", page_icon="🩺", layout="wide")
    initialize_chat_history()
    
    st.title("🩺 AI Doctor Consultation Assistant")
    st.markdown("Helping you with doctor appointments and general health guidance")

    # Chat Interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    user_input = st.chat_input("Ask me about doctor appointments or general health queries")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Let me check that for you..."):
                ai_response = get_ai_response(user_input, st.session_state.messages)
                st.markdown(ai_response)
        
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

if __name__ == "__main__":
    main()
