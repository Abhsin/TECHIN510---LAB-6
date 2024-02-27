import streamlit as st
import random
import time

st.set_page_config(
    page_title="Abhi's Lab 6 ",
    page_icon="👋",
)

st.write("# Welcome to LLM's! 👋")

st.sidebar.success("Select a page to view")

st.markdown(
    """Welcome to LLMS (Language Learning Management System), an innovative platform designed to revolutionize language education. LLMS offers a comprehensive suite of tools and resources tailored to enhance language learning experiences for students and educators alike. With state-of-the-art features such as interactive lessons, personalized study plans, and real-time feedback, LLMS empowers learners to master new languages with confidence and efficiency. Whether you're a beginner embarking on your language learning journey or an experienced polyglot seeking to refine your skills, LLMS provides the support and guidance you need to succeed. Join us today and unlock the doors to a world of linguistic exploration and discovery!

"""
)

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
if prompt := st.chat_input("What is up?"):
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