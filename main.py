from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
import uvicorn

app = FastAPI(title="AI Operations Assistant")

planner = PlannerAgent()
executor = ExecutorAgent()
verifier = VerifierAgent()

class TaskRequest(BaseModel):
    task: str

@app.post("/run-task")
async def run_task(request: TaskRequest):
    try:
        plan = planner.create_plan(request.task)
        if "error" in plan:
            raise HTTPException(status_code=500, detail=plan["error"])
        
        execution_results = executor.execute_plan(plan)
        
        final_result = verifier.verify(request.task, execution_results)
        
        return {
            "plan": plan,
            "execution_log": execution_results,
            "final_response": final_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def home():
    return {"message": "AI Assistant is running! Go to /docs to test it."}

if __name__ == "__main__":
    print("Starting AI Operations Assistant...")
    uvicorn.run(app, host="127.0.0.1", port=8000)