
**Components**
- **GUI**: Streamlit app collects image + description and triggers the pipeline.
- **Sanitizer**: Blocks common prompt-injection patterns, trims length, removes URLs/emails.
- **LLM Extractor**: GPT-4o mini (Azure) coerced to strict JSON; post-validated and normalized.
- **Dummy Classifier**: Placeholder for future CV body type model.
- **Merger**: Injects body_type into LLM JSON.
- **Emailer**: Sends JSON + image to the designated Gmail address.
