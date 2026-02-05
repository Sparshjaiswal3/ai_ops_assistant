from tools import TOOL_REGISTRY

class ExecutorAgent:
    def execute_plan(self, plan_data):
        results = {}
        print("--> Executor: Starting execution...")
        
        if "plan" not in plan_data:
            return {"error": "Invalid plan format"}

        for step in plan_data["plan"]:
            step_id = step["step_id"]
            tool_name = step.get("tool")
            args = step.get("arguments", {})
            description = step.get("description")

            print(f"    [Step {step_id}] {description} | Tool: {tool_name}")

            if tool_name in TOOL_REGISTRY:
                tool_instance = TOOL_REGISTRY[tool_name]()
                

                if tool_name == "github_search":
                    output = tool_instance.execute(
                        query=args.get("query"),
                        limit=args.get("limit", 5)
                    )
                elif tool_name == "get_weather":
                    output = tool_instance.execute(args.get("city"))
                else:
                    output = "Tool arguments not mapped."
                
                results[step_id] = {"tool": tool_name, "output": output}
            else:
                results[step_id] = {"output": "No tool executed or tool not found."}
        
        return results