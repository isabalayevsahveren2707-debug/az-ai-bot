import streamlit as st
import google.generativeai as genai

# Səhifə nizamı
st.set_page_config(page_title="Az AI Pro", page_icon="🤖")
st.title("🤖 Az AI Pro")

# API Key yoxlanışı (Bunu Streamlit Secrets-dən götürəcək)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Lütfən Secrets hissəsinə GOOGLE_API_KEY əlavə edin!")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # 0.4.1 versiyası üçün ən stabil model
    model = genai.GenerativeModel('gemini-pro')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mesaj tarixçəsini göstər
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # İstifadəçidən sual al
    if prompt := st.chat_input("Sualınızı yazın..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Xəta: {e}")
