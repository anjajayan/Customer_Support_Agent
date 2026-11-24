from langchain_openai import OpenAIEmbeddings

# from digital_pdfs.extract_pdf import extract_pdf
from embed_chunks import embed_all_chunks
from tables.chunking import build_order_customer_chunks_from_table
from tables.upload_to_db import upload_to_local_db
from query import support_query

from dotenv import load_dotenv

def main():
    load_dotenv()

    print("Hello from RAG Customer support agent!")

    # CONSTANTS
    embedding_model_name = "text-embedding-3-small"
    model_name = "gpt-5.6-luna"

    # pdf_path = "C:\\Users\\anjajayan\\Documents\\Customer Support agent\\digital_pdfs\\623410.pdf"

    print(f"Using embedding model: {embedding_model_name}")
    print(f"Using model: {model_name}")

    query = "Which refund is on hold until a technician reports on the drum noise?"
    support_query(query, model_name=model_name, 
                  embedding_model_name=embedding_model_name)


if __name__ == "__main__":
    main()
