
### Hallucination Grader

from ragfile import aidata
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel,Field
from langchain_core.output_parsers.string import StrOutputParser


# Data model
class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


def Hallucination_Grader():
    # LLM

    model,embeddings = aidata()

    # LLM with function call

    structured_llm_grader = model.with_structured_output(GradeHallucinations)

    # Prompt
    system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
         Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""
    hallucination_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
        ]
    )

    hallucination_grader = hallucination_prompt | structured_llm_grader
    #hallucination_grader.invoke({"documents": docs, "generation": generation})
    return hallucination_grader

