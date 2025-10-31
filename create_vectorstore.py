from utils import VectorStoreManager, settings



vector_db = VectorStoreManager()
vector_db.add_documents_to_store(settings['vector_store']['documents_directory'])