from langchain_openai import OpenAIEmbeddings

from digital_pdfs.extract_pdf import extract_pdf
from embed_chunks import embed_all_chunks
from tables.chunking import build_order_customer_chunks_from_table
from tables.upload_to_db import upload_to_local_db

from dotenv import load_dotenv

def main():
    load_dotenv()

    print("Hello from RAG Customer support agent!")
    # CONSTANTS
    embedding_model_name = "text-embedding-3-small"
    pdf_path = "C:\\Users\\anjajayan\\OneDrive - Deloitte (O365D)\\Documents\\Project CSA - poc\\codebase\\digital_pdfs\\623410.pdf"

    print(f"Using embedding model: {embedding_model_name}")

    ### ---- Chunking/ embedding for corpus ----
    # Load tabular data into the local database
    upload_to_local_db()

    # Check on the table's tools that will be exposed to LLM
    # print(get_order("ORD-50001"))
    # print(get_customer_by_email("maria.gonzalez@example.com"))
    # print(list_orders("C1001", status="Delivered", since="2026-01-01"))
    # print(customer_order_summary("C1001"))

    # Create chunks for tabular data to be used in the RAG pipeline
    chunks_on_tables = build_order_customer_chunks_from_table()
    print(f"{len(chunks_on_tables)} chunks have been created from relational tables")

    # Create chunks from instruction manuals data
    extract_pdf()
    # Combine all chunks from different sources (currently only tables) into a single list
    # To be worked upon
    all_chunks = chunks_on_tables
    
    # # Embed the above chunks
    # vectorstore = embed_all_chunks(all_chunks, embedding_model_name)

    # # Test on the embedding
    # results = vectorstore.similarity_search("Which customer's washer leaks near the door during the spin cycle and got a full refund?", k=5)
    # print(f"Top 5 results for the query"\
    #       f"'Which customer's washer leaks near the door during the spin cycle and got a full refund?': {results}")








if __name__ == "__main__":
    main()
