# speech_to_query.py
import speech_recognition as sr

def capture_query(timeout=5, phrase_time_limit=8):
    """Listen via default mic and return text or None."""
    r = sr.Recognizer()
    with sr.Microphone() as src:
        print("🎙️  Speak your request…")
        audio = r.listen(src, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        return r.recognize_google(audio)  # free quota; swap in Whisper locally
    except sr.UnknownValueError:
        return None
