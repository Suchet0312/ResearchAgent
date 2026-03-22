from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from tools import web_search,fetch_page
import requests
import json

llm = ChatOllama(model="mistral")

# OLLAMA_URL = "http://localhost:11434/api/chat"
# MODEL_NAME = "mistral"

# tools_definition = [
#     {
#         "type": "function",
#         "function": {
#             "name": "web_search",
#             "description": "Search the web for information on a topic. Use this first to find relevant URLs.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "query": {
#                         "type": "string",
#                         "description": "The search query"
#                     }
#                 },
#                 "required": ["query"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "fetch_page",
#             "description": "Read the full content of a webpage. Use this after web_search to get details from a URL.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "url": {
#                         "type": "string",
#                         "description": "The full URL to fetch"
#                     }
#                 },
#                 "required": ["url"]
#             }
#         }
#     }
# ]

# def call_ollama(messages):
#     response = requests.post(OLLAMA_URL,json={
#         "model":MODEL_NAME,
#         "messages":messages,
#         "tools":tools_definition,
#         "stream":False
#     })
#     return response.json()

@tool
def search_web(query:str)->str:
    """Search the web for information on a topic. Use this first to find relevant URLs."""
    results = web_search(query)
    return str(results)

@tool
def read_page(url:str)->str:
    """Read the full content of a webpage. Use this after search_web to get details from a URL."""
    return fetch_page(url)

tools = [search_web, read_page]
agent = create_react_agent(llm, tools)

def run_agent(topic: str) -> str:
    print(f"\n🤖 Starting research on: {topic}\n")
    
    messages = [HumanMessage(content=f"""Research this topic thoroughly and write a clear report: {topic}

Use search_web to find sources, then read_page to read them in detail.
When you have enough information write a structured report with:
- Key findings
- Important details
- Your sources (URLs)""")]

    result = agent.invoke({"messages": messages})
    
    final_message = result["messages"][-1]
    return final_message.content

if __name__ == "__main__":
    while True:
        a = input("\nEnter research topic (or 'bye' to quit): ")
        if a.lower() == "bye":
            break
        result = run_agent(a)
        print(result)

