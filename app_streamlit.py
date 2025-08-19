import io
import json
import streamlit as st
from src.config import MAX_DESC_CHARS
from src.utils import sanitize_user_text, safe_merge_body_type
from src.image_classifier import classify_body_type_dummy
from src.extractor import llm_extract_json
from src.emailer import send_email_with_attachments

st.set_page_config(page_title="Car Lister", page_icon="🚗", layout="centered")
st.title("🚗 Car Lister – JSON + Email")

with st.expander("ℹ️ How it works"):
    st.write("""
    1) Upload a car image and enter a description.
    2) We sanitize the text to reduce prompt-injection attempts.
    3) The description is sent to an LLM to extract a strict JSON payload.
    4) A dummy image classifier infers the car **body_type** from the image. (Pluggable later.)
    5) We merge the classifier output into the JSON and email it (JSON + image) to your configured Gmail.
    """)

img = st.file_uploader("Car image", type=["jpg","jpeg","png","webp"])
desc = st.text_area("Text description", height=200, placeholder="e.g., Blue Ford Fusion produced in 2015 ...")

email_preview = st.checkbox("Show email preview instead of sending (dry run)", value=False)

if st.button("Submit"):
    if not img or not desc.strip():
        st.error("Please provide both an image and a description.")
        st.stop()

    # 1) Sanitize input
    safe_text = sanitize_user_text(desc, MAX_DESC_CHARS)

    # 2) Extract JSON
    with st.spinner("Extracting JSON from description..."):
        data = llm_extract_json(safe_text)

    # 3) Dummy image classification
    with st.spinner("Classifying body type from image (dummy)..."):
        body = classify_body_type_dummy(img.getvalue())
        data = safe_merge_body_type(data, body)

    st.subheader("Generated JSON")
    st.json(data)

    # 4) Email
    json_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    body = "Car listing attached.\n\nThis email was sent automatically by Car Lister."
    subject = "New Car Listing"

    if email_preview:
        st.info("Dry run mode: showing what would be emailed.")
        st.code(subject)
        st.code(body)
        st.code(json.dumps(data, indent=2))
    else:
        with st.spinner("Sending email..."):
            send_email_with_attachments(subject, body, json_bytes, img.getvalue(), image_filename=img.name)
        st.success("Email sent!")
