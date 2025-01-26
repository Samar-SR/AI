### Generate

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from ragfile import aidata


def Generate():
    # LLM

    model,embeddings = aidata()

    # Prompt
    prompt = hub.pull("rlm/rag-prompt")

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Chain
    rag_chain = prompt | model | StrOutputParser()

    # Run
    #generation = rag_chain.invoke({"context": docs, "question": question})
    return rag_chain

