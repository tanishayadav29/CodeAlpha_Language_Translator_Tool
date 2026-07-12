import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import os

st.set_page_config(page_title="AI Translator", page_icon="🌍", layout="centered")

# ---------- UI HEADER ----------
st.markdown(
    "<h1 style='text-align:center; color:#4CAF50;'>🌍 Language Translator</h1>",
    unsafe_allow_html=True
)

# ---------- LANGUAGE DICTIONARY ----------
languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN"
}

# ---------- INPUT ----------
text = st.text_area("Enter text here", height=150)

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("From", list(languages.keys()))

with col2:
    target_lang = st.selectbox("To", list(languages.keys()))

# ---------- TRANSLATE ----------
if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter some text")
    else:
        translated_text = GoogleTranslator(
            source=languages[source_lang],
            target=languages[target_lang]
        ).translate(text)

        st.session_state["translated"] = translated_text
        st.session_state["target_lang"] = languages[target_lang]

# ---------- OUTPUT ----------
if "translated" in st.session_state:
    st.markdown("### 📄 Translated Text")
    st.success(st.session_state["translated"])
    st.code(st.session_state["translated"])

    if st.button("🔊 Listen Translation"):
        try:
            # gTTS uses "zh-CN" differently, so convert it to "zh-cn"
            audio_lang = st.session_state["target_lang"].lower()

            tts = gTTS(
                text=st.session_state["translated"],
                lang=audio_lang
            )

            audio_file = "speech.mp3"
            tts.save(audio_file)

            with open(audio_file, "rb") as f:
                audio_bytes = f.read()

            st.audio(audio_bytes, format="audio/mpeg")

        except Exception as e:
            st.error(f"Audio error: {e}")
            
# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built with Python + Streamlit + Google Translator API")