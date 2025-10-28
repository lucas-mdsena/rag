import os

import pymupdf
import chromadb
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

from utils import setup_logger




logger = setup_logger()


class VectorDataBaseManager:
    def __init__(self):
        self.embedding_model = GoogleGenerativeAiEmbeddingFunction(api_key=os.environ["GEMINI_API_KEY"])
        self.chroma_client = chromadb.PersistentClient(path="data/db")

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
    
    def update_vectordb(
        self, 
        document_dir: str, 
        document_name: str
    ):
        # Document load ----------------------------------------------------------------------
        documents = self.load_documents(document_dir=document_dir)

        # Text splits ------------------------------------------------------------------------
        splitter = RecursiveCharacterTextSplitter(chunk_size = 3000, chunk_overlap = 100)
        text_splits = splitter.split_text(documents)
        ids = [f"{document_name} - {str(i)}" for i in range(len(text_splits))]

        # Gets existing collection and adds new embedded text splits -------------------------
        chroma_client = chromadb.PersistentClient(path="data/db")
        chroma_collection = chroma_client.get_collection(name="laws", embedding_function=self.embedding_model)
        chroma_collection.add(ids=ids, documents=text_splits)
        logger.info(f"VECTOR STORE UPDATED WITH: {document_name}")

    def build_vectordb(self):        
        # Creates new collection
        self.chroma_client.create_collection("laws", embedding_function=self.embedding_model)
        logger.info("VECTOR STORE CREATED")
    
    def check_id(self):
        # Futuro
        pass
