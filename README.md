# Multimedia Chatbot Assistant

A Python-based Chatbot web application built with Streamlit and the official OpenAI API. This project enables interactive conversations with advanced Large Language Models (LLMs) and features contextual analysis of uploaded documents using a simplified RAG / In-Context Learning mechanism.

[View the live application](https://vados182-streamlit-openai-chatbot-app-m3ly6e.streamlit.app/)

## 🚀 Key Features

* **Real-Time Model Selection:** Dynamically switch models via the sidebar interface. Supported models include `gpt-4o-mini`, `gpt-4o`, `gpt-4-turbo`, and `gpt-3.5-turbo`.
* **Multi-Format Document Processing:** The chatbot can extract, merge, and analyze content from multiple files simultaneously. Supported formats include:
  * **PDF** (via `pypdf`)
  * **DOCX** (via `python-docx`)
  * **TXT** (standard UTF-8 encoding)
* **Chat History Management:** Maintains conversation context within the active user session (`st.session_state`), passing the recent message history to the API (memory buffer up to the last 20 messages).
* **Intuitive User Interface (UX):** Built with Streamlit forms (`st.form`) featuring automatic input field resetting upon submission and dynamic message history rendering positioned above the input panel.
* **Custom CSS Styling:** Enhanced UI aesthetics through custom CSS injections (e.g., forcing a pointer cursor on selectbox elements).