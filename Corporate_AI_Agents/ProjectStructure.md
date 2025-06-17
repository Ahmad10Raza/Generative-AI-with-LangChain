LangGraph_AI_Team/
│
├── app/                         # 🌐 Streamlit app logic
│   └── main.py
│
├── agents/                      # 🤖 Individual agent setup
│   ├── __init__.py
│   ├── planner.py
│   ├── researcher.py
│   ├── coder.py
│   ├── reviewer.py
│   └── tester.py
│
├── tools/                       # 🧰 LangChain tools (functions, wrappers)
│   ├── __init__.py
│   ├── rag_tool.py              # Vector search, RAG setup
│   └── utility_tool.py
│
├── graph/                       # 🔁 LangGraph logic
│   ├── __init__.py
│   └── graph_builder.py         # Builds the agent flow
│
├── data/                        # 📂 Knowledge base / SOPs / PDFs
│   └── sample_doc.pdf
│
├── embeddings/                  # 🧠 Vector DB and embedding storage
│   └── faiss_index/
│
├── config/                      # ⚙️ API keys and environment
│   └── settings.py
│
├── tests/                       # ✅ Unit & integration tests
│   └── test_agents.py
│
├── requirements.txt             # 📦 Python dependencies
├── README.md
└── .env                         # 🔐 Environment variables
