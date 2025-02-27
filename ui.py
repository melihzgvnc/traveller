import streamlit as st
import json
from llm import run
from langchain_core.messages import ToolMessage

st.title("Travel Assistant")

"""
def generate_response(query):
    output = run(query)
    print(output) # -> this here is the key to see tool calls!!!!!!!!!!
    kwargs = output["messages"][-1].additional_kwargs
    response = output["messages"][-1].content
    return (response, kwargs)

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
    response, kwargs = generate_response(prompt)
    st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Add button to sidebar
    with st.sidebar:
        tool_calls_exist = 'tool_calls' in kwargs
        button = st.button(
            "Execute Tool Call", 
            disabled=tool_calls_exist,
            key=f"tool_button_{len(st.session_state.messages)}"
        )
    """

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
  
  button = st.button(
    f"Create Flyer for {data['destination']}",
    disabled=not tool_call_exist,
    key="flyer_button"
  )
