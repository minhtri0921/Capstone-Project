from langchain_core.documents import Document


def convert_list_context_source_to_str(contexts: list[Document]):
    formatted_str = ""
    for i, context in enumerate(contexts):
        formatted_str += f"Document index {i}:\nContent: {context.page_content}\n"
        formatted_str += "----------------------------------------------\n\n"
    return formatted_str
