from langgraph.graph import StateGraph, END
from agent.graph_nodes import AgentState, node_retrieve_context, node_analyze_risk, node_generate_tests
from flask import Flask, request, jsonify

def create_agent_graph():
    """Wires the nodes together into a directed LangGraph."""
    workflow = StateGraph(AgentState)

    workflow.add_node("retrieve_context", node_retrieve_context)
    workflow.add_node("analyze_risk", node_analyze_risk)
    workflow.add_node("generate_tests", node_generate_tests)

    workflow.set_entry_point("retrieve_context")
    workflow.add_edge("retrieve_context", "analyze_risk")
    workflow.add_edge("analyze_risk", "generate_tests")
    workflow.add_edge("generate_tests", END)

    return workflow.compile()

app = Flask(__name__)
agent_app = create_agent_graph()

@app.route("/generate", methods=["POST"])
def run_agent_endpoint():
    """HTTP endpoint to serve the agent."""
    data = request.json
    initial_state = {
        "recent_changes": data.get("recent_changes", "Unknown changes"),
        "retrieved_context": "",
        "risk_analysis": "",
        "generated_test_code": ""
    }
    
    final_state = agent_app.invoke(initial_state)
    
    return jsonify({
        "risk_analysis": final_state["risk_analysis"],
        "generated_test_code": final_state["generated_test_code"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)