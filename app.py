import streamlit as st
import pdfplumber
from docx import Document
from gtts import gTTS

# ---------------- TITLE ----------------
st.title("📘 AudioBook Generator")
st.write("Upload your document and convert it into an audiobook")

# ---------------- SESSION STATE INIT ----------------
if "audiobook_text" not in st.session_state:
    st.session_state.audiobook_text = ""

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload PDF, DOCX or TXT file",
    type=["pdf", "docx", "txt"]
)

# ---------------- TEXT EXTRACTION FUNCTIONS (Member 2) ----------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def extract_text_from_txt(file):
    return file.read().decode("utf-8")


# ---------------- MEMBER 3: AUDIOBOOK STYLE REWRITE ----------------
def rewrite_text_audiobook_style(text):
    if text.strip() == "":
        return ""

    sentences = text.replace("\n", " ").split(".")
    audiobook_text = "🎧 Audiobook Style Version\n\n"

    for sentence in sentences[:7]:
        sentence = sentence.strip()
        if sentence:
            audiobook_text += f"Now listen carefully. {sentence}.\n\n"

    audiobook_text += "This explanation was designed for easy listening."
    return audiobook_text


# ---------------- MEMBER 4: TEXT TO SPEECH ----------------
def text_to_speech(text):
    if text.strip() == "":
        return None

    tts = gTTS(text=text, lang="en")
    audio_file = "audiobook.mp3"
    tts.save(audio_file)
    return audio_file


# ---------------- MAIN LOGIC ----------------
if uploaded_file is not None:
    st.success("File uploaded successfully ✅")
    st.write("📄 File name:", uploaded_file.name)

    file_type = uploaded_file.name.split(".")[-1].lower()
    extracted_text = ""

    if file_type == "pdf":
        extracted_text = extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        extracted_text = extract_text_from_docx(uploaded_file)
    elif file_type == "txt":
        extracted_text = extract_text_from_txt(uploaded_file)

    # -------- Member 2 Output --------
    st.subheader("📝 Extracted Text (Member 2 Output)")
    if extracted_text.strip():
        st.text(extracted_text[:800])
    else:
        st.warning("No text found in document.")

    # -------- Member 3 Output --------
    if st.button("Rewrite in Audiobook Style"):
        with st.spinner("AI is rewriting text..."):
            st.session_state.audiobook_text = rewrite_text_audiobook_style(extracted_text)

    if st.session_state.audiobook_text.strip():
        st.subheader("🎧 Audiobook Style Text (Member 3 Output)")
        st.write(st.session_state.audiobook_text)

    # -------- Member 4 Output --------
    if st.button("Generate Audio"):
        if st.session_state.audiobook_text.strip() == "":
            st.error("Please rewrite text first.")
        else:
            with st.spinner("Converting text to audio..."):
                audio_path = text_to_speech(st.session_state.audiobook_text)

            if audio_path:
                st.success("Audio generated successfully 🎧")

                audio_file = open(audio_path, "rb")
                st.audio(audio_file.read(), format="audio/mp3")

                audio_file.seek(0)
                st.download_button(
                    label="Download AudioBook",
                    data=audio_file,
                    file_name="audiobook.mp3",
                    mime="audio/mp3"
                )
