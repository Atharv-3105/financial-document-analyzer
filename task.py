## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, risk_assessor, investment_advisor
from tools import FinancialDocumentTool


#=========Create task for document verification============
verification_task = Task(
    description=(
        "Read the document at {file_path}. "
        "Determine whether it is a legitimate financial document. "
        "Check for presence of financial statements, earnings data, "
        "balance sheet, income statement, or risk disclosures."
    ),
    expected_output=(
        "Return:\n"
        "- 'Valid Financial Document' OR\n"
        "- 'Invalid Document'\n"
        "Provide brief reasoning."
    ),
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
)

#=========Create task for analyzing financial document=============
analyze_financial_document = Task(
    description=(
        "You are given a financial document located at: {file_path}. \n\n"
        "Step 1: Read the entire document carefully.\n"
        "Step 2: Extract key financial data including (if available):\n"
        "- Revenue\n"
        "- Net income\n"
        "- Operating income\n"
        "- Cash flow\n"
        "- Debt levels\n"
        "- Growth metrics\n"
        "- Risk disclosures\n\n"
        "Step 3: Based strictly on extracted data, answer the user's query:\n"
        "{query}\n\n"
        "Important Rules:\n"
        "- Only use information explicitly present in the document. \n"
        "- If specifix data is not found, clearly state 'Not mentioned in document. \n"
        "- Do NOT fabricate numbers, URLs, or market predictions.\n"
        "- Do NOT provide personalized financial advice.\n"
        "- Keep analysis objective and professional."
    ),
    expected_output=(
        "Return a structured financial analysis in the following format:\n\n"
        "1. Executive Summary\n"
        "2. Key Financial Metrics (Bullet Points)\n"
        "3. Profitability & Revenue Analysis\n"
        "4. Liquidity & Cash Flow Analysis\n"
        "5. Evidence-Based Insights Relevant to User Query\n"
        "6. Limitations (If data missing, explicitly state it)\n\n"
        "Do not include external references or speculative commentary."
    ),
    agent = financial_analyst,
    tools = [FinancialDocumentTool.read_data_tool],
)

#==========Create task for Risk_Analysis==============
risk_task = Task(
    description=(
        "Based on the financial analysis provided earlier, "
        "identify financial risks including:\n"
        "- Liquidity risk\n"
        "- Debt exposure\n"
        "- Revenue volatility\n"
        "- Operational risks\n"
        "Only rely on extracted financial evidence."
    ),
    expected_output=(
        "1. Key Risk Categories\n"
        "2. Risk Severity (Low/Medium/High)\n"
        "3. Supporting Evidence from Document\n"
        "4. Risk Summary"
    ),
    agent=risk_assessor,
)


#===========Create Investment Strategy Task==================
investment_task = Task (
    description= (
        "Based on the financial analysis and risk assessment, "
        "provide strategic investment considerations.\n\n"
        "Important:\n"
        "-Do NOT provide personalized financial advice.\n"
        "-Do NOT recommend specific financial products.\n"
        "- Focus on strategic interpretation of financial strength and risk profile.\n"
        "- Base reasoning strictly on previously extracted financial evidence."
    ),
    expected_output = (
        "1. Financial Strength Summary\n"
        "2. Growth Outlook (Evidence-Based)\n"
        "3. Risk-Adjusted Considerations\n"
        "4. Strategic Positioning Insights\n"
        "5. Disclaimer: Not Financial Advice"
    ),
    agent = investment_advisor,
)