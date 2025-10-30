import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters.character import RecursiveCharacterTextSplitter

from utils.setup_logger import logger 
from utils.read_yaml_file import settings



load_dotenv()

class VectorStoreManager:
    """Class to manage the vector store for document embeddings."""
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings(
            model=settings['openai']['embedding_model'],
            api_key=os.environ["OPENAI_API_KEY"]
        )
        # Creates, if not exists, or loads existing vector store
        self.vector_store = Chroma(
            collection_name=settings['vector_store']['collection_name'],
            embedding_function=self.embedding_model,
            persist_directory=settings['vector_store']['persist_directory']
        )

    @staticmethod
    def __load_document(document_path: str) -> Document:
        """Loads a document from the specified directory.
        
        :param document_path: Path to the document to be loaded.
        :return: Loaded document as a Document object.
        """
        if not os.path.exists(document_path):
            raise FileNotFoundError(f'Document not found at: {document_path}.')
        
        loader = PyMuPDFLoader(file_path=document_path)
        loaded_doc = loader.load()
        logger.info(f'Loaded document with {len(loaded_doc)} pages from {document_path}.')
        return loaded_doc
    
    @staticmethod
    def __split_document(
        document: Document,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> list[Document]:
        """Splits a document into chunks for embedding."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )
        chunks = splitter.split_documents(document)
        logger.info(f'Document split into {len(chunks)} chunks.')
        return chunks

    def add_documents_to_store(self, document_dir: str) -> None:
        """Adds documents from the specified directory to the vector store."""
        # TODO: Add check for existing document IDs to avoid duplicates
        files = os.listdir(document_dir)
        for file in files:
            loaded_doc = self.__load_document(os.path.join(document_dir, file))
            chunks = self.__split_document(loaded_doc)
            self.vector_store.add_documents(chunks)

    def retrieve_chunks(self, query: str, k: int = 5) -> list[Document]:
        return self.vector_store.similarity_search(query, k=k)
