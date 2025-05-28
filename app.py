import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from rag_chain import init_rag

# Load environment variables
load_dotenv()

# Initialize RAG chain once at startup
chain = init_rag()

# Create FastAPI app
app = FastAPI(title="RAG Chat Web App", version="1.0.0")

# Serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models for API
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str

# Serve the main HTML page
@app.get("/")
async def serve_chat():
    return FileResponse("static/index.html")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "rag_ready": chain is not None}

# Main chat endpoint
@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    try:
        response = await chain.ainvoke(request.question)
        return QuestionResponse(answer=response["answer"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting RAG Chat Web App...")
    print("📱 Open your browser to: http://localhost:8999")
    uvicorn.run(app, host="0.0.0.0", port=8999)