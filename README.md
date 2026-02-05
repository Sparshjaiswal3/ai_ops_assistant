# AI Operations Assistant

A local, multi-agent AI system designed to solve natural language tasks by planning, executing, and verifying actions using real-world APIs.

This project implements a **Planner–Executor–Verifier** architecture to autonomously interface with **GitHub** and **OpenWeatherMap**.

---

## Architecture

The system follows a strict multi-agent workflow to ensure reliability and structured reasoning:

1. **Planner Agent**
   Receives the user's natural language request and uses an LLM to generate a structured JSON plan consisting of specific tool calls.

2. **Executor Agent**
   Iterates through the plan, dynamically calling the appropriate Python tools (`github_search`, `get_weather`) and capturing real outputs.

3. **Verifier Agent**
   Analyzes the original request against the execution results to synthesize a final, natural-language response.

---

## Integrated APIs & Tools

| Tool Name       | API Source      | Function                                                        |
| --------------- | --------------- | --------------------------------------------------------------- |
| `github_search` | GitHub REST API | Searches public repositories for names, stars, and descriptions |
| `get_weather`   | OpenWeatherMap  | Fetches current temperature and weather conditions for any city |

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai_ops_assistant.git
cd ai_ops_assistant
```

### 2. Create a Virtual Environment

This project requires **Python 3.10+** (Python **3.11 recommended**).

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named `.env` in the root directory and add your API keys:

```ini
# LLM Provider (Groq is used for high-speed inference)
GROQ_API_KEY=gsk_...

# Tool APIs
GITHUB_TOKEN=ghp_...
OPENWEATHER_API_KEY=...
```

> See `.env.example` for a template.

---

## How to Run

You can run the assistant in three different modes depending on your preference.

### Option A: Interactive UI (Recommended)

Launch a ChatGPT-style web interface using **Streamlit**.

```bash
streamlit run app.py
```

**URL:** [http://localhost:8501](http://localhost:8501)

---

### Option B: API Server

Run the backend as a REST API using **FastAPI**.

```bash
uvicorn main:app --reload
```

* **API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Endpoint:** `POST /run-task`

---

## Example Prompts

Try these prompts to test the agent’s capabilities:

**Weather Check**

```
Check the current weather in Tokyo.
```

**GitHub Research**

```
Find the top 3 AI agent repositories on GitHub.
```

**Multi-Step / Composite Task**

```
Check the weather in London and find popular Python weather libraries on GitHub.
```

**Edge Case (Missing Info)**

```
Get the weather.
```

> The agent should gracefully ask for the missing city or return an appropriate error.

---

## Project Structure

```
ai_ops_assistant/
├── agents/             # Core agent logic
│   ├── planner.py      # Decomposes tasks into JSON plans
│   ├── executor.py     # Executes tools based on the plan
│   └── verifier.py     # Converts results into natural language
├── tools/              # API tool wrappers
│   ├── base.py         # Tool registry decorator
│   ├── github_tool.py  # GitHub API logic
│   └── weather_tool.py # OpenWeatherMap API logic
├── llm/                # LLM interface
│   └── wrapper.py      # Standardized wrapper for Groq/OpenAI
├── main.py             # FastAPI entry point
├── app.py              # Streamlit UI entry point
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

---

## Limitations & Tradeoffs

* **Linear Execution**
  The Executor currently runs steps sequentially. Parallel execution (e.g., checking weather for multiple cities simultaneously) is a potential future improvement.

* **Error Recovery**
  If a tool fails (e.g., API downtime), the Verifier reports the error but does not trigger a re-planning loop.

* **LLM Context & Hallucinations**
  The system uses **Llama-3-70B via Groq**. While powerful, it may occasionally hallucinate tool arguments for ambiguous or overly complex queries.

* **Rate Limits**
  Heavy usage may hit free-tier rate limits on GitHub or OpenWeatherMap APIs.

---

