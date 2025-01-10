from langgraph.graph import StateGraph, START, END
from graph_function import (
    route_fn,
    transform_query_fn,
    retrieve_document_fn,
    grade_document_fn,
    gen_answer_normal_fn,
    grade_hallucinations_fn,
    generate_answer_rag_fn,
    State,
)

workflow = StateGraph(State)
workflow.add_node("routing", route_fn)
workflow.add_node("transform_query", transform_query_fn)
workflow.add_node("retrieve_document", retrieve_document_fn)
workflow.add_node("grade_document", grade_document_fn)
workflow.add_node("generate_answer_rag", generate_answer_rag_fn)
workflow.add_node("grade_hallucinations", grade_hallucinations_fn)
workflow.add_node("generate_answer_normal", gen_answer_normal_fn)

workflow.add_edge(START, "routing")


def routing_after_route(state: State):
    if state["route"] == "vectorstore":
        return "transform_query"
    else:
        return "generate_answer_normal"


workflow.add_conditional_edges(
    "routing",
    routing_after_route,
    {
        "transform_query": "transform_query",
        "generate_answer_normal": "generate_answer_normal",
    },
)
workflow.add_edge("transform_query", "retrieve_document")


def routing_after_retrieve_document(state: State):
    return "grade_document" if len(state["documents"]) != 0 else "generate_answer_normal"


workflow.add_conditional_edges(
    "retrieve_document",
    routing_after_retrieve_document,
    {
        "grade_document": "grade_document",
        "generate_answer_normal": "generate_answer_normal",
    },
)


def route_after_grade_document(state: State):
    return (
        "generate_answer_rag"
        if len(state["documents"]) != 0
        else "generate_answer_normal"
    )


workflow.add_conditional_edges(
    "grade_document",
    route_after_grade_document,
    {
        "generate_answer_rag": "generate_answer_rag",
        "generate_answer_normal": "generate_answer_normal",
    },
)
workflow.add_edge("generate_answer_rag", "grade_hallucinations")


def routing_check_pass_grade_hallucinations(state: State):
    return END if state["grade_response"] == "yes" else "generate_answer_normal"


workflow.add_conditional_edges(
    "grade_hallucinations",
    routing_check_pass_grade_hallucinations,
    {
        END: END,
        "generate_answer_normal": "generate_answer_normal",
    },
)
workflow.add_edge("generate_answer_normal", END)
app = workflow.compile()
