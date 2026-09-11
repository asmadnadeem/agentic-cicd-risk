import os
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from agent.retrieval_store import retrieve_context

load_dotenv()

class AgentState(TypedDict):
    recent_changes: str
    retrieved_context: str
    risk_analysis: str
    generated_test_code: str

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.1,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def node_retrieve_context(state: AgentState) -> AgentState:
    """Node 1: Pulls relevant CI configs and error logs."""
    query = state["recent_changes"]
    context = retrieve_context(query)
    state["retrieved_context"] = context
    return state

def node_analyze_risk(state: AgentState) -> AgentState:
    """Node 2: Analyzes context for code risk areas."""
    prompt = f"""
    Analyze the following recent code changes alongside the CI config and error logs.
    Identify the specific modules that are at risk of regression.
    
    Recent Changes: {state['recent_changes']}
    Context: {state['retrieved_context']}
    
    Provide a concise risk analysis.
    """
    response = llm.invoke(prompt)
    state["risk_analysis"] = response.content
    return state

def node_generate_tests(state: AgentState) -> AgentState:
    """Node 3: Writes regression test cases."""
    prompt = f"""
    Based on the following risk analysis, generate a strict Python pytest regression test.
    
    Risk Analysis: {state['risk_analysis']}
    
    Output ONLY valid Python code starting with 'import pytest'.
    """
    response = llm.invoke(prompt)
    state["generated_test_code"] = response.content
    return state