import streamlit as st
import json
import re

# Load presets
def load_presets():
    try:
        with open("presets.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Escape reserved characters
def escape_reserved_characters(text):
    escape_map = {
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;'
    }
    for char, escape in escape_map.items():
        text = text.replace(char, escape)
    return text

# Clean multiple spaces
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

# Insert <s> and <p> tags, optionally followed by em dash
def add_ssml_tags(text, add_s_and_p, add_em_dash):
    sentences = re.split(r'(?<=[.!?:])\s+', text.strip())
    tagged = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            if add_s_and_p:
                s_tagged = f"<s>{escape_reserved_characters(sentence)}</s>"
                if add_em_dash:
                    s_tagged += " —"
                tagged.append(s_tagged)
            elif add_em_dash:
                sentence += " —"
                tagged.append(escape_reserved_characters(sentence))
            else:
                tagged.append(escape_reserved_characters(sentence))
    if add_s_and_p:
        return f"<p>{' '.join(tagged)}</p>"
    else:
        return ' '.join(tagged)

# UI
st.title("SSML Tagging Tool (Web Version)")
st.write("Add prosody and pauses to SSML text.")

# === SIDEBAR CONTROLS ===
with st.sidebar:
    st.markdown("## Settings")
   
    # Section: Wrapper
    st.markdown("### Wrap Output")
    wrap_speak = st.checkbox("Wrap the SSML output in `<speak>` tags", value=True)

    # Section: Whole Track Prosody
    st.markdown("### Whole Track Prosody")
    prosody_rate = st.slider("Rate (%)", min_value=20, max_value=200, value=100)
    prosody_pitch = st.selectbox("Pitch", ["x-low", "low", "medium", "high", "x-high"], index=2)
    prosody_volume = st.selectbox("Volume", ["silent", "x-soft", "soft", "medium", "loud", "x-loud"], index=3)

    # Section: Pauses
    st.markdown("### Pauses – Sentences and Paragraphs")
    pause_ssml = st.checkbox("Add brief pauses using `<s>` and `<p>` tags")
    pause_dash = st.checkbox("Add longer pause after sentences using —")

    # Section: Presets (if already implemented)
    st.markdown("### Presets")
    # (existing preset controls stay here)


# --- MAIN PANEL ---

st.title("SSML Tagging Tool")

# Text input area (where users paste their script)
input_text = st.text_area("Paste your script text here", height=300)

# Define output_text with a default to avoid NameError
output_text = ""

# Generate SSML Output button
if st.button("Generate SSML Output"):
    # Replace this with your actual SSML generation logic
    output_text = generate_ssml(input_text)

# Output area for SSML
st.text_area("Generated SSML Output", value=output_text, height=300)
