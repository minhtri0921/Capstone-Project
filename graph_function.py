from dotenv import load_dotenv
load_dotenv()
from prompt import (
    RouteQuery,
    GradeDocuments,
    GenerateAnswer,
    GradeHallucinations,
    ExtractFilter,
    route_chain,
    transform_query_chain,
    grade_documents_chain,
    gen_normal_answer_chain,
    gen_answer_rag_chain,
    grade_hallucinations_chain,
    extract_filter_chain,
)
from config.database import vector_store
from langchain_core.documents import Document
from prompt import GradeDocuments
from helper import convert_list_context_source_to_str
from logger import logger
from langgraph.graph.message import AnyMessage, add_messages
from typing import TypedDict, Literal



class State(TypedDict):
    user_query: AnyMessage
    route: str
    messages_history: list
    documents: list[Document]
    filter: dict
    llm_response: AnyMessage
    grade_response: Literal["yes", "no"]
    language: str
    document_id_selected: str


def route_fn(state: State):
    question = state["user_query"].content
    route_response: RouteQuery = route_chain.invoke({"question": question})
    logger.info(f"Route response: {route_response}")
    return {"route": route_response.datasource}


def transform_query_fn(state: State):
    question = state["user_query"].content
    chat_history = state["messages_history"]
    transform_response = transform_query_chain.invoke(
        {"question": question, "chat_history": chat_history}
    )
    logger.info(f"Transform response: {transform_response}")
    return {"user_query": transform_response}


def retrieve_document_fn(state: State):
    question = state["user_query"].content
    history = state["messages_history"]
    filter = state.get("filter", None)

    if not filter:
        filter_response: ExtractFilter = extract_filter_chain.invoke(
            {"question": question, "history": history}
        )
        logger.info(f"Extract filter response: {filter_response}")
        job_title = filter_response.job_title
        job_level = filter_response.job_level
        filter = {}

        if job_title:
            filter["title"] = job_title
        if job_level:
            filter["level"] = job_level

    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 5, "score_threshold": 0.0},
    )

    documents = retriever.invoke(question, filter=filter)
    logger.info(f"Retrieved documents: {documents}")

   
    for doc in documents:
        doc_id = doc.metadata.get("id", "No ID found")  
        logger.info(f"Document ID: {doc_id}")


    return {"documents": documents}



def grade_document_fn(state: State):
    question = state["user_query"].content
    documents = state["documents"]
    inputs_bach = [
        {"question": question, "document": doc.page_content} for doc in documents
    ]
    grade_document_response: list[GradeDocuments] = grade_documents_chain.batch(inputs_bach)
    logger.info(f"Grade document response: {grade_document_response}")
    document_index = [
        index for index, doc in enumerate(grade_document_response) if doc.binary_score == "yes"
    ]
    filtered_documents = [documents[i] for i in document_index]

    return {"documents": filtered_documents}


def generate_answer_rag_fn(state: State):
    question = state["user_query"].content
    documents = state["documents"]
    language = state["language"]
    if documents:
        context_str = convert_list_context_source_to_str(documents)
        
    gen_answer_response: GenerateAnswer = gen_answer_rag_chain.invoke(
        {"question": question, "context": context_str, "language": language}
    )
    logger.info(f"Generate answer response: {gen_answer_response}")
    id_selected = None
    if gen_answer_response.selected_document_index is not None:
        id_selected = documents[gen_answer_response.selected_document_index].metadata[
            "id"
        ]
    logger.info(f"Document id selected: {id_selected}")
    return {
        "llm_response": gen_answer_response.answer,
        "document_id_selected": id_selected,
    }


def grade_hallucinations_fn(state: State):
    question = state["user_query"].content
    llm_response = state["llm_response"]
    grade_response: GradeHallucinations = grade_hallucinations_chain.invoke(
        {"question": question, "generation": llm_response}
    )
    logger.info(f"Grade hallucinations response: {grade_response}")
    return {"grade_response": grade_response.binary_score}
    # return {"grade_response": "yes"}


def gen_answer_normal_fn(state: State):
    question = state["user_query"].content
    history = state["messages_history"]
    gen_answer_response = gen_normal_answer_chain.invoke(
        {"question": question, "history": history}
    )
    logger.info(f"Generate answer response: {gen_answer_response}")
    return {"llm_response": gen_answer_response.content}
