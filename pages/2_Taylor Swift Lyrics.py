import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE"))

# Function to generate lyrics
def generate_lyrics(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Taylor Swift Inspired song lyrics generator."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Main function
def main():
    st.title("Song Lyrics Generator")

    # Text input for user prompt
    st.header("Sample Prompt: Write a song about love and Chainsaws!")
    prompt = st.text_input("Enter a prompt for the lyrics generation:")

    # Generate button to start lyrics generation process
    if st.button("Generate Lyrics"):
        with st.spinner("Your lyrics are being generated. Please wait..."):
            if prompt:
                # Generate lyrics
                lyrics = generate_lyrics(prompt)
                st.write("Generated Lyrics:")
                st.write(lyrics)
            else:
                st.error("Please enter a prompt.")

if __name__ == "__main__":

    main()
    
