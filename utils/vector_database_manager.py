import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters.character import RecursiveCharacterTextSplitter

from utils.setup_logger import logger 
from utils.read_yaml_file import read_yaml_file


load_dotenv()
settings = read_yaml_file("settings/config.yaml")

class VectorDataBaseManager:
    """Class to manage the vector database for document embeddings."""
    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model=settings['google_embeddings']['model'],
            google_api_key=os.environ["GEMINI_API_KEY"]
        )
        self.chroma_client = Chroma(
            collection_name=settings['vector_store']['collection_name'],
            embedding_function=self.embedding_model,
            persist_directory=settings['vector_store']['persist_directory']
        )

    def load_documents(
        self, 
        document_dir
    ):
        documents = []
        document_path = Path(document_dir)
        files = [file for file in document_path.glob("*") if file.is_file() and file.suffix == ".pdf"] # Lists all documents in the path

        for file in files:
            with pymupdf.open(file) as source_document:
                for page in source_document:
                    documents.append(page.get_text())    
        documents = ''.join(documents)
        documents = documents.lower()

        return documents
    
    # def update_vectordb(
    #     self, 
    #     document_dir: str, 
    #     document_name: str
    # ):
    #     # Document load ----------------------------------------------------------------------
    #     documents = self.load_documents(document_dir=document_dir)

    #     # Text splits ------------------------------------------------------------------------
    #     splitter = RecursiveCharacterTextSplitter(chunk_size = 3000, chunk_overlap = 100)
    #     text_splits = splitter.split_text(documents)
    #     ids = [f"{document_name} - {str(i)}" for i in range(len(text_splits))]

    #     # Gets existing collection and adds new embedded text splits -------------------------
    #     chroma_client = chromadb.PersistentClient(path="data/db")
    #     chroma_collection = chroma_client.get_collection(name="laws", embedding_function=self.embedding_model)
    #     chroma_collection.add(ids=ids, documents=text_splits)
    #     logger.info(f"VECTOR STORE UPDATED WITH: {document_name}")

    # def build_vectordb(self):        
    #     # Creates new collection
    #     self.chroma_client.create_collection("laws", embedding_function=self.embedding_model)
    #     logger.info("Vector database built successfully.")
    
    # def check_id(self):
    #     # Futuro
    #     pass
