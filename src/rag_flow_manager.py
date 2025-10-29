# https://docs.langchain.com/oss/python/langchain/rag#expand-for-full-code-snippet

import os
import json

from google import genai
from google.genai import types
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

from utils import setup_logger, read_yaml_file
from src.prompts.system_prompt import SYSTEM_PROMPT



load_dotenv()
logger = setup_logger()
config = read_yaml_file("settings/config.yaml")


class RAGFlowManager:
    """A class that implements a Retrieval-Augmented Generation (RAG) to process user queries about brazilian labor legislation."""
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="data/db")
        self.model = config[0]["model"]
        self.temperature = config[0]["temperature"]
        self.response_type = config[0]["response_type"]
        self.max_tokens = config[0]["max_output_tokens"]
        self.google_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.google_embedding_model = GoogleGenerativeAiEmbeddingFunction(api_key=os.environ["GEMINI_API_KEY"])
        
    def __retrieve_documents(
        self, 
        query: str
    ) -> str:
        """Retrieves the most relevant context based on cosine similarity, for a given query.
        
        :param query: user query.
        :returns: retrieved context.
        """
        try:
            chroma_collection = self.chroma_client.get_collection(name="laws", embedding_function=self.google_embedding_model)
            retrieved_docs = chroma_collection.query(query_texts=[query])
            logger.info("CONTEXT RETRIEVED")
            return retrieved_docs
        except Exception as e:
            logger.error(f"ERROR RETRIEVING CONTEXT: {e}")

    def generate_response(
        self, 
        query: str
    ) -> str:
        """Process the user query with the retrieved context.

        :param query: user query.
        :returns: model response.
        """
        logger.info(f"QUERY: {query}")
        retrieved_docs = self.__retrieve_documents(query)
        logger.info(f"RETRIEVED CONTEXT: {retrieved_docs}")
        
        try:
            results = self.google_client.models.generate_content(
                contents=query,
                model=self.model,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens = self.max_tokens,
                    response_mime_type=self.response_type,
                    system_instruction=SYSTEM_PROMPT.format(context=retrieved_docs, query=query)
                )
            )
            response = json.loads(results.text)["resposta_final"]
            logger.info(f"MODEL RESPONSE: {response}")
            return response
        except Exception as e:
            logger.error(f"ERROR GENERATING RESPONSE: {e}")

