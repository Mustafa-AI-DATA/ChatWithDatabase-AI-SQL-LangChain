import streamlit as st
from pathlib import Path
import logging
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.agents import AgentType
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Chat with SQL Database",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🖥️ Chat with SQL Database")
st.markdown("*Ask questions about your database in natural language!*")

# Database selection constants
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")
radio_opt = [
    "Use SQLite Database (student.db)",
    "Connect to MySQL Database"
]

selected_opt = st.sidebar.radio(
    label="Choose database:",
    options=radio_opt
)

# Database configuration
db_uri = None
mysql_host = None
mysql_user = None
mysql_password = None
mysql_db = None

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    st.sidebar.subheader("MySQL Configuration")
    mysql_host = st.sidebar.text_input("MySQL Host", placeholder="localhost")
    mysql_user = st.sidebar.text_input("MySQL User", placeholder="root")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database", placeholder="your_database")
else:
    db_uri = LOCALDB

# API Key configuration
st.sidebar.subheader("API Configuration")
api_key = st.sidebar.text_input(
    label="Groq API Key",
    type="password",
    help="Get your API key from https://groq.com"
)

# Validation checks
if not api_key:
    st.warning("⚠️ Please add your Groq API Key in the sidebar to continue.")
    st.stop()

if db_uri == MYSQL and not all([mysql_host, mysql_user, mysql_password, mysql_db]):
    st.warning("⚠️ Please provide all MySQL connection details.")
    st.stop()

# Initialize LLM
try:
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="Gemma2-9b-It",
        streaming=True
    )
except Exception as e:
    st.error(f"❌ Error initializing LLM: {str(e)}")
    st.stop()

# Database configuration function
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    try:
        if db_uri == LOCALDB:
            dbfilepath = (Path(__file__).parent / "student.db").absolute()
            logger.info(f"Using SQLite database at: {dbfilepath}")
            
            if not dbfilepath.exists():
                st.error(f"❌ Database file not found: {dbfilepath}")
                st.stop()
            
            creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
            return SQLDatabase(create_engine("sqlite:///", creator=creator))
        
        elif db_uri == MYSQL:
            if not (mysql_host and mysql_user and mysql_password and mysql_db):
                st.error("❌ Please provide all MySQL connection details.")
                st.stop()
            
            logger.info(f"Connecting to MySQL database: {mysql_db} at {mysql_host}")
            connection_string = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
            return SQLDatabase(create_engine(connection_string))
    
    except Exception as e:
        st.error(f"❌ Database connection error: {str(e)}")
        logger.error(f"Database error: {str(e)}")
        st.stop()

# Configure database
try:
    if db_uri == MYSQL:
        db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
    else:
        db = configure_db(db_uri)
except Exception as e:
    st.error(f"❌ Failed to configure database: {str(e)}")
    st.stop()

# Create toolkit and agent
try:
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )
except Exception as e:
    st.error(f"❌ Error creating agent: {str(e)}")
    logger.error(f"Agent creation error: {str(e)}")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! 👋 I can help you query your database. Ask me anything about your data!"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
user_query = st.chat_input(placeholder="Ask a question about your database...")

# Clear history button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat history cleared! How can I help you?"}
    ]
    st.rerun()

# Process user query
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)
    
    with st.chat_message("assistant"):
        try:
            streamlit_callback = StreamlitCallbackHandler(st.container())
            
            # Use invoke instead of run (new LangChain API)
            response = agent.invoke(
                {"input": user_query},
                callbacks=[streamlit_callback]
            )
            
            # Extract the output
            output = response.get("output", str(response))
            
            st.session_state.messages.append({"role": "assistant", "content": output})
            st.write(output)
            
        except Exception as e:
            error_msg = f"❌ Error processing query: {str(e)}"
            st.error(error_msg)
            logger.error(f"Query error: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Made with ❤️ by Mustafa-AI-DATA**\n\n"
    "[GitHub](https://github.com/Mustafa-AI-DATA) | "
    "[Portfolio](https://mustafa-ai-data.com)"
)
