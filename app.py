import streamlit as st
from agent_langgraph import run_agent, app as langgraph_app
import json

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Research Agent")
st.caption("Powered by Mistral + LangGraph")

topic = st.text_input("Enter your research topic", placeholder="e.g. latest developments in AI agents...")

if st.button("Research", type="primary"):
    if not topic:
        st.warning("Please enter a topic first")
    else:
        with st.status("Agent is working...", expanded=True) as status:
            
            st.write("📋 Planning search queries...")
            
            progress_placeholder = st.empty()
            report_placeholder = st.empty()
            
            try:
                initial_state = {
                    "topic": topic,
                    "plan": [],
                    "search_results": [],
                    "report": ""
                }
                
                for step in langgraph_app.stream(initial_state):
                    node_name = list(step.keys())[0]
                    node_output = step[node_name]
                    
                    if node_name == "plan":
                        queries = node_output.get("plan", [])
                        st.write(f"✅ Plan ready — {len(queries)} queries:")
                        for q in queries:
                            st.write(f"   → {q}")
                    
                    elif node_name == "search":
                        results = node_output.get("search_results", [])
                        st.write(f"✅ Search done — read {len(results)} sources")
                    
                    elif node_name == "write_report":
                        st.write("✅ Report written!")
                        report = node_output.get("report", "")
                
                status.update(label="Research complete!", state="complete")
                
                st.subheader("📄 Research Report")
                st.markdown(report)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download Report",
                        data=report,
                        file_name=f"{topic[:30]}_report.txt",
                        mime="text/plain"
                    )
                with col2:
                    st.code(report, language=None)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                status.update(label="Error", state="error")