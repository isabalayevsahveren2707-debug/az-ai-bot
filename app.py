import streamlit as st
import google.generativeai as genai

# Səhifə nizamı
st.set_page_config(page_title="Az AI Pro", page_icon="🤖")
st.title("🤖 Az AI Pro")

# API Key yoxlanışı
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Lütfən Secrets hissəsinə GOOGLE_API_KEY əlavə edin!")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Model seçimi - Google bəzən 'models/' prefiksi tələb edir
    # Ən stabil 1.5 Flash modelini yoxlayırıq
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('models/gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mesaj tarixçəsini göstər
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # İstifadəçidən sual al
    if prompt := st.chat_input("Sualınızı bura yazın..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Cavabı almağa çalışırıq
                response = model.generate_content(prompt)
                
                # Cavabı ekrana çıxarırıq
                if response.text:
                    bot_message = response.text
                else:
                    bot_message = "Təəssüf ki, cavab boş qayıtdı."
                
                st.markdown(bot_message)
                st.session_state.messages.append({"role": "assistant", "content": bot_message})
            
            except Exception as e:
                # Əgər yuxarıdakı model işləməsə, avtomatik köhnə modelə keçid edirik
                try:
                    alt_model = genai.GenerativeModel('gemini-pro')
                    alt_response = alt_model.generate_content(prompt)
                    st.markdown(alt_response.text)
                    st.session_state.messages.append({"role": "assistant", "content": alt_response.text})
                except Exception as e2:
                    st.error(f"Xəta davam edir: {e2}")
