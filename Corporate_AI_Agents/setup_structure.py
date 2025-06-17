import os

folders = [
    "app",
    "agents",
    "tools",
    "graph",
    "data",
    "embeddings/faiss_index",
    "config",
    "tests"
]

files = {
    "app/main.py": "",
    "agents/__init__.py": "",
    "agents/planner.py": "",
    "agents/researcher.py": "",
    "agents/coder.py": "",
    "agents/reviewer.py": "",
    "agents/tester.py": "",
    "tools/__init__.py": "",
    "tools/rag_tool.py": "",
    "tools/utility_tool.py": "",
    "graph/__init__.py": "",
    "graph/graph_builder.py": "",
    "config/settings.py": "",
    "tests/test_agents.py": "",
    "requirements.txt": "",
    "README.md": "",
    ".env": ""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

print("✅ Project structure created successfully.")
