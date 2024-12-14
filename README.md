# LLM Observability Demo
This notebook runs a simple `LangGraph` agent that uses custom tools capable of querying the ESPN API for NFL data.

The `LangGraph` traces are automatically logged to both the `LangSmith` and `Arize` observability platforms without the need for annotations or any explicit code. Simply set the platform-specific environment variables. From my experience, traces are captured immediately in `LangSmith` and take a few minutes to reflect in `Arize`.

This demo uses `OpenAI` but could easily use `Anthropic` by replacing `langchain_openai` with `langchain_anthropic`.