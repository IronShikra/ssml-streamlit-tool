import streamlit as st

# --- SIDEBAR CONTROLS ---
st.sidebar.title("SSML Settings")

# Wrapper toggle
wrap_speak = st.sidebar.checkbox("Wrap output in <speak> tags", value=True)

# Whole track prosody settings
st.sidebar.subheader("Whole Track Prosody")
prosody_rate = st.sidebar.slider("Prosody Rate (%)", 20, 200, 100)
prosody_pitch = st.sidebar.selectbox("Prosody Pitch", ["x-low", "low", "medium", "high", "x-high"], index=2)
prosody_volume = st.sidebar.selectbox("Prosody Volume", ["silent", "x-soft", "soft", "medium", "loud", "x-loud"], index=3)

# Pause options
st.sidebar.subheader("Pauses - All Sentences and Paragraphs")
pause_ssml = st.sidebar.checkbox("Add brief pauses after sentences and paragraphs using <s> and <p> tags")
pause_dash = st.sidebar.checkbox("Add a longer pause after sentences using —")

# --- MAIN PANEL ---
st.title("SSML Tagging Tool")

input_text = st.text_area("Paste your script text here", height=300)
output_text = ""

def generate_ssml(text):
    import re

    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Sentence segmentation with optional <s> tags
    if pause_ssml:
        sentences = re.split(r'(?<=[.!?:])\s+', text)
        sentences = [f"<s>{s.strip()}</s>" + (" — " if pause_dash else "") for s in sentences]
        paragraph = " ".join(sentences)
        text = f"<p>{paragraph}</p>"
    elif pause_dash:
        text = re.sub(r'([.!?:])', r'\1 —', text)

    # Apply prosody
    prosody_tag = f'<prosody rate="{prosody_rate}%" pitch="{prosody_pitch}" volume="{prosody_volume}">{text}</prosody>'

    # Wrap in <speak> if selected
    if wrap_speak:
        return f"<speak>{prosody_tag}</speak>"
    else:
        return prosody_tag

# Generate button
if st.button("Generate SSML Output"):
    output_text = generate_ssml(input_text)

# Output display
st.text_area("Generated SSML Output", value=output_text, height=300)
