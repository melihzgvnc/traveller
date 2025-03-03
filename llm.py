from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from get_flights import get_flight_tickets
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai = OpenAI()



llm = ChatOpenAI(model="gpt-4o-mini")
llm = llm.bind_tools([get_flight_tickets])
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            """You are a helpful assistant that find best flights tickets
            for a given destination. The year we are in is 2025.
            If user did not tell their departure location,
            ask for that info. If user did not provide their desired travel date,
            ask for it. If user did not provide their return date, assume it is a one-way ticket.
            If user did not provide airport information for departure and arrival, ask them to provide. Do not assume the information.

            Once you fetch the data from your tool,
            format it in a tabular form and present to the user.
            Include airport information with their IATA code, price, departure and
            arrival time, duration and date. If it is not a direct flight, then include the layover information.
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


workflow = StateGraph(state_schema=MessagesState)

def call_model(state: MessagesState):
    prompt = prompt_template.invoke(state)
    response = llm.invoke(prompt)
    
    # If the response includes tool calls, process them and create ToolMessage
    if response.additional_kwargs.get("tool_calls"):
        tool_calls = response.additional_kwargs["tool_calls"]
        for tool_call in tool_calls:
            #print(tool_call)
            tool_name = tool_call["function"]["name"]
            tool_args = tool_call["function"]["arguments"]
            tool_args = json.loads(tool_args)
            # Execute the tool and create a ToolMessage
            tool_result = get_flight_tickets.invoke(tool_args)
            #tool_result = get_flight_tickets.invoke(**eval(tool_args))
            tool_message = ToolMessage(
                tool_name=tool_name,
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
            
            # Add the tool message to the state
            state["messages"].append(response)
            state["messages"].append(tool_message)
            
            # Get final response from LLM
            final_response = llm.invoke(prompt_template.invoke(state))
            return {"messages": final_response}
    
    return {"messages": response}

workflow.add_edge(START, "chain")
workflow.add_node("chain", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}



def run(query):
    output = app.invoke({"messages": HumanMessage(query)}, config)
    return output


