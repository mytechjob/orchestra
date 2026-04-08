"""
News & Research Agent — Streamlit Web Interface
================================================
Run: streamlit run web_app.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Add parent directory to path to import agent module
sys.path.insert(0, os.path.dirname(__file__))
from agent import run_agent, build_graph

load_dotenv()

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="News & Research Agent",
    page_icon="🗞️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CSS Styling
# ──────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .query-box {
        font-size: 1.1rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        padding: 0.75rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    .response-box {
        padding: 1.5rem;
        background-color: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .example-chip {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        background-color: #e8eaf6;
        border-radius: 20px;
        cursor: pointer;
        font-size: 0.9rem;
    }
    .example-chip:hover {
        background-color: #c5cae9;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────
def check_env():
    """Validate required API keys are set."""
    missing = []
    for key in ["OPENAI_API_KEY", "TAVILY_API_KEY"]:
        if not os.environ.get(key):
            missing.append(key)
    return missing


def load_graph_image():
    """Load the agent graph visualization image."""
    graph_path = Path(__file__).parent / "agent_graph.png"
    if graph_path.exists():
        return graph_path
    return None


def run_agent_with_tracking(query):
    """
    Run agent with Streamlit progress tracking.
    Uses Streamlit's status indicators for node execution feedback.
    """
    import os
    from datetime import datetime
    from agent import build_graph, AgentState
    
    agent = build_graph()
    
    initial_state: AgentState = {
        "query": query,
        "intent": None,
        "entity": None,
        "format_pref": None,
        "search_queries": [],
        "raw_results": [],
        "ranked_results": [],
        "research_summary": None,
        "final_response": None,
        "error": None,
        "messages": [],
    }
    
    # Track execution steps
    execution_steps = []
    
    # Custom callback to track progress (using Streamlit session state)
    # Note: LangGraph doesn't have built-in streaming callbacks in all versions,
    # so we'll use the verbose mode capture
    
    result = agent.invoke(initial_state)
    response = result.get("final_response") or result.get("error") or "No response generated."
    
    # Extract execution metadata from result state
    intent = result.get("intent", "unknown")
    entity = result.get("entity", None)
    format_pref = result.get("format_pref", "prose")
    num_articles = len(result.get("raw_results", []))
    num_ranked = len(result.get("ranked_results", []))
    
    execution_metadata = {
        "intent": intent,
        "entity": entity,
        "format_pref": format_pref,
        "articles_found": num_articles,
        "articles_ranked": num_ranked,
        "search_queries": result.get("search_queries", [])
    }
    
    return response, execution_metadata


# ──────────────────────────────────────────────
# Main UI
# ──────────────────────────────────────────────
def main():
    # Header
    st.markdown('<div class="main-header">🗞️ News & Research Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-powered news analysis and research assistant</div>', unsafe_allow_html=True)
    
    # Check environment
    missing_keys = check_env()
    if missing_keys:
        st.error(f"❌ Missing API keys: {', '.join(missing_keys)}")
        st.warning("Please set these environment variables in your `.env` file or system environment.")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Example queries
        st.markdown("### 📝 Example Queries")
        example_queries = [
            "Check recent news and let me know which is most important",
            "Check latest news and return in table format",
            "What's happening in the world",
            "What is happening with Donald Trump",
            "Who is Donald Trump",
        ]
        
        selected_example = st.selectbox(
            "Choose an example query:",
            example_queries,
            index=0
        )
        
        if st.button("Use Example Query"):
            st.session_state.example_query = selected_example
        
        st.divider()
        
        # Agent diagram toggle
        show_diagram = st.toggle("📊 Show Agent Architecture", value=True)
        
        if show_diagram:
            st.divider()
            st.markdown("### 🤖 Agent Architecture")
            
            graph_image = load_graph_image()
            if graph_image:
                st.image(
                    str(graph_image),
                    caption="LangGraph Agent Flow",
                    use_container_width=True
                )
            else:
                st.warning("Graph image not found. Run `python agent.py` to generate it.")
            
            # Text description of agent flow
            with st.expander("📖 How It Works"):
                st.markdown("""
                **Agent Workflow:**
                
                1. **Classify Intent** - Analyzes query to determine:
                   - Intent: news, research, or overview
                   - Entity: person/topic mentioned
                   - Format preference: table, list, or prose
                   
                2. **Fetch News** (for news/overview) - Searches Tavily API for relevant articles
                
                3. **Research Entity** (for research) - Deep background research on entity
                
                4. **Rank Importance** - AI scores articles by global importance (1-10)
                
                5. **Format Output** - Generates response in requested format
                
                **Routing Logic:**
                - Research queries → research_entity → format_output
                - News/Overview → fetch_news → rank_importance → format_output
                """)
        
        st.divider()
        
        # About section
        with st.expander("ℹ️ About"):
            st.markdown("""
            Built with:
            - **LangGraph** for stateful agent
            - **OpenAI GPT-4o** for intelligence
            - **Tavily API** for news search
            - **Streamlit** for web interface
            """)
    
    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Query input
        default_query = st.session_state.get("example_query", "")
        user_query = st.text_area(
            "Enter your query:",
            value=default_query,
            placeholder="e.g., What's the latest news about AI?",
            height=100,
            key="query_input"
        )
        
        # Run button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            run_button = st.button("🔍 Analyze", type="primary")
    
    # Process query
    if run_button and user_query.strip():
        with st.spinner("🤖 Agent is analyzing your query..."):
            try:
                response, metadata = run_agent_with_tracking(user_query)
                
                # Display execution metadata
                st.markdown("### 📊 Analysis Details")
                meta_cols = st.columns(4)
                with meta_cols[0]:
                    st.metric("Intent", metadata["intent"].title())
                with meta_cols[1]:
                    st.metric("Entity", metadata["entity"] or "General")
                with meta_cols[2]:
                    st.metric("Articles Found", metadata["articles_found"])
                with meta_cols[3]:
                    st.metric("Format", metadata["format_pref"].title())
                
                # Display search queries used
                if metadata["search_queries"]:
                    with st.expander("🔎 Search Queries Used", expanded=False):
                        for i, sq in enumerate(metadata["search_queries"], 1):
                            st.text(f"{i}. {sq}")
                
                # Display response
                st.markdown("---")
                st.markdown("### 📄 Response")
                st.markdown(response)
                
                # Success notification
                st.success("✅ Query processed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error processing query: {str(e)}")
                st.exception(e)
    
    elif run_button and not user_query.strip():
        st.warning("⚠️ Please enter a query first.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888; font-size: 0.9rem;'>"
        "Powered by LangGraph · OpenAI · Tavily · Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
