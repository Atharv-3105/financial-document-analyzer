from langchain_core.messages import AIMessage

class MockLLM:
    def invoke(self, input, **kwargs):
        return AIMessage(
            content="""
{
  "executive_summary": "Mock financial summary.",
  "key_metrics": {},
  "profitability_analysis": "Mock profitability.",
  "liquidity_analysis": "Mock liquidity.",
  "query_insights": "Mock insights.",
  "limitations": "Mock limitations."
}
"""
        )