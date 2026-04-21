import streamlit as st
import google.generativeai as genai

# Səhifə nizamı
st.set_page_config(page_title="Az AI Pro", page_icon="🤖")
st.title("🤖 Az AI Pro")

# API Key yoxlanışı
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Lütfən Secrets hissəsinə GOOGLE_API_KEY əlavə edin!")
else:
    # Google Gemini konfiqurasiyası
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Sənin API Key-in üçün ən uyğun model ünvanı
    model = genai.GenerativeModel('models/gemini-pro')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mesajları göstər
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
                # Birbaşa cavab generasiyası
                response = model.generate_content(prompt)
                
                if response.text:
                    res_text = response.text
                else:
                    res_text = "Bot cavab verə bilmədi, lütfən yenidən yoxlayın."
                
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"Xəta baş verdi: {e}")
