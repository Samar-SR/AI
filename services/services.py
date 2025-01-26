
from langgraph.graph import END, StateGraph, START
from .methoddirectory import GraphState, retrieve, grade_documents, generate, transform_query, \
    decide_to_generate, grade_generation_v_documents_and_question


def result(inputs):

    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("retrieve", retrieve)  # retrieve
    workflow.add_node("grade_documents", grade_documents)  # grade documents
    workflow.add_node("generate", generate)  # generatae
    workflow.add_node("transform_query", transform_query)  # transform_query

    # Build graph
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        },
    )
    workflow.add_edge("transform_query", "retrieve")
    workflow.add_conditional_edges(
        "generate",
        grade_generation_v_documents_and_question,
        {
            "not supported": "generate",
            "useful": END,
            "not useful": "transform_query",
        },
    )

    # Compile
    app = workflow.compile()
    count = 0
    for output in app.stream(inputs):
        for key, value in output.items():
            # Node
            print(f"Node '{key}':")
            print(f"value  {value}")
            if key == "generate":
                count = count + 1
            if count == 3:
                break
            # Optional: print full state at each node
            #print(value["keys"], indent=2, width=80, depth=None)
        print("\n---\n")
        if count == 3:
            break

    # Final generation
    #print(value["generation"])

    values = "this is result"

    return values





