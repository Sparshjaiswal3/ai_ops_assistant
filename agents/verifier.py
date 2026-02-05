from llm.wrapper import LLMNode

VERIFIER_PROMPT = """
You are a Verifier Agent. 
You will receive:
1. The original user request.
2. The execution results from tools.

Your job:
1. Validate if the results satisfy the request.
2. Summarize the findings into a clear, natural language response.
3. If data is missing, mention what failed.

Output JSON:
{
    "status": "success" or "incomplete",
    "final_answer": "Your summary here..."
}
"""

class VerifierAgent:
    def __init__(self):
        self.llm = LLMNode(VERIFIER_PROMPT)

    def verify(self, original_request, execution_results):
        print("--> Verifier: Validating results...")
        context = f"Request: {original_request}\nResults: {execution_results}"
        return self.llm.generate(context, json_mode=True)