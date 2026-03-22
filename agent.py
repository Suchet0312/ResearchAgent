import requests
import json
from tools import web_search, fetch_page

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information on a topic. Use this first to find relevant URLs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_page",
            "description": "Read the full content of a webpage. Use this after web_search to get details from a URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The full URL to fetch"
                    }
                },
                "required": ["url"]
            }
        }
    }
]

def call_ollama(messages):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "messages": messages,
        "tools": tools_definition,
        "stream": False
    })
    return response.json()

def run_agent(topic: str) -> str:
    print(f"\n🤖 Starting research on: {topic}\n")

    messages = [
        {
            "role": "user",
            "content": f"""Research this topic thoroughly and write a clear report: {topic}

Use web_search to find sources, then fetch_page to read them in detail.
When you have enough information write a structured report with:
- Key findings
- Important details
- Your sources (URLs)"""
        }
    ]

    while True:
        print("🤔 Thinking...")
        response = call_ollama(messages)

        message = response["message"]
        tool_calls = message.get("tool_calls", [])
        text_response = message.get("content", "")

        if not tool_calls:
            print("\n✅ Research complete!")
            return text_response

        messages.append(message)

        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            tool_input = tool_call["function"]["arguments"]

            if isinstance(tool_input, str):
                tool_input = json.loads(tool_input)

            print(f"🔧 Using tool: {tool_name} with input: {tool_input}")

            if tool_name == "web_search":
                result = web_search(tool_input["query"])
                result_str = json.dumps(result)
            elif tool_name == "fetch_page":
                result_str = fetch_page(tool_input["url"])
            else:
                result_str = f"Unknown tool: {tool_name}"

            print(f"   → Got result: {result_str[:100]}...")

            messages.append({
                "role": "tool",
                "content": result_str
            })

if __name__ == "__main__":
    result = run_agent("latest developments in artificial intelligence")
    print(result)