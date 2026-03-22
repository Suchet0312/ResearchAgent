# 🔍 Research Agent

An autonomous research agent that plans, searches, and writes structured reports — built three ways to demonstrate progressive understanding of agentic AI systems.

## 🎯 What it does

Give it any topic and it will:
1. **Plan** — break the topic into targeted search queries
2. **Search** — fetch real results from Google
3. **Read** — extract content from relevant pages
4. **Write** — produce a structured report with sources

## 🏗️ Three implementations

| File | Approach | What you learn |
|------|----------|----------------|
| `agent.py` | Raw Python | Agent loop fundamentals — while loop, tool calling, message history |
| `agent_langchain.py` | LangChain | Abstractions — create_react_agent, @tool decorator, ChatOllama |
| `agent_langgraph.py` | LangGraph | Graph-based agents — nodes, edges, state management |

## 🛠️ Tech Stack

- **LangGraph** — graph-based agent orchestration
- **LangChain** — agent abstractions and tool definitions
- **Ollama + Mistral** — local LLM, runs entirely on your machine
- **Streamlit** — web UI
- **googlesearch-python** — free Google search, no API key needed
- **BeautifulSoup** — webpage content extraction

## 📁 Project Structure
```
research-agent/
├── tools.py              # web_search + fetch_page tools
├── agent.py              # raw Python agent loop
├── agent_langchain.py    # LangChain implementation
├── agent_langgraph.py    # LangGraph implementation
├── app.py                # Streamlit web UI
├── .env                  # API keys (not committed)
└── requirements.txt      # dependencies
```

## ⚡ Quick Start

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/research-agent
cd research-agent
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Install and start Ollama**

Download from https://ollama.com and run:
```bash
ollama pull mistral
ollama serve
```

**5. Run the app**
```bash
streamlit run app.py
```

## 📦 Requirements

Create a `requirements.txt` file with:
```
langchain
langchain-community
langchain-ollama
langgraph
streamlit
requests
beautifulsoup4
googlesearch-python
python-dotenv
```

## 🧠 Architecture
```
[START]
   ↓
[Plan Node]    → breaks topic into 3 targeted search queries
   ↓
[Search Node]  → executes searches, fetches page content
   ↓
[Report Node]  → synthesizes findings into structured report
   ↓
[END]
```

Each node reads from and writes to a shared `AgentState`:
```python
class AgentState(TypedDict):
    topic: str           # original research topic
    plan: list[str]      # search queries from plan node
    search_results: list # fetched content from search node
    report: str          # final report from report node
```

## 💡 Key Concepts Demonstrated

**Tool Calling** — the model requests tools, your code executes them and feeds results back

**Agent Loop** — think → act → observe → think again, until the agent decides it has enough information

**LangGraph State** — a typed dictionary that flows between nodes, each node reads what it needs and writes what it produces

**ReAct Pattern** — Reason + Act, the agent reasons about what to do next before acting

## 🔄 Comparing the three approaches

**Raw Python (`agent.py`)**
```python
while True:
    response = call_ollama(messages)
    if not tool_calls:
        return text_response      # done
    # run tools, add results, loop again
```

**LangChain (`agent_langchain.py`)**
```python
agent = create_react_agent(llm, tools)
result = agent.invoke({"messages": messages})
```

**LangGraph (`agent_langgraph.py`)**
```python
graph = StateGraph(AgentState)
graph.add_node("plan", plan_node)
graph.add_node("search", search_node)
graph.add_node("write_report", write_report_node)
graph.add_edge("plan", "search")
graph.add_edge("search", "write_report")
graph.add_edge("write_report", END)
app = graph.compile()
```

## 🚀 Future improvements

- [ ] Deploy on Streamlit Cloud
- [ ] Add research history
- [ ] Export reports to PDF
- [ ] Swap Mistral for a stronger model
- [ ] Add source credibility scoring
- [ ] Multi-agent version with CrewAI

## 👨‍💻 Author

Built as a learning project to understand agentic AI systems from the ground up — raw fundamentals first, frameworks second.