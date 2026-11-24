from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import uuid

def embed_all_chunks(chunks, embedding_model_name = "text-embedding-3-small"):
    embeddings = OpenAIEmbeddings(model=embedding_model_name) 
     # reads OPENAI_API_KEY from env

    docs = [
        Document(page_content=c["text"],
                 metadata={k: v for k, v in c.items() if k != "text"})
        for c in chunks
    ]
    # ids are needed for ease of re-ingestion where in this list is used by the 
    # vectorstore creation. Each chunk gets a unique ID to for storage, updation and deletion of 
    # a particular chunk.
    ids = [str(uuid.uuid4()) for _ in chunks]

    vectorstore = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory="./chroma_db",
        ids=ids,
    )

    return vectorstore