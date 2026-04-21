import streamlit as st
import google.generativeai as genai

# Səhifə nizamı
st.set_page_config(page_title="Az AI Pro", page_icon="🤖")
st.title("🤖 Az AI Pro")

# API Key yoxlanışı (Streamlit Secrets-dən götürülür)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Lütfən Secrets hissəsinə GOOGLE_API_KEY əlavə edin!")
else:
    # Google Gemini konfiqurasiyası
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Ən yeni və stabil model (Flash modeli həm daha sürətlidir, həm də xətasızdır)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Mesaj tarixçəsini yaddaşda saxla
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Köhnə mesajları ekranda göstər
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # İstifadəçidən sual al
    if prompt := st.chat_input("Sualınızı bura yazın..."):
        # İstifadəçinin mesajını əlavə et
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Süni intellektin cavabını hazırla
        with st.chat_message("assistant"):
            try:
                # Cavabın yaradılması
                response = model.generate_content(prompt)
                
                if response.text:
                    full_response = response.text
                else:
                    full_response = "Təəssüf ki, cavab hazırlana bilmədi."
                
                st.markdown(full_response)
                # Cavabı tarixçəyə əlavə et
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Sistem xətası baş verdi: {e}")
