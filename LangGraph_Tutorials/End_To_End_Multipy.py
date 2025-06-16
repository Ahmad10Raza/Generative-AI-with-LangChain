from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.agents import tool, initialize_agent, AgentType
from langchain.agents.agent_toolkits import Tool
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage

# Step 1: Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers"""
    return a * b

@tool
def reverse_string(text: str) -> str:
    """Reverses a string"""
    return text[::-1]

tools = [Tool.from_function(multiply), Tool.from_function(reverse_string)]

# Step 2: Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Step 3: Initialize LLM and Agent
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True
)

# Step 4: Define Graph Nodes

def input_node(state):
    print("🔹 User Input:", state['input'])
    return state

def agent_node(state):
    messages = [HumanMessage(content=state["input"])]
    response = agent.invoke({"input": state["input"]})
    state["response"] = response["output"]
    return state

def output_node(state):
    print("🤖 AI Response:", state["response"])
    return state

# Step 5: Create Graph
workflow = StateGraph(dict)

workflow.add_node("input", RunnableLambda(input_node))
workflow.add_node("agent", RunnableLambda(agent_node))
workflow.add_node("output", RunnableLambda(output_node))

workflow.set_entry_point("input")
workflow.add_edge("input", "agent")
workflow.add_edge("agent", "output")
workflow.set_finish_point("output")

graph = workflow.compile()

# Step 6: Run the Graph
inputs = {"input": "What is 6 * 9? Then reverse 'LangGraph'."}
graph.invoke(inputs)
