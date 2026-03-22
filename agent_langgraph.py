import json
from typing import TypedDict,Annotated
from langgraph.graph import StateGraph,END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,AIMessage
import operator
from tools import web_search,fetch_page

class AgentState(TypedDict):
    topic:str
    plan:list[str]
    search_results: Annotated[list,operator.add]
    report:str

llm = ChatOllama(model="mistral")

def plan_node(state: AgentState) -> dict:
    print(f"\n📋 Planning research for: {state['topic']}")
    
    prompt = f"""You are a research planner. Given a topic, generate 3 specific search queries to research it thoroughly.

Topic: {state['topic']}

Respond with ONLY a JSON array of 3 search queries like this:
["query 1", "query 2", "query 3"]

Nothing else. Just the JSON array."""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        queries = json.loads(response.content)
    except:
        queries = [state['topic']]
    
    print(f"   → Plan: {queries}")
    return {"plan": queries}


def search_node(state: AgentState) -> dict:
    print(f"\n🔍 Searching for {len(state['plan'])} queries...")
    
    all_results = []
    
    for query in state['plan']:
        print(f"   → Searching: {query}")
        results = web_search(query)
        
        for result in results[:2]:
            if result.get('url'):
                print(f"   → Fetching: {result['url']}")
                content = fetch_page(result['url'])
                all_results.append({
                    "query": query,
                    "url": result['url'],
                    "content": content
                })
    
    print(f"   → Got {len(all_results)} total results")
    return {"search_results": all_results}

def write_report_node(state: AgentState) -> dict:
    print(f"\n📝 Writing report...")
    
    context = ""
    for result in state['search_results']:
        context += f"\nSource: {result['url']}\n"
        context += f"Query: {result['query']}\n"
        context += f"Content: {result['content'][:500]}\n"
        context += "-" * 40 + "\n"
    
    prompt = f"""You are a research writer. Based on the following research results, write a clear and structured report.

Topic: {state['topic']}

Research Results:
{context}

Write a structured report with:
- Key findings
- Important details
- Your sources (URLs)"""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"report": response.content}

graph = StateGraph(AgentState)

graph.add_node("plan", plan_node)
graph.add_node("search", search_node)
graph.add_node("write_report", write_report_node)

graph.set_entry_point("plan")

graph.add_edge("plan", "search")
graph.add_edge("search", "write_report")
graph.add_edge("write_report", END)

app = graph.compile()

def run_agent(topic: str) -> str:
    result = app.invoke({
        "topic": topic,
        "plan": [],
        "search_results": [],
        "report": ""
    })
    return result["report"]


if __name__ == "__main__":
    while True:
        topic = input("\nEnter research topic (or 'bye' to quit): ")
        if topic.lower() == "bye":
            break
        result = run_agent(topic)
        print("\n" + "="*60)
        print(result)
        print("="*60)