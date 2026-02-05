import streamlit as st
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent

st.set_page_config(page_title="AI Operations Assistant")

st.title("AI Operations Assistant")
st.markdown("Enter a task that requires **GitHub** or **Weather** data.")

@st.cache_resource
def load_agents():
    return PlannerAgent(), ExecutorAgent(), VerifierAgent()

planner, executor, verifier = load_agents()

task = st.text_input("Enter your task:", placeholder="e.g., Find top 3 AI repos and check weather in New Delhi")

if st.button("Run Task"):
    if not task:
        st.warning("Please enter a task.")
    else:
        with st.spinner("Generating Plan..."):
            plan = planner.create_plan(task)
            with st.expander("View Plan"):
                st.json(plan)
        
        with st.spinner("Executing Tools..."):
            results = executor.execute_plan(plan)
            with st.expander("View Execution Logs"):
                st.json(results)

        with st.spinner("Verifying Results..."):
            final_response = verifier.verify(task, results)
        
        st.success("Task Complete!")
        st.subheader("Final Answer")
        st.info(final_response.get("final_answer"))