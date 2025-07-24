import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env
load_dotenv()

# Set up Gemini model using your API key
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Define the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
    ("human", "{input}"),
])

# Output parser
output_parser = StrOutputParser()

# Combine the prompt, model, and parser into a chain
chain = prompt | llm | output_parser

# Streamlit UI
st.title('Langchain Translator using Gemini')

# Input box
input_text = st.text_input("Enter text in any language:")

# Language selection
languages = [
    "Urdu", "German", "French", "Spanish", "Arabic",
    "Hindi", "Chinese", "Russian", "Turkish", "Japanese"
]
selected_language = st.selectbox("Select language to translate to:", languages)

# Translation trigger
if input_text and selected_language:
    response = chain.invoke({
        "input_language":  selected_language,
        "output_language": selected_language,
        "input": input_text
    })

    st.markdown(f"### Translated ({selected_language}):")
    st.write(response)
