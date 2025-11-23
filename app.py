import streamlit as st
import google.generativeai as genai

# --- Konfiguracja ---
st.set_page_config(page_title="AI Mechanik", page_icon="🚗")

api_key = st.secrets.get("GOOGLE_API_KEY")

st.title("🚗 Wirtualny Mechanik")

if not api_key:
    st.error("Brak klucza API. Sprawdź ustawienia Secrets.")
    st.stop()

# --- Ustawiamy model na sztywno na 1.5 Flash ---
# To jest najbezpieczniejszy, darmowy model
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Błąd konfiguracji: {e}")

# --- Interfejs ---
car_model = st.text_input("Marka i model pojazdu:")
symptoms = st.text_area("Objawy (opisz dokładnie):", height=150)
btn = st.button("Diagnozuj")

if btn and symptoms:
    with st.spinner('AI analizuje silnik...'):
        try:
            prompt = f"""
            Jesteś mechanikiem. Auto: {car_model}. Objawy: {symptoms}.
            Zdiagnozuj problem, podaj 3 przyczyny i oszacuj koszt/trudność.
            """
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
        except Exception as e:
            # Jeśli nadal będzie błąd, wyświetlimy go dokładnie
            st.error(f"Wystąpił błąd: {e}")
            st.warning("Jeśli widzisz błąd 404, upewnij się, że w pliku requirements.txt masz wpisane: google-generativeai>=0.8.0")

elif btn:
    st.warning("Musisz wpisać objawy!")
