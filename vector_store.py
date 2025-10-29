from utils import VectorDataBaseManager



vectordb_manager = VectorDataBaseManager()

vectordb_manager.build_vectordb()

for name in ["cf", "clt", "sumulas_trt3"]:
    vectordb_manager.update_vectordb(
        document_dir=f"data/docs/{name}",
        document_name=name
    )

