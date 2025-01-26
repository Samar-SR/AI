from langchain_mongodb import MongoDBAtlasVectorSearch
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from ragfile.ai import aidata

load_dotenv(override=True)

load_dotenv()


def mongo_store():
    os.environ["USER_AGENT"] = os.environ.get("USER_AGENT", "MyApplication/1.0")

    model, embeddings = aidata()
    # insert the documents in MongoDB Atlas Vector Search
    MONGODB_ATLAS_CLUSTER_URI = os.environ["mogokey"]

    # initialize MongoDB python client
    client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

    DB_NAME = "self_rag"
    COLLECTION_NAME = "self_rag_vectorstores"
    ATLAS_VECTOR_SEARCH_INDEX_NAME = "self_rag_index-vectorstores"

    MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

    vector_store = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding=embeddings,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
        relevance_score_fn="cosine",
    )

    # vector_store.create_vector_search_index(dimensions=768)

    # doc_list = document_list()

    # vector_store.add_documents(documents=doc_list,)

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    return retriever, vector_store
