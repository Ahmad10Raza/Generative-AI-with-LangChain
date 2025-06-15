import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from io import BytesIO
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain.utilities import SQLDatabase
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# --- DATABASE CONFIGURATION ---
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "Ahmad10Raza",
    "password": "@786&md#AS",
    "database": "retail_sales_db"
}

# Build DB URI with encoded password
encoded_password = quote_plus(db_config["password"])
db_uri = f"mysql+pymysql://{db_config['user']}:{encoded_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# --- Connect using SQLDatabase and SQLAlchemy ---
db = SQLDatabase.from_uri(db_uri)
engine = create_engine(db_uri)

# --- SETUP OPENAI LLM ---
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# --- Create SQL Query Chain ---
sql_chain = create_sql_query_chain(llm, db)

# --- Initialize history ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Streamlit UI ---
st.set_page_config(page_title="Chat with MySQL DB", layout="centered")
st.title("📊 Chat with Your MySQL Database")
st.markdown("Ask a question about your `sales_tb` table. Example: `What is the total sales by month?`")

user_query = st.text_input("🧠 Enter your natural language question")

if user_query:
    with st.spinner("Thinking..."):
        try:
            # Step 1: Generate SQL
            sql_query = sql_chain.invoke({"question": user_query}).strip("```sql").strip("```").strip()

            # Step 2: Execute SQL safely
            with engine.connect() as conn:
                result = conn.execute(text(sql_query))
                rows = result.fetchall()
                columns = result.keys()
                df = pd.DataFrame(rows, columns=columns)

            # Step 3: Save to history
            st.session_state.history.append({"question": user_query, "sql": sql_query, "df": df})

            # Step 4: Show results
            st.subheader("📝 Generated SQL Query")
            st.code(sql_query, language="sql")

            st.subheader("📊 Query Results")
            st.dataframe(df)

            # Step 5: Download button
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            st.download_button(
                label="📥 Download as Excel",
                data=output.getvalue(),
                file_name="query_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- Display History ---
if st.session_state.history:
    st.sidebar.title("📜 Query History")
    for i, entry in enumerate(reversed(st.session_state.history)):
        with st.sidebar.expander(f"Query {len(st.session_state.history) - i}"):
            st.markdown(f"**Q:** {entry['question']}")
            st.code(entry['sql'], language="sql")
            st.dataframe(entry['df'])
