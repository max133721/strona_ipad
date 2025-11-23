import streamlit as st
import google.generativeai as genai
import os

# --- Konfiguracja Strony ---
st.set_page_config(page_title="AI Mechanik", page_icon="🚗")

st.title("🚗 Wirtualny Mechanik AI")
st.write("Opisz, co dzieje się z Twoim samochodem, a AI spróbuje zdiagnozować problem.")

# --- Pasek boczny (Sidebar) na klucz API ---
# W wersji publicznej klucz ukryjemy w ustawieniach serwera,
# ale dla testów lokalnych można go wpisać tutaj lub pobrać ze zmiennych środowiskowych.
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.warning("Brak klucza API. Aplikacja może nie działać poprawnie w środowisku lokalnym bez konfiguracji.")
    st.stop()

# --- Konfiguracja AI ---
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

except Exception as e:
    st.error(f"Błąd konfiguracji API: {e}")

# --- Interfejs Użytkownika ---
car_model = st.text_input("Marka i model pojazdu (opcjonalnie):", placeholder="np. Volkswagen Golf 5 1.9 TDI")
symptoms = st.text_area("Opisz objawy:", placeholder="np. Silnik szarpie na niskich obrotach, słychać stukanie z prawej strony...", height=150)

analyze_button = st.button("Diagnozuj Usterkę 🛠️")

# --- Logika Aplikacji ---
if analyze_button and symptoms:
    if not api_key:
        st.error("Proszę podać klucz API, aby kontynuować.")
    else:
        with st.spinner('Analizuję objawy... to może chwilę potrwać...'):
            try:
                # Inżynieria Promptu (Instrukcja dla AI)
                prompt = f"""
                Jesteś doświadczonym mechanikiem samochodowym. Użytkownik zgłasza problem.
                
                Pojazd: {car_model if car_model else "Nieznany"}
                Objawy: {symptoms}
                
                Twoje zadanie:
                1. Podaj 3 najbardziej prawdopodobne przyczyny usterki.
                2. Dla każdej przyczyny oszacuj poziom trudności naprawy (Łatwy/Średni/Trudny).
                3. Podaj orientacyjne kroki, jak to sprawdzić.
                4. Dodaj ostrzeżenie, że jesteś AI i należy skonsultować się z żywym mechanikiem.
                
                Odpowiedź sformatuj w czytelnym Markdown. Używaj polskich terminów technicznych.
                """
                
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Wystąpił błąd podczas łączenia z AI: {e}")
elif analyze_button and not symptoms:
    st.warning("Musisz opisać objawy, aby uzyskać diagnozę.")

# --- Stopka ---
st.markdown("---")
st.caption("⚠️ Uwaga: To narzędzie wykorzystuje sztuczną inteligencję. Wyniki są tylko sugestią. Zawsze skonsultuj się z profesjonalnym warsztatem przed podjęciem naprawy.")
