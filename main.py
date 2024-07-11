# 1. Imports
from openai import OpenAI
import os
#from dotenv import load_dotenv
import streamlit as st

# 2. Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Set Title
st.title("Dongyang High school's ChatGPT")

# 4. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])    

# 6. Model assigining
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# 7. React to user input.
prompt = st.chat_input("메시지 ChatGPT ?")
if prompt:
    # ======== USER CONTAINER ========
    # display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # add message to chat history
    st.session_state.messages.append({'role': 'user', 'content':prompt})

    # ======== ASSISTANT CONTAINER ========
    # display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages], # focus on the loop, helps keep context by simulating a conversation.
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})   