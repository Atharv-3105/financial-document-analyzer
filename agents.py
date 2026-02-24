from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import FinancialDocumentTool

### Initialize the LLM we will be using
llm = ChatOpenAI(
    model = "gpt-40-mini",
    temperature=0.2
)

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
    tool=[FinancialDocumentTool.read_data_tool],
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
    verbose = True,
    llm = llm, 
    allow_delegation= False
)


