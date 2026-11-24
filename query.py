
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def support_query(raw_query,
                   model_name="gpt-4o-mini", embedding_model_name="text-embedding-3-small"):
    print("Running support Agent...")

    # 1. (same embedding model used at ingestion)
    embeddings = OpenAIEmbeddings(model=embedding_model_name)
    vectorstore = Chroma(
        persist_directory="./chroma_db",       # whatever path you used at ingestion
        embedding_function=embeddings,
    )

    # 2. Turn it into a retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    # Get and format the context 
    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)
    context = format_docs(retriever.invoke(raw_query))

    # 3. Prompt
    prompt = """
    Answer the question using only the context below.
    If the answer isn't in the context, say you don't know.

    Context:
    {context}

    Question: {raw_query}
    """

    prompt = PromptTemplate(
        template = prompt,
        input_variables = ['raw_query', 'context']
    )
    input_var = {'raw_query': raw_query, 'context': context}


    # 4. LLM
    llm = ChatOpenAI(model=model_name, temperature=0)

    # 5. Chain it together (LCEL)
    rag_chain = ( prompt
        | llm
        | StrOutputParser()
    )
    print(f"User: {raw_query}")
    response = rag_chain.invoke(input_var)
    print(f"Agent: {response}")