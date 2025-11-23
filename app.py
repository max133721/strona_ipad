import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Mechanik", page_icon="🚗")

# 1. Pobieramy klucz
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("Brak klucza API w Secrets! Wpisz go w ustawieniach.")
    st.stop()

genai.configure(api_key=api_key)

st.title("🚗 Wirtualny Mechanik")

# 2. Automatyczne wykrywanie modelu (To naprawi Twój błąd)
@st.cache_resource
def get_working_model():
    try:
        # Pobieramy listę wszystkich modeli dostępnych dla Twojego klucza
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Szukamy najlepszego (priorytet: Flash -> Pro -> Cokolwiek innego)
        # API zwraca nazwy jako 'models/gemini-1.5-flash', więc szukamy fragmentu tekstu
        best_model = next((m for m in models if 'flash' in m and '1.5' in m), None)
        if not best_model:
            best_model = next((m for m in models if 'pro' in m and '1.5' in m), None)
        if not best_model:
            best_model = next((m for m in models if 'pro' in m), None)
        if not best_model and models:
            best_model = models[0] # Bierzemy pierwszy lepszy jak nic nie pasuje
            
        return best_model
    except Exception as e:
        return None

# Uruchamiamy wykrywanie
model_name = get_working_model()

if model_name:
    st.caption(f"✅ Połączono z modelem: {model_name}") # Pokaże nam, co zadziałało
    
    car_model = st.text_input("Marka i model pojazdu:")
    symptoms = st.text_area("Objawy:", height=150)
    
    if st.button("Diagnozuj"):
        if not symptoms:
            st.warning("Wpisz objawy!")
        else:
            with st.spinner(f'Analizuję używając {model_name}...'):
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(f"Auto: {car_model}. Objawy: {symptoms}. Zdiagnozuj usterkę, podaj przyczyny i rozwiązania. Pisz po polsku.")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Wystąpił błąd: {e}")
else:
    st.error("🚨 Nie znaleziono żadnego działającego modelu dla Twojego klucza API.")
    st.info("Sprawdź, czy Twój klucz w Google AI Studio jest aktywny.")
    # Wyświetlamy błąd techniczny, żeby wiedzieć co się dzieje
    try:
        st.write("Dostępne modele (debug):")
        for m in genai.list_models():
            st.code(m.name)
    except Exception as e:
        st.error(f"Błąd łączenia z Google: {e}")
