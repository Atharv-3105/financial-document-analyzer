from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
# import asyncio

from crewai import Crew, Process
from agents import financial_analyst, verifier, risk_assessor, investment_advisor
from task import analyze_financial_document, verification_task, risk_task, investment_task

from schema import AnalysisResponse, ErrorResponse
from queue_worker import queue
from worker_tasks import run_financial_analysis
from rq.job import Job
from redis import Redis

app = FastAPI(title="Financial Document Analyzer",
              description=(
                  "Multi-agent AI-powered financial document analysis system.\n\n"
                  "This API allows users to upload financial PDFs and receive:\n"
                  "- Structured financial analysis\n"
                  "- Risk assessment\n"
                  "- Strategic investment considerations\n\n"
                  "*** This system DOES NOT provide personalized financial advice."
              ),
              version="1.0.0")

def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew"""
    financial_crew = Crew(
        agents=[verifier, financial_analyst, risk_assessor, investment_advisor],
        tasks=[verification_task, analyze_financial_document, risk_task, investment_task],
        process=Process.sequential,
    )
    
    result = financial_crew.kickoff(
        inputs = {
            "query" : query,
            "file_path" : file_path
        }
    )
    return result

@app.get("/health")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze", tags=["Financial Document Analysis"],
          response_model=AnalysisResponse,
          responses={
              500: {"model":ErrorResponse}
          },
          summary = "Analyze Financial PDF document",
          description="upload a financial PDF and receive structured multi-agent financial analysis.")

async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(default="Provide financial insights from this document.")
):

    file_id = str(uuid.uuid4())
    #Ensure the Data Directory exists
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{file_id}.pdf"
    
    try:
        contents = await file.read()
        #Save the file
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Validate query
        if query=="" or query is None:
            query = "Analyze this financial document for investment insights"
            
        # Process the financial document with all analysts
        response = run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)