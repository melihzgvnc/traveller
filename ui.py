import streamlit as st
import json
from llm import run
from langchain_core.messages import ToolMessage
from gather_flyer_data import gather_data

st.title("Travel Assistant")


with open("data.json", "r") as f:
  data = json.load(f)
  

def generate_response(query):
    output = run(query)
    print(output) # -> this here is the key to see tool calls!!!!!!!!!!
    response = output["messages"][-1]
    return output

if "messages" not in st.session_state:
  st.session_state.messages = []

if "tool_called" not in st.session_state:
  st.session_state.tool_called = False

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("What's up?"):
  st.session_state.messages.append({"role": "user", "content": prompt})

  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    output = generate_response(prompt)
    response = output["messages"][-1].content
    st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    if isinstance(output["messages"][-2], ToolMessage):
      st.session_state.tool_called = True 

with st.sidebar:

  tool_call_exist = False
  print(tool_call_exist)

  if st.session_state.tool_called:
      tool_call_exist = True
  
  generate_button = st.button(
    f"Design Flyer",
    disabled=not tool_call_exist,
    key="generate_flyer_button",
    type="primary"
  )

  if generate_button:
    gather_data()
    st.write("Your flyer has been designed successfully!")

    # Change regular button to download_button
    with open(f"{data['destination']}-flyer.pdf", "rb") as pdf_file:
      st.download_button(
          label="Download your unique flyer",
          data=pdf_file,
          file_name=f"{data['destination']}-flyer.pdf",
          mime="application/pdf",
          key="download_flyer_button"  # Fixed typo in key name
      )

    with open(f"{data['destination']}.jpg", "rb") as file:
      st.download_button(
          label="Download the AI Art",
          data=file,
          file_name=f"{data['destination']}.jpg",
          mime="image/jpg",
      )