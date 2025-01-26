### Answer Grader

from pydantic import BaseModel,Field
from langchain_core.prompts import ChatPromptTemplate
from ragfile import aidata



# Data model
class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""

    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )




def answer_grader():
    # LLM

    model, embeddings = aidata()

    # LLM with function call
    structured_llm_grader = model.with_structured_output(GradeAnswer)

    # Prompt
    system = """You are a grader assessing whether an answer addresses / resolves a question \n 
         Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
        ]
    )

    answer_grader = answer_prompt | structured_llm_grader
    # answer_grader.invoke({"question": question, "generation": generation})
    return answer_grader


