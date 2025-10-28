import traceback

import uvicorn
from fastapi import FastAPI, HTTPException

from src import RAGFlowManager
from utils import setup_logger



app = FastAPI()
logger = setup_logger()
rag_manager = RAGFlowManager()

@app.post("/rag")
def rag_flow(data: QueryRequest):
    try:
        response = rag_manager.generate_response(query=data.text)
        return {"response": response}
    except Exception as e:
        error = traceback.format_exc()
        logger.error(f"ERROR PROCESSING REQUEST: {error}.")
        raise HTTPException(status_code=400, detail=f"Error processing request: {str(e)}.")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)