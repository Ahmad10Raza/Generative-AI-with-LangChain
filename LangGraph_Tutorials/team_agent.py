import streamlit as st
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_openai import ChatOpenAI
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

load_dotenv()

# 🗃 Shared state container
class AgentState(TypedDict):
    messages: List[BaseMessage]

# 🔌 Agents with system prompts
def create_agent(role, system_prompt) -> Runnable:
    """Create agent with explicit system message prompt."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    return prompt | llm

planner = create_agent("planner", "You are a project planner. Break the user request into development steps.")
researcher = create_agent("researcher", "You are a researcher. Provide technical background info to help the coder.")
coder = create_agent("coder", "You are a Python programmer. Write complete code for the task.")
reviewer = create_agent("reviewer", "You are a senior software reviewer. Refactor and improve the code.")
tester = create_agent("tester", "You are a code tester. Simulate executing the code and describe the result.")

# 🧱 Safe wrapper for agent node execution
def safe_node(agent, label):
    def node(state: AgentState):
        try:
            response = agent.invoke(state["messages"])
            state["messages"].append(response)
            return {"messages": state["messages"]}
        except Exception as e:
            error_msg = f"{label} failed with error: {e}"
            state["messages"].append(HumanMessage(content=error_msg))
            return {"messages": state["messages"]}
    return node

# 📊 Build LangGraph
builder = StateGraph(AgentState)
builder.add_node("planner", safe_node(planner, "Planner"))
builder.add_node("researcher", safe_node(researcher, "Researcher"))
builder.add_node("coder", safe_node(coder, "Coder"))
builder.add_node("reviewer", safe_node(reviewer, "Reviewer"))
builder.add_node("tester", safe_node(tester, "Tester"))

builder.set_entry_point("planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "coder")
builder.add_edge("coder", "reviewer")
builder.add_edge("reviewer", "tester")
builder.add_edge("tester", END)

graph = builder.compile()

# 🌐 Streamlit UI
st.set_page_config(page_title="LangGraph AI Team", layout="centered")
st.title("🔷 LangGraph AI Task Solver")

user_input = st.text_area("Enter a software development task:", "Create a Python function to scrape all links from a webpage.")

if st.button("🚀 Run Agents"):
    with st.spinner("Running AI agents..."):
        try:
            init_state = {"messages": [HumanMessage(content=user_input)]}
            result = graph.invoke(init_state)
            st.success("Completed!")

            st.subheader("📦 Final State Keys:")
            st.write(result.keys())

            st.subheader("📜 Conversation:")
            for msg in result["messages"]:
                role = "User" if isinstance(msg, HumanMessage) else "AI"
                st.markdown(f"**{role}:** {msg.content}")
        except Exception as e:
            st.exception(e)
