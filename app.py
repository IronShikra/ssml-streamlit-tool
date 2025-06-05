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

selected_tag = st.sidebar.selectbox(
    "Insert Tag",
    ["<emphasis>", "<say-as>", "<sub>", "<lang>", "<voice>", "<phoneme>", "<break>"]
)

# Example logic after the user selects a tag
if selected_tag:
    st.subheader("Tag Behavior")

    tag_descriptions = {
        "<prosody>": "Wraps selected text (paired tag)",
        "<break>": "Inserts at cursor (self-closing tag)",
        "<emphasis>": "Wraps selected text (paired tag)",
        "<speak>": "Wraps entire SSML output (wrapper tag)",
        "<phoneme>": "Wraps selected text (paired tag)",
        "<amazon:auto-breaths>": "Wraps selected text (paired tag)",
        "<p>": "Wraps selected text (paired tag)",
        "<s>": "Wraps selected text (paired tag)",
    }

    tag_behavior = tag_descriptions.get(selected_tag, "Tag behavior info not available.")
    st.markdown(f"**Tag behavior:** {tag_behavior}")

tag_params = {}  # Store parameters to build the tag

if selected_tag == "<emphasis>":
    tag_params["level"] = st.sidebar.selectbox("Level", ["strong", "moderate", "reduced"])

elif selected_tag == "<say-as>":
    tag_params["interpret-as"] = st.sidebar.selectbox("Interpret As", ["date", "time", "digits", "fraction", "characters"])

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
    st.warning("Tag insertion not wired up yet — coming in next step!")


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
