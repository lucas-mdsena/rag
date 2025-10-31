import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser

from utils import logger, settings, VectorStoreManager
from src.prompts.system_prompt import SYSTEM_PROMPT



load_dotenv()

class RAGManager:
    """A class that implements a Retrieval-Augmented Generation (RAG) to process user queries about 
    brazilian labor legislation and federal constitution.
    """
    def __init__(self):
        self.vector_store = VectorStoreManager()
        self.parser = JsonOutputParser()
        self.llm = ChatOpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            model=settings['openai']['llm_model'],
            temperature=settings['openai']['temperature'],
            max_tokens=settings['openai']['max_output_tokens'],
        )
    
    def retrieve_and_generate(self, query: str) -> str:
        """Process the user query with the retrieved context.

        :param query: user query.
        :returns: model response.
        """
        logger.info(f'User query: "{query}"')

        retrieved_docs = self.vector_store.retrieve(query)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        prompt = PromptTemplate(
            template=SYSTEM_PROMPT,
            input_variables=["query"],
            partial_variables={"context": context}
        )

        chain = prompt | self.llm | self.parser
        response = chain.invoke({"query": query})
        logger.info(f"LLM response: {response['resposta_final']}")
        return response['resposta_final']

