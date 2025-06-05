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

# Presets
presets = load_presets()
preset_names = list(presets.keys())
selected_preset = st.selectbox("Select a preset", preset_names)
selected_tags = presets.get(selected_preset, "")

# Prosody settings
rate = st.slider("Whole track prosody rate", min_value=20, max_value=200, value=100, step=10, format="%d%%")
pitch = st.selectbox("Whole track prosody pitch", options=["x-low", "low", "medium", "high", "x-high"], index=2)
volume = st.selectbox("Whole track prosody volume", options=["silent", "x-soft", "soft", "medium", "loud", "x-loud"], index=3)

# Toggles
add_s_and_p = st.checkbox("Add brief pauses after sentences and paragraphs using <s> and <p> tags")
add_em_dash = st.checkbox("Add a longer pause after sentences using —")

# Input text
input_text = st.text_area("Paste or type your text below:", height=200)

# Output
if st.button("Generate SSML Output"):
    clean = clean_text(input_text)
    body = add_ssml_tags(clean, add_s_and_p, add_em_dash)
    ssml = f"<speak><prosody rate=\"{rate}\" pitch=\"{pitch}\" volume=\"{volume}\"> {body} </prosody></speak>"
    st.text_area("SSML Output", value=ssml, height=300)
