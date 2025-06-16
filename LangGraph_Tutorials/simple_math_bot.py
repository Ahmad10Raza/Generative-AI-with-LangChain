from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

# Load OpenAI API Key
load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Tool to multiply two numbers
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

# Create the agent
agent = create_react_agent(
    model=llm,
    tools=[multiply],
    prompt="You are a smart assistant that answers math questions using only the multiply tool."
)

# Input and invoke
if __name__ == "__main__":
    question = input("🧠 Ask me a math question: ")
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    
    # ✅ Extract the last AI message for final response
    if "messages" in result and result["messages"]:
        final_message = result["messages"][-1]
        print("🤖", final_message.content)
    else:
        print("🤖 Could not find output in result:", result)
