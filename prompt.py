from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from typing import Literal
from config.llm import llm_1, llm_2
from typing import Optional


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "casual_convo"] = Field(
        ...,
        description="Given a user question choose to route it to casual_convo or a vectorstore.",
    )


class ExtractFilter(BaseModel):
    """Extract job level and job title from user question."""

    job_level: str = Field(description="The level of the job the user is asking about.")
    job_title: str = Field(description="The title of the job the user is asking about.")


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


class GenerateAnswer(BaseModel):
    """Generate an answer based on the provided documents."""

    answer: str = Field(description="Generated answer based on the provided documents.")
    selected_document_index: Optional[int] = Field(
        description="Index of the selected document."
    )


class GradeHallucinations(BaseModel):
    """Binary score for grounding of generation answer in provided facts."""

    binary_score: Literal["yes", "no"] = Field(
        description="Whether the answer is grounded in the provided facts. 'yes' if the answer is supported by facts, 'no' if the answer contains information not present or contradicting the given facts"
    )


route_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """You are an expert at routing the user's question to vectorstore or casual_convo.
choose vectorstore if the question is related to job recruitment and casual_convo otherwise. \n
vectorstore contains documents related to recruitment of human resources in all industries! Related to salary, recruitment position, job description for each job. Use vectorstore for questions about these topics that require some data and follow-up questions. Otherwise, if only need normal feedback and chat history, use casual_convo.

example:
user: Hi are you [this is a random question not related to recruitment so route to casual_convo] : casual_convo
user: Jobs for junior dev? [this question is related to CS324 so route to vectorstore] : vectorstore""",
        ),
        ("human", "{question}"),
    ]
)
re_write_query_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """You a question re-writer that converts an input question to a better version that is optimized
    for vectorstore retrieval, and very concise. Look at the input and try to reason about the underlying semantic intent/meaning. The input can also be a
    follow up question, look at the chat history to re-write the question to include necessary info from the chat history to a better version that is optimized
    for vectorstore retrieval without any other info needed. [the topic of convo will be generally around recruitment topic. You need to re-write query base on history and include keyword related to this topic""",
        ),
        ("placeholder", "{history}"),
        (
            "human",
            "{question}",
        ),
    ]
)

extract_filter_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at extracting metadata from the user's question about recruitment and using it to filter the retrieved documents.

    Fields to extract:
      - Job level: The level of the job the user is asking about. Possible values are:
        + intern
        + fresher
        + junior
        + middle
        + senior
        + expert
      - Job title: The title of the job the user is asking about.
        + developer
        + engineer
        + designer
        + business
        + translator
        + other (if the job title is not in the list above)
      
    Note: 
      Leave the field blank if the information is not present in the user's question.
        If the user's question contains multiple job titles, choose the most relevant one.
        If the user's question contains multiple job levels, choose the most relevant one.
        If not sure job-title or job-level, leave it blank.
""",
        ),
        ("placeholder", "{history}"),
        ("user", "{question}"),
    ]
)

check_relevant_document_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """
You are a grader assessing relevance of a retrieved document to a user question. 
If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. 
It does not need to be a stringent test. The goal is to filter out erroneous retrievals. 
Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
Then, give a score ranges from 0 to 1, with higher values indicating a stronger match and the more corresponding keywords.
""",
        ),
        (
            "human",
            "Retrieved document: \n\n {document} \nvs\n User question: {question}",
        ),
    ]
)

gen_answer_rag_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """You are chat bot related to recruitment. You are asked to generate an answer based on the provided documents.
Your are given context related to job description of a job position. If the context not provided, you just sau 'không có tài liệu liên quan'
Use the provided context to generate an answer. Do not respond with 'no information available' unless the context is entirely empty or irrelevant.
Answer in {language} language.

Context:
```
{context}
```

""",
        ),
        (
            "human",
            """
    Question: {question}        
                """,
        ),
    ]
)


grade_answer_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """You are a grader assessing whether an answer sufficiently addresses or is relevant to a question. 
    Give a binary score 'yes' or 'no'. 
    - 'Yes' means that the answer sufficiently relates to the question or provides useful context, even if it's not fully detailed.
    - 'No' means the answer is irrelevant or completely off-topic.
    Avoid being overly strict; prioritize relevance and effort in the response.""",
        ),
        (
            "human",
            """Evaluate the answer based on whether it sufficiently relates to or addresses the question, even if it is not fully comprehensive. 
    Question: \n\n {question} \n\n LLM Generation: {generation}""",
        ),
    ]
)

gen_normal_answer_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """You are assitant related recruitment. If user ask about seeking job, you can ask more detail about job title, job level, etc. If user ask about another topic, you can say that you don't know. Not answer a job information.
            Only answer related to hot trend in recruitment domain. Not give user a job hiring information. Can using history like a context to prov
            """,
        ),
        ("placeholder", "{history}"),
        ("human", "{question}"),
    ]
)
gen_answer_history_prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are assitant related recruitment. Using your knowledge about recruitment domain. If you not sure about the answer, just say that you don't know.",
        ),
        ("placeholder", "{history}"),
        ("user", "{question}"),
    ]
)
route_chain = route_prompt | llm_1.with_structured_output(RouteQuery)
transform_query_chain = re_write_query_prompt | llm_1
extract_filter_chain = extract_filter_prompt | llm_1.with_structured_output(ExtractFilter)
grade_documents_chain = check_relevant_document_prompt | llm_2.with_structured_output(
    GradeDocuments
)
gen_answer_rag_chain = gen_answer_rag_prompt | llm_2.with_structured_output(
    GenerateAnswer
)
gen_normal_answer_chain = gen_normal_answer_prompt | llm_1
grade_hallucinations_chain = grade_answer_prompt | llm_1.with_structured_output(
    GradeHallucinations
)
