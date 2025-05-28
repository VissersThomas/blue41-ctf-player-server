import os
import shutil

from dotenv import load_dotenv
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails

from remote_vector_store import connect_to_remote_vector_db

def init_rag():
    """Initialize complete RAG pipeline with documents and return ready-to-use chain"""
    # Clear existing vector store to ensure fresh data
    store_dir = "store"
    if os.path.exists(store_dir):
        print(f"Clearing existing vector store: {store_dir}")
        shutil.rmtree(store_dir)

    print("Setting up connection to remote vector db...")
    vs = connect_to_remote_vector_db()
    retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    print("Setting up RAG chain...")
    # Create model and prompt
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    rag_prompt = hub.pull("rlm/rag-prompt")

    # Build RAG chain with proper LCEL patterns
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | rag_prompt
        | model
        | StrOutputParser()
        | RunnableParallel(answer=RunnablePassthrough())  # Wrap for guardrails compatibility
    )

    # Add guardrails - simple and clean
    config = RailsConfig.from_path("config")
    guardrails = RunnableRails(config, input_key="question", output_key="answer")

    chain_with_guardrails = guardrails | rag_chain

    print("RAG chain with input guardrails initialized")
    return chain_with_guardrails

