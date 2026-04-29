# template.py
import os
from pathlib import Path

def create_project_template():
    # 📁 Directories that contain no files (or need .gitkeep)
    empty_dirs = [
        "app/db/migrations",
        "reports"
    ]

    # 📄 Files to create
    files = [
        ".env.example", ".env", "docker-compose.yml", "Dockerfile",
        "pyproject.toml", "requirements.txt", "README.md", "Makefile",
        
        "app/__init__.py", "app/main.py", "app/config.py", "app/dependencies.py",
        
        "app/api/v1/router.py", "app/api/v1/research.py", "app/api/v1/reports.py", "app/api/v1/health.py",
        
        "app/agents/__init__.py", "app/agents/graph.py", "app/agents/state.py", "app/agents/orchestrator.py",
        "app/agents/researcher.py", "app/agents/synthesizer.py", "app/agents/report_builder.py", "app/agents/validator.py",
        
        "app/llm/base.py", "app/llm/groq_provider.py", "app/llm/gemini_provider.py", "app/llm/router.py",
        
        "app/tools/search_tool.py", "app/tools/wikipedia_tool.py", "app/tools/pdf_tool.py",
        
        "app/db/models.py", "app/db/session.py",
        
        "app/tasks/celery_app.py", "app/tasks/research_task.py",
        
        "app/schemas/request.py", "app/schemas/response.py",
        
        "app/utils/logger.py", "app/utils/cache.py", "app/utils/retry.py",
        
        "tests/conftest.py", "tests/unit/test_agents.py", "tests/unit/test_tools.py",
        "tests/integration/test_api.py",
        
        "prompts/researcher.md", "prompts/synthesizer.md", "prompts/report_builder.md"
    ]

    print("🚀 Generating project structure...\n")

    # 1️⃣ Create empty directories + .gitkeep
    for d in empty_dirs:
        dir_path = Path(d)
        dir_path.mkdir(parents=True, exist_ok=True)
        (dir_path / ".gitkeep").touch(exist_ok=True)
        print(f"📁 {d}/")

    # 2️⃣ Create files with safe placeholders
    for f in files:
        path = Path(f)
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            print(f"⚠️  Skipped (already exists): {f}")
            continue

        # Add minimal boilerplate so files aren't completely blank
        if f.endswith(".py"):
            content = f'"""\nModule: {path.name}\nDescription: TODO\n"""\n# TODO: Implement logic\n'
        elif f.endswith(".md"):
            content = f"# {path.stem}\n\n<!-- TODO: Add documentation -->\n"
        elif f == ".env" or f == ".env.example":
            content = "# API Keys & Configuration\n# GROQ_API_KEY=\n# GEMINI_API_KEY=\n# TAVILY_API_KEY=\n"
        elif f == "requirements.txt":
            content = "# Add your pip dependencies here\n# fastapi\n# uvicorn\n# langgraph\n# sqlalchemy\n"
        elif f == "pyproject.toml":
            content = '[project]\nname = "ai-research-agent"\nversion = "0.1.0"\ndescription = "Automated Research Agent"\n'
        elif f == "Makefile":
            content = ".PHONY: run test docker-up\n\nrun:\n\tuvicorn app.main:app --reload --port 8000\n\ntest:\n\tpytest tests/\n\ndocker-up:\n\tdocker-compose up --build\n"
        elif f == "Dockerfile":
            content = "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
        elif f == "docker-compose.yml":
            content = "version: '3.8'\nservices:\n  api:\n    build: .\n    ports:\n      - '8000:8000'\n    env_file:\n      - .env\n"
        elif f == "README.md":
            content = "# 🤖 AI Research Agent\n\nFastAPI + LangGraph + Multi-LLM Research Pipeline.\n\n## Setup\n1. `cp .env.example .env`\n2. `pip install -r requirements.txt`\n3. `make run`\n"
        else:
            content = ""

        path.write_text(content)
        print(f"📄 {f}")

    print("\n✅ Project structure generated successfully!")

if __name__ == "__main__":
    create_project_template()