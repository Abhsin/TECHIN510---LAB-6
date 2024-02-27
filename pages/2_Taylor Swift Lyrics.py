from tempfile import NamedTemporaryFile
import os
import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import random
import time

load_dotenv()

st.set_page_config(
    page_title="Taylor Swift Lyrics Generation",
    page_icon="🎤",
)

st.write("# Welcome to Taylor's Lyrics Generator! 👋")

st.sidebar.success("Select a page to view")

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Basic Chat App with Streamlit Components")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Taylor Swift Lyrics Generation
user_lyrics = st.text_area("Enter your lyrics to generate Taylor Swift-style lyrics")

if st.button("Generate Taylor Swift-style Lyrics"):
    if user_lyrics:
        # Initialize OpenAI client
        try:
            llm = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE"),
                model="gpt-3.5-turbo",
                temperature=0.0,
            )

            # Generate Taylor Swift-style lyrics based on user input
            response = llm.completion.create(
                model="text-davinci-003",
                prompt=user_lyrics,
                max_tokens=50,
                temperature=0.7,
                stop=["\n"]
            )

            generated_lyrics = response.choices[0].text.strip()
            st.write(generated_lyrics)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some lyrics to generate Taylor Swift-style lyrics.")
