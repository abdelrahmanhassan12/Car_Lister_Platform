# Car Lister – User Manual

## 1. Prereqs
- **Python 3.10+** (Windows/macOS/Linux PC)
- A Gmail account with an **App Password** (2FA required). See: Google Account → Security → App passwords.
- Azure OpenAI access (deployment of GPT-4o mini or another model).

## 2. Setup
```bash
git clone <your-private-repo-url>.git car_lister
cd car_lister
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` in the project root:
```env
# --- Azure OpenAI ---
AZURE_OPENAI_API_KEY=YOUR_AZURE_KEY
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_ENDPOINT=https://your-endpoint.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini-AH320

# --- Gmail ---
GMAIL_USER=youraddress@gmail.com
GMAIL_APP_PASSWORD=your_app_password   # 16 chars from Google
DEST_EMAIL=recipient@gmail.com         # where to send the JSON + image

# --- Safety/limits ---
MAX_DESC_CHARS=2000
```

> **Note:** You were provided test creds in the brief. For security and auditability, prefer setting them in `.env` rather than hardcoding.


## 3. Run
```bash
streamlit run app_streamlit.py
```
- Upload a car image and paste the description.
- Optionally tick **"Show email preview instead of sending"** to dry-run without emailing.
- Click **Submit**. The email is sent a few seconds later.

## 4. Prompt-Injection Mitigations
- Input sanitizer truncates long text, strips control chars, removes URLs/emails, and scrubs common “ignore previous instructions” patterns.
- Strong **system prompt** forces JSON-only output aligning to a fixed schema.
- Post-parse validation ensures the response is strictly JSON (no markdown) and normalizes price values.
- Dry-run mode allows manual inspection before sending.

> These are simple defenses. Additional hardening ideas: allowlisted vocab for specific fields, regexes for years/cc, sandboxed parsing, and JSON schema validation with Pydantic.

## 5. Replacing the Dummy Classifier
- Implement your CV model in `src/image_classifier.py` as `classify_body_type(image_bytes: bytes) -> str`.
- Update the import in `app_streamlit.py` accordingly.

## 6. Cost Control
- The description is sanitized and truncated (`MAX_DESC_CHARS`).
- LLM temperature = 0, max_tokens limited (500).
- JSON-only output (no chit-chat) reduces overhead.

## 7. Troubleshooting
- **Email fails**: Ensure Gmail 2FA + App Password, and `.env` vars are set. Corporate Gmail may block SMTP.
- **JSON errors**: The app will retry the LLM up to 3 times with exponential backoff.
- **Firewall**: Allow outbound HTTPS (Azure OpenAI) + SMTP 587.

## 8. Files
- `app_streamlit.py` – GUI entrypoint.
- `src/extractor.py` – LangChain LLM extraction.
- `src/image_classifier.py` – dummy body-type classifier.
- `src/emailer.py` – SMTP email sender.
- `src/utils.py` – sanitization & normalization helpers.
- `src/config.py` – config/env loader.
- `DESIGN.md` – architecture + Mermaid diagram.
- `prompt_solution_creation.txt` – one-shot prompt for LLM-powered IDE to scaffold this project.
