import os 
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import read_data_tool, extract_metrics_tool, compute_risk_profile, compute_investment_score
#For testing only
from mockLLM import MockLLM

if os.getenv("OPENAI_API_KEY"):
    llm = ChatOpenAI(
        model = "gpt-4o-mini",
        temperature=0.2
    )
else:
    llm = MockLLM()

#Defining a Document Verifier Agent
#Confirms file is financial, Rejects non-financial PDFs
verifier = Agent(
    role = "Financial Document Verifier",
    goal = "Verify whether the uploaded file is a valid financial document.",
    backstory = (
        "You are a financial compliance officer."
        "You strictly verify whether a document contains financial statements,"
        "corporate disclosures, or accounting data."
    ),
    tools = [read_data_tool],
    verbose = True,
    llm = llm,
    allow_delegation=False
)

# Defining a Financial Analyst Agent
financial_analyst=Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents accurately and provide evidence-based insights.",
    backstory=(
        "You are a CFA-certified financial analyst. "
        "You perform structured financial analysis strictly using document data. "
    ),
    tools=[read_data_tool, extract_metrics_tool],
    verbose=True,
    llm=llm,
    allow_delegation=False  # Allow delegation to other specialists
)

#Defining a Risk Assessor Agent
risk_assessor = Agent(
    role = "Financial Risk Specialist",
    goal = "Assess financial risks using extracted financial data.",
    backstory = (
        "You are a risk management expert focused on liquidity riks, leverage risk, "
        "operational risk, and market exposure."
    ),
    tools=[extract_metrics_tool, compute_risk_profile],
    verbose = True,
    llm = llm,
    allow_delegation = False
)

#Defining an INVESTMENT STRATEGY ANALYST
investment_advisor = Agent(
    role = "Investment Strategy Analyst", 
    goal = "Provide strategic investment considerations based on financial performance and risk profile.",
    backstory = (
        "You are an institutional investment strategist. "
        "You do not provide personalized financial advice. "
        "You provide high-level strategic positioning insights "
        "based strictly on financial analysis and risk evaluation. "
    ),
    tools = [extract_metrics_tool,compute_risk_profile,compute_investment_score],
    verbose = True,
    llm = llm, 
    allow_delegation= False
)


