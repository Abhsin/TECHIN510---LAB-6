from tempfile import NamedTemporaryFile
import os
import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Chat with Multiple PDFs",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about your documents!"}
    ]

uploaded_files = st.file_uploader("Upload one or more PDF files", accept_multiple_files=True)

if uploaded_files:
    docs = []
    temp_files = []  # List to store temporary file names
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        with NamedTemporaryFile(delete=False) as tmp:  # open a named temporary file
            tmp.write(bytes_data)  # write data from the uploaded file into it
            temp_files.append(tmp.name)  # Add temporary file name to the list
            reader = PDFReader()
            docs += reader.load_data(tmp.name)

    with st.spinner(
        text="Indexing the documents – this may take a moment."
    ):
        llm = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
            model="gpt-3.5-turbo",
            temperature=0.0,
            system_prompt="You are an expert on the content of the document, provide detailed answers to the questions. Use the document to support your answers.",
        )
        index = VectorStoreIndex.from_documents(docs)

    if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=False, llm=llm
        )

    # Close and remove the temporary files
    for temp_file in temp_files:
        os.remove(temp_file)

if prompt := st.chat_input(
    "Your question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.stream_chat(prompt)
            st.write_stream(response.response_gen)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history