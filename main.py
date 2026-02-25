from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
# import asyncio

from crewai import Crew, Process
from agents import financial_analyst, verifier, risk_assessor, investment_advisor
from task import analyze_financial_document, verification_task, risk_task, investment_task

from schema import AnalysisResponse, ErrorResponse, QueueResponse
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

# def run_crew(query: str, file_path: str="data/sample.pdf"):
#     """To run the whole crew"""
#     financial_crew = Crew(
#         agents=[verifier, financial_analyst, risk_assessor, investment_advisor],
#         tasks=[verification_task, analyze_financial_document, risk_task, investment_task],
#         process=Process.sequential,
#     )
    
#     result = financial_crew.kickoff(
#         inputs = {
#             "query" : query,
#             "file_path" : file_path
#         }
#     )
#     return result

@app.get("/health")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze", tags=["Financial Document Analysis"],
          response_model=QueueResponse,
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
        
        query = query.strip() or "Analyze this financial document for investment insights."
            
        # Process the financial document with all analysts
        job = queue.enqueue(
            "worker_tasks.run_financial_analysis", 
            query,
            file_path
        )
        
        return {
            "status" : "queued",
            "job_id" : job.id,
            "message" : "Financial Analysis is processing..."
        }
        
    except Exception as e:
        #Clean the file if Enqueueing failed
        if os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

redis_conn = Redis(host = "localhost", port = 6379, db = 0)

@app.get("/status/{job_id}", tags = ["Financial Analysis"]
         , response_model = AnalysisResponse)
def check_status(job_id : str) :
    job = Job.fetch(job_id, connection = redis_conn)
    
    if job.is_finished:
        return {
            "status" : "completed",
            "result" : job.result,
        }
    elif job.is_failed:
        return {
            "status" : "failed",
            "error" : str(job.exc_info)
        }
    else:
        return{
            "status" : "processing"
        }

