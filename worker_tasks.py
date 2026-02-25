from crewai import Crew, Process
from agents import verifier, financial_analyst, risk_assessor, investment_advisor
from task import verification_task, analyze_financial_document, risk_task, investment_task


def run_financial_analysis(query: str, file_path:str):
    crew = Crew(
        agents = [verifier, financial_analyst, risk_assessor, investment_advisor],
        tasks = [verification_task, analyze_financial_document, risk_task, investment_task],
        process = Process.sequential,
    )
    
    result = crew.kickoff(
        inputs = {
            "query" : query,
            "file_path" : file_path
        }
    )
    
    
    return str(result)
