import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import time
import base64
from dotenv import load_dotenv
import os
import matplotlib
matplotlib.use('TkAgg')  # Set Matplotlib backend to "TkAgg"
import matplotlib.pyplot as plt
import seaborn as sns
load_dotenv()
api_token = os.getenv("API_TOKEN")
print(api_token)
llm = OpenAI(api_token)
st.title("Smart Analyst Chatbot 📊🤖📶")
# Initialize st.session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for CSV upload and API keys
st.sidebar.header("Configuration")
csv_file = st.sidebar.file_uploader("Choose a CSV file 📄", type=["csv"])

if csv_file is not None:
    try:
        df = pd.read_csv(csv_file, low_memory=False)
        df = SmartDataframe(df, config={"llm": llm})
        st.header("Data")
        st.dataframe(df, use_container_width=True)
        prompt = st.text_input('Enter your prompt ⌨')
        if st.button('Generate'):
            if prompt:
                start_time = time.time()
                with st.spinner("Generating response..."):
                    output = df.chat(prompt)
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    # Check for different output types and handle accordingly
                    if isinstance(output, str):
                        st.write(output)  # Display text outputs
                    elif isinstance(output, SmartDataframe):
                        st.dataframe(output)  # Display DataFrame outputs
                    elif isinstance(output, plt.Figure):  # Matplotlib plot
                        # plt.figure(figsize=(8, 6))
                        st.pyplot(output)
                    else:
                        st.write("Output type not recognized.")
                    
                    # Save question and answer to session state
                    st.session_state.messages.append({"prompt": prompt, "output": output})
                st.write("Execution time:", execution_time, "seconds")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Display previous questions and their answers
st.write("## Previous Questions and Answers")
for message in st.session_state.messages:
    st.write(f"**Q 🕵🏻:** {message['prompt']}")
    st.write(f"**A 🤖:** {message['output']}")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('blue-smooth-wall-textured-background.jpg')

hide_st_style = """
    <style>
    #MainMenu footer {visibility: hidden;}
    header {}
    </style> 
"""

st.markdown(hide_st_style, unsafe_allow_html=True)