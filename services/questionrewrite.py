
### Question Re-writer
from ragfile import aidata
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser


def Re_writer():
    # LLM

    model,embeddings = aidata()

    # Prompt
    system = """You a question re-writer that converts an input question to a better version that is optimized \n 
         for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                "Here is the initial question: \n\n {question} \n Formulate an improved question.",
            ),
        ]
    )

    question_rewriter = re_write_prompt | model | StrOutputParser()
    #question_rewriter.invoke({"question": question})
    return question_rewriter

