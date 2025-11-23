import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Mechanik", page_icon="🚗")

# Pobranie klucza
api_key = st.secrets.get("GOOGLE_API_KEY")

st.title("🚗 Wirtualny Mechanik")

if not api_key:
    st.error("Brak klucza API w Secrets!")
    st.stop()

# Konfiguracja
genai.configure(api_key=api_key)

# Interfejs
car_model = st.text_input("Model auta:")
symptoms = st.text_area("Objawy:", height=150)
btn = st.button("Diagnozuj")

if btn and symptoms:
    with st.spinner('Analizuję...'):
        try:
            # Używamy modelu FLASH - jest szybszy i nowszy
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content(f"Pojazd: {car_model}. Objawy: {symptoms}. Zdiagnozuj usterkę po polsku.")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Błąd: {e}")
            # To pomoże nam zrozumieć problem, jeśli nadal wystąpi:
            st.write("Próbuję sprawdzić dostępne modele...")
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        st.caption(f"Dostępny model: {m.name}")
            except:
                pass
