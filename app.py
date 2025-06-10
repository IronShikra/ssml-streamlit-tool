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
    ["Select a tag...", "<emphasis>", "<say-as>", "<sub>", "<lang>", "<voice>", "<phoneme>", "<break>"],
    help="Choose a tag to apply. Tags either wrap selected text or insert at cursor."
)

# Define descriptions for each tag based on the reference guide
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

# Show behavior description
if selected_tag and selected_tag != "Select a tag...":
    behavior_text = tag_descriptions.get(selected_tag, "Unknown behavior")
    st.sidebar.markdown(f"<span style='font-size: 0.85em; color: gray;'>Tag behavior: {behavior_text}</span>", unsafe_allow_html=True)
    # [Your tag-specific input logic here]

tag_params = {}  # Store parameters to build the tag

if selected_tag == "<emphasis>":
    tag_params["level"] = st.sidebar.selectbox(
        "Level",
        ["strong", "moderate", "reduced"],
        help="Wraps selected text to add vocal emphasis."
    )

elif selected_tag == "<say-as>":
    tag_params["interpret-as"] = st.sidebar.selectbox(
    "Interpret As",
    ["date", "time", "digits", "fraction", "characters"],
    help="Controls how the text is read aloud. For example, 'digits' reads numbers individually."
)

elif selected_tag == "<sub>":
    tag_params["alias"] = st.sidebar.text_input("Alias (replacement text)")

elif selected_tag == "<lang>":
    tag_params["xml:lang"] = st.sidebar.text_input("Language Code (e.g., en-US)")

elif selected_tag == "<voice>":
    tag_params["name"] = st.sidebar.text_input("Voice Name (platform-specific)")

elif selected_tag == "<phoneme>":
    tag_params["alphabet"] = st.sidebar.selectbox("Alphabet", ["ipa", "x-sampa"])
    tag_params["ph"] = st.sidebar.text_input("Phoneme String")

elif selected_tag == "<break>":
    break_method = st.sidebar.radio("Set Break By:", ["Strength", "Time"])
    if break_method == "Strength":
        tag_params["strength"] = st.sidebar.selectbox("Strength", ["none", "x-weak", "weak", "medium", "strong", "x-strong"])
    else:
        tag_params["time"] = st.sidebar.text_input("Time (e.g., 500ms)")

if st.sidebar.button("Insert Tag"):
    tag_text = ""

    if selected_tag == "<emphasis>":
        level = tag_params.get("level", "moderate")
        tag_text = f"<emphasis level=\"{level}\">{{text}}</emphasis>"

    elif selected_tag == "<say-as>":
        interpret_as = tag_params.get("interpret-as", "characters")
        tag_text = f"<say-as interpret-as=\"{interpret_as}\">{{text}}</say-as>"

    elif selected_tag == "<sub>":
        alias = tag_params.get("alias", "")
        tag_text = f"<sub alias=\"{alias}\">{{text}}</sub>"

    elif selected_tag == "<lang>":
        lang = tag_params.get("xml:lang", "en-US")
        tag_text = f"<lang xml:lang=\"{lang}\">{{text}}</lang>"

    elif selected_tag == "<voice>":
        voice = tag_params.get("name", "")
        tag_text = f"<voice name=\"{voice}\">{{text}}</voice>"

    elif selected_tag == "<phoneme>":
        alphabet = tag_params.get("alphabet", "ipa")
        ph = tag_params.get("ph", "")
        tag_text = f"<phoneme alphabet=\"{alphabet}\" ph=\"{ph}\">{{text}}</phoneme>"

    elif selected_tag == "<break>":
        if "strength" in tag_params:
            strength = tag_params["strength"]
            tag_text = f"<break strength=\"{strength}\"/>"
        elif "time" in tag_params:
            time = tag_params["time"]
            tag_text = f"<break time=\"{time}\"/>"

    # Insert tag logic
    if "{{text}}" in tag_text:
        st.session_state.input_text_area += tag_text.replace("{{text}}", "your text here")
    else:
        st.session_state.input_text_area += tag_text

# --- MAIN PANEL ---
st.markdown(
    """
    <div style="padding:10px; border-left: 4px solid #1e90ff;">
        <strong>Note:</strong> If this app was asleep, it may take a few seconds to wake up. Try again if needed.
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
