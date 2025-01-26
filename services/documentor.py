from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from ragfile.mongo import mongo_store
from langchain.schema import Document


def document_list(data, url):
    if url is True:
        urls = [data]
        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]
        content = [doc.page_content for doc in docs_list]

    else:
        content = [data]

    content = [
        doc.decode("utf-8") if isinstance(doc, bytes) else doc
        for doc in content
    ]

    for doc in content:
        doc = "".join(doc.split("\n"))

    content = [
        doc.decode("utf-8") if isinstance(doc, bytes) else doc
        for doc in content
    ]

    document = [Document(page_content=doc) for doc in content]

    text_splitter = RecursiveCharacterTextSplitter(
        separators=['.', '/n'],
        chunk_size=600,
        chunk_overlap=100
    )

    doc_list = text_splitter.split_documents(document)

    retriever, vector_store = mongo_store()

    vector_store.add_documents(documents=doc_list)

    return True
