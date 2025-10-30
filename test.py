from utils import VectorStoreManager
vector_db = VectorStoreManager()
vector_db.add_documents_to_store('data/docs/all')