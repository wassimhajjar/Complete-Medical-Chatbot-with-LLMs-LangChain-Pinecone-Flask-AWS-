from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain_classic.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.db_methods import save_message


#Extract data from pdf files
def load_pdf_files(data):
    loader=DirectoryLoader(data,glob="*.pdf",loader_cls=PyPDFLoader)
    documents=loader.load()
    print("documents loaded")
    return documents

#filter pdf to get only the important information
def filter_to_minimal_docs(docs: List[Document])->List[Document]:
    """
    Given a list of document objects, return a new list of Document objects containing only 'source' in metadata and the original page_content.
    """
    minimal_docs:List[Document]=[]
    for doc in docs:
        src=doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source":src}
            )
        )

    print("Documents filtered")
    return minimal_docs

#Split the documents into smaller chunks
def text_split(minimal_docs):
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
        length_function=len
    )
    texts_chunk=text_splitter.split_documents(minimal_docs)
    print("texts splitted")
    return texts_chunk

#Download the embeddings from HuggingFace
def download_hugging_face_embeddings():
    """
    Download and return the HuggingFace embeddings model
    """
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    embeddings= HuggingFaceEmbeddings(
        model_name=model_name
    )
    print("Embedding model loaded")
    return embeddings

def invoke_and_save(session_id, input_text,conversational_rag_chain):
    # Save the user question with role "human"
    save_message(session_id, "human", input_text)
    
    result = conversational_rag_chain.invoke(
        {"input": input_text},
        config={"configurable": {"session_id": session_id}}
    )["answer"]

    # Save the AI answer with role "ai"
    save_message(session_id, "ai", result)
    return result


