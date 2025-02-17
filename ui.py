import streamlit as st
import numpy as np
import pandas as pd
import time
from llm import run

st.title("Travel Assistant")


def generate_response(query):
    output = run(query)
    response = output["messages"][-1].content
    return response

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("What's up?"):
  st.session_state.messages.append({"role": "user", "content": prompt})

  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    response = generate_response(prompt)
    st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
