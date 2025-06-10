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

# ─────────────────────────────
# Additional Tags Section
# ─────────────────────────────
st.sidebar.markdown("### Additional Tags")

tag_options = ["Select a tag...", "<emphasis>", "<say-as>", "<sub>", "<lang>", "<voice>", "<phoneme>", "<break>"]
selected_tag = st.sidebar.selectbox(
    "Insert Tag",
    tag_options,
    help="Choose a tag to apply. Tags either wrap selected text or insert at cursor."
)

# Tag behavior descriptions
tag_descriptions = {
    "<speak>": "Wraps entire SSML output",
    "<prosody>": "Wraps selected text",
    "<break>": "Inserts at cursor",
    "<emphasis>": "Wraps selected text",
    "<say-as>": "Wraps selected text",
    "<sub>": "Wraps selected text",
    "<lang>": "Wraps selected text",
    "<p>": "Wraps selected text",
    "<s>": "Wraps selected text",
    "<voice>": "Wraps selected text",
    "<amazon:auto-breaths>": "Wraps selected text",
    "<amazon:effect>": "Wraps selected text",
    "<phoneme>": "Wraps selected text"
}

# Show behavior
if selected_tag != "Select a tag...":
    behavior_text = tag_descriptions.get(selected_tag, "Unknown behavior")
    st.sidebar.markdown(f"<span style='font-size: 0.85em; color: gray;'>Tag behavior: {behavior_text}</span>", unsafe_allow_html=True)

    tag_params = {}
    tag_text = ""

    # Inputs for each tag
    if selected_tag == "<emphasis>":
        level = st.sidebar.selectbox("Level", ["strong", "moderate", "reduced"])
        tag_text = f"<emphasis level=\"{level}\">{{text}}</emphasis>"

    elif selected_tag == "<say-as>":
        interpret_as = st.sidebar.selectbox("Interpret As", ["date", "time", "digits", "fraction", "characters"])
        tag_text = f"<say-as interpret-as=\"{interpret_as}\">{{text}}</say-as>"

    elif selected_tag == "<sub>":
        alias = st.sidebar.text_input("Alias (replacement text)")
        tag_text = f"<sub alias=\"{alias}\">{{text}}</sub>"

    elif selected_tag == "<lang>":
        lang = st.sidebar.text_input("Language Code (e.g., en-US)")
        tag_text = f"<lang xml:lang=\"{lang}\">{{text}}</lang>"

    elif selected_tag == "<voice>":
        voice = st.sidebar.text_input("Voice Name (platform-specific)")
        tag_text = f"<voice name=\"{voice}\">{{text}}</voice>"

    elif selected_tag == "<phoneme>":
        alphabet = st.sidebar.selectbox("Alphabet", ["ipa", "x-sampa"])
        ph = st.sidebar.text_input("Phoneme String")
        tag_text = f"<phoneme alphabet=\"{alphabet}\" ph=\"{ph}\">{{text}}</phoneme>"

    elif selected_tag == "<break>":
        break_method = st.sidebar.radio("Set Break By:", ["Strength", "Time"])
        if break_method == "Strength":
            strength = st.sidebar.selectbox("Strength", ["none", "x-weak", "weak", "medium", "strong", "x-strong"])
            tag_text = f"<break strength=\"{strength}\"/>"
        else:
            time = st.sidebar.text_input("Time (e.g., 500ms)")
            tag_text = f"<break time=\"{time}\"/>"

    # Insert tag on button click
    if st.sidebar.button("Insert Tag"):
        if "{{text}}" in tag_text:
            tag_text = tag_text.replace("{{text}}", "your text here")
        st.session_state.input_text_area = st.session_state.get("input_text_area", "") + tag_text


# --- MAIN PANEL ---
st.markdown(
    """
    <div style="padding:10px; border-left: 4px solid #1e90ff;">
        <strong>❗Note:</strong> If this app was asleep, it may take a few seconds to wake up. Try again if needed.
    </div>
    """,
    unsafe_allow_html=True
)

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
