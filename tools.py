import os
import re
from pypdf import PdfReader
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()

#============ PDF Reading Tool ============
@tool("financial_document_reader")
def read_data_tool(path: str) -> str:
    """
    Reads and extracts text from a financial PDF document located at the given path.
    Use this to get the raw text content of corporate reports.
    """
    if not os.path.exists(path):
        return f"Error: File not found at {path}"
    
    try:
        reader = PdfReader(path)
        txt = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                # Clean extra whitespace for better LLM processing
                cleaned = " ".join(text.split())
                txt.append(cleaned)
        
        return "\n".join(txt)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

#============ Risk Assessment Tool ============
@tool("risk_profile_calculator")
def compute_risk_profile(metrics: dict) -> dict:
    """
    Computes financial risk ratios (Debt Ratio, Profit Margin, Liquidity) 
    based on a dictionary of financial metrics including revenue, net_income, 
    total_assets, total_liabilities, and cash.
    """
    risk_profile = {}
    
    # Helper to safely get values
    def get_val(k): return metrics.get(k)

    # Compute the DEBT RATIO
    assets = get_val("total_assets")
    liabilities = get_val("total_liabilities")
    risk_profile["debt_ratio"] = liabilities / assets if assets and liabilities else None
    
    # Compute the PROFIT MARGIN
    revenue = get_val("revenue")
    net_income = get_val("net_income")
    risk_profile["profit_margin"] = net_income / revenue if revenue and net_income else None
    
    # Basic Risk classification
    severity = "Low"
    if risk_profile["debt_ratio"] and risk_profile["debt_ratio"] > 0.7:
        severity = "High"
    elif risk_profile["debt_ratio"] and risk_profile["debt_ratio"] > 0.5:
        severity = "Medium"
    
    risk_profile["risk_severity"] = severity
    return risk_profile

#============ Investment Analysis Tool ============
@tool("investment_score_provider")
def compute_investment_score(metrics: dict, risk_profile: dict) -> dict:
    """
    Generates a numerical investment score (0-100) based on financial metrics 
     and a risk profile. Higher scores indicate stronger fundamentals.
    """
    score = 50
    profit_margin = risk_profile.get("profit_margin")
    debt_ratio = risk_profile.get("debt_ratio")
    
    if profit_margin and profit_margin > 0.15: score += 15
    elif profit_margin and profit_margin > 0.05: score += 5
    
    if debt_ratio and debt_ratio < 0.4: score += 10
    elif debt_ratio and debt_ratio > 0.7: score -= 15
    
    return {
        "investment_score": max(0, min(100, score)),
        "interpretation": "Higher score indicates stronger fundamentals with manageable risk."
    }
    
#==========Financial Metrics Extractor Tool============
@tool("financial_metrics_extractor")
def extract_metrics_tool(financial_text: str) -> dict:
    """
    Uses Regex to extract key numerical values from raw financial text.
    Extracts: Revenue, Net Income, Operating Income, Assets, Liabilities, Cash, and Debt.
    Use this immediately after reading the document.
    """
    patterns = {
        "revenue": r"(revenue|total revenue)[^\d]{0,20}([\$]?\d[\d,\.]+)",
        "net_income": r"(net income|net earnings)[^\d]{0,20}([\$]?\d[\d,\.]+)",
        "operating_income": r"(operating income)[^\d]{0,20}([\$]?\d[\d,\.]+)",
        "total_assets": r"(total assets)[^\d]{0,20}([\$]?\d[\d,\.]+)",
        "total_liabilities": r"(total liabilities)[^\d]{0,20}([\$]?\d[\d,\.]+)",
        "cash": r"(cash and cash equivalents|cash)[^\d]{0,20}([\$]?\d[\d,\.]+)",
        "debt": r"(total debt|long[- ]?term debt|debt)[^\d]{0,20}([\$]?\d[\d,\.]+)"
    }
    
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, financial_text, re.IGNORECASE)
        if match:
            # Clean string to float
            value_str = match.group(2).replace(",", "").replace("$", "")
            try:
                extracted[key] = float(value_str)
            except:
                extracted[key] = None
        else:
            extracted[key] = None
            
    return extracted