import base64
import streamlit as st
from openai import OpenAI
from dotenv import dotenv_values
from pypdf import PdfReader
from docx import Document

# --- inicjalizacja klienta OpenAI z kluczem API ---
env = dotenv_values(".env")
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- ustawiam tło z lokalnego dysku
def get_base64_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

try:
    bin_str = get_base64_image('ukraine.jpg')  # Podaj nazwę i rozszerzenie swojego pliku
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{bin_str}");
            background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("data:image/jpeg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
except FileNotFoundError:
    st.warning("Nie znaleziono pliku obrazu 'ukraine.jpg' w folderze projektu.")

# --- WYBÓR MODELU W PANELU BOCZNYM ---
st.sidebar.title("Bot Settings")
selected_model = st.sidebar.selectbox(
    "Select OpenAI model:",
    options=["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
    index=0  # Domyślnie gpt-4o-mini
)

st.markdown(
    """
    <style>
        div[data-baseweb="select"] {
            cursor: pointer !important;
        }
        div[data-testid="stSelectbox"] svg {
            cursor: pointer !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Multimedia Chatbot Assistant")

def read_uploaded_files(uploaded_files):
    documents_text = ""
    for file in uploaded_files:
        # TXT
        if file.type == "text/plain":
            text = file.read().decode("utf-8")
            documents_text += f"\n\n===== FILE: {file.name} =====\n{text}"

        # PDF
        elif file.type == "application/pdf":
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            documents_text += f"\n\n===== FILE: {file.name} =====\n{text}"

        # DOCX
        elif "word" in file.type:
            doc = Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            documents_text += f"\n\n===== FILE: {file.name} =====\n{text}"
            
    return documents_text

# --- FUNKCJA DO PRZETWARZANIA PYTAŃ I PLIKÓW ---
def get_chatbot_reply(user_prompt, model_name, chat_history, documents_text):
    messages = [
        {
            "role": "system",
            "content": """
            You are an expert in everything.
            You answer clearly, concisely, and honestly.
            You also analyze uploaded documents.
            """
        }
    ]

    # Pobieramy historię BEZ ostatniej wiadomości użytkownika 
    messages.extend(chat_history[-21:-1] if len(chat_history) > 1 else [])

    if documents_text:
        current_message = f"User documents:\n{documents_text}\n\nUser question:\n{user_prompt}"
    else:
        current_message = user_prompt

    messages.append({
        "role": "user",
        "content": current_message
    })

    response = openai_client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=1000
    )

    return {
        "role": "assistant",
        "content": response.choices[0].message.content
    }

# Inicjalizacja stanu sesji
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "documents" not in st.session_state:
    st.session_state["documents"] = "" 

# --- KROK 1: Najpierw rezerwujemy miejsce na historię czatu na samej górze ---
chat_container = st.container()

# --- KROK 2: Formularz wpisywania wiadomości na samym dole skryptu ---
with st.form("chat_form", clear_on_submit=True):
    uploaded_files = st.file_uploader(
        "📎 Attach files",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True
    )
    prompt = st.text_input("What would you like to ask?")
    send_button = st.form_submit_button("Send")

# --- KROK 3: Logika po kliknięciu wyślij ---
if send_button and prompt:
    # Przetworzenie plików
    if uploaded_files:
        st.session_state["documents"] = read_uploaded_files(uploaded_files)

    # Przygotowanie wiadomości użytkownika z załącznikami
    user_content = prompt
    if uploaded_files:
        files_info = "\n".join([f" *📎 File uploaded: {file.name}*" for file in uploaded_files])
        user_content = f"{prompt}\n\n{files_info}"
                
    # Zapisujemy do sesji
    st.session_state["messages"].append({"role": "user", "content": user_content})

    # Pobranie odpowiedzi od bota i zapis do sesji
    chatbot_message = get_chatbot_reply(
        prompt,
        selected_model,
        st.session_state["messages"],
        st.session_state["documents"]
    )
    st.session_state["messages"].append(chatbot_message)

# --- KROK 4: Renderowanie historii rozmowy w zarezerwowanym kontenerze ---
# Pętla wykonuje się ZAWSZE i rysuje CAŁĄ zawartość w jednym miejscu NAD formularzem
with chat_container:
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
# --- STOPKA (FOOTER) ---
with st.bottom:
    st.markdown(
        """
        <div style="text-align: center; padding: 10px; font-weight: bold; font-size: 16px;">
            We stand with Ukraine
        </div>
        """,
        unsafe_allow_html=True
    )
  
# ==============================================================================
# --- STYLOWANIE CSS (KOŃCOWY BLOK STYLI) ---
# ==============================================================================
import base64

def get_base64_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

try:
    bin_str = get_base64_image('ukraine.jpg')
    st.markdown(
        f"""
        <style>
        /* 1. Tło główne */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("data:image/jpeg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* 2. Przezroczyste dymki wiadomości czatu */
        div[data-testid="stChatMessage"] {{
            background-color: rgba(15, 20, 30, 0.35) !important;
            border-radius: 12px;
            padding: 12px 16px;
            margin-bottom: 10px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
        }}

        /* 3. Przezroczysta ramka formularza st.form */
        div[data-testid="stForm"] {{
            background-color: rgba(15, 20, 30, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(10px) !important;
        }}

        /* 4. PRZEZROCZYSTE POLE DROPZONE I INPUTY (Rozwiązanie ciemnego prostokąta) */
        [data-testid="stFileUploaderDropzone"],
        [data-testid="stFileUploader"] section,
        div[data-baseweb="input"] > div {{
            background-color: rgba(0, 0, 0, 0.25) !important;
            border: 1px dashed rgba(255, 255, 255, 0.3) !important;
        }}

        /* 5. Przycisk Send (Żółty, lekko przezroczysty) */
        div[data-testid="stFormSubmitButton"] > button {{
            background-color: rgba(255, 215, 0, 0.85) !important;
            color: #000000 !important;
            font-weight: bold !important;
            border: none !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }}

        /* 6. Przycisk Upload (Wszystkie możliwe selektory dla st.file_uploader) */
        [data-testid="stFileUploader"] button,
        [data-testid="stFileUploaderDropzone"] button,
        section[data-testid="stFileUploader"] button {{
            background-color: rgba(255, 215, 0, 0.85) !important;
            color: #000000 !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            border: none !important;
            transition: all 0.3s ease !important;
        }}

        /* Efekt najechania (Hover) dla obu przycisków */
        div[data-testid="stFormSubmitButton"] > button:hover,
        [data-testid="stFileUploader"] button:hover,
        [data-testid="stFileUploaderDropzone"] button:hover {{
            background-color: rgba(255, 215, 0, 1) !important;
            box-shadow: 0 2px 8px rgba(255, 215, 0, 0.5) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
except FileNotFoundError:
    st.warning("Nie znaleziono pliku 'ukraine.jpg' w folderze projektu.")