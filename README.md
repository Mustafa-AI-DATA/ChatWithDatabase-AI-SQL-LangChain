# 🖥️ Chat with SQL Database using AI

An intelligent chatbot built with **LangChain**, **Streamlit**, and **Groq API** that allows you to interact with **SQLite** or **MySQL** databases using natural language queries.

## ✨ Features

- 💬 **Natural Language Interface**: Ask questions about your database in plain English
- 🗄️ **Multi-Database Support**: Works with SQLite and MySQL
- ⚡ **Fast Processing**: Powered by Groq's high-speed LLM inference
- 🎨 **User-Friendly UI**: Built with Streamlit for seamless interaction
- 📝 **Conversation History**: Maintains chat history within sessions
- 🔒 **Secure**: API keys handled securely via environment variables
- 🛡️ **Error Handling**: Comprehensive error management and logging

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Groq API Key ([Get one free](https://groq.com))
- SQLite or MySQL database

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mustafa-AI-DATA/ChatWithDatabase-AI-SQL-LangChain.git
   cd ChatWithDatabase-AI-SQL-LangChain
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

### Running the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 Usage

### Using SQLite (Default)
1. Select "Use SQLite Database (student.db)" from sidebar
2. Enter your Groq API Key
3. Start asking questions!

### Using MySQL
1. Select "Connect to MySQL Database"
2. Enter your MySQL credentials:
   - Host (e.g., localhost)
   - Username
   - Password
   - Database name
3. Enter your Groq API Key
4. Ask away!

## 💡 Example Queries

```
"Show me all tables in the database"
"How many records are in the students table?"
"What's the total number of entries?"
"List all students with age greater than 20"
"Show me the top 5 oldest records"
"Count students grouped by department"
```

## 🔧 Configuration

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Logger level
- Upload size limits
- Security settings

## 🏗️ Project Structure

```
.
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version for deployment
├── .streamlit/
│   └── config.toml      # Streamlit configuration
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── student.db           # Sample SQLite database
└── README.md            # This file
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "API Key error" | Make sure you have a valid Groq API key from [groq.com](https://groq.com) |
| "Database not found" | Verify the database path and file permissions |
| "Connection timeout" | Check MySQL credentials and network connectivity |
| "Import errors" | Run `pip install -r requirements.txt` again |
| "Streamlit not found" | Make sure you're in the virtual environment |

## 📦 Key Dependencies

- **streamlit** - Web framework
- **langchain** - LLM orchestration
- **langchain-groq** - Groq LLM integration
- **sqlalchemy** - SQL toolkit
- **mysql-connector-python** - MySQL driver

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Select the app and deploy
5. Add secrets in Streamlit Cloud dashboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source under the MIT License.

## 🙏 Support

- **Issues**: [GitHub Issues](https://github.com/Mustafa-AI-DATA/ChatWithDatabase-AI-SQL-LangChain/issues)
- **GitHub**: [Mustafa-AI-DATA](https://github.com/Mustafa-AI-DATA)

---

**Made with ❤️ by [Mustafa-AI-DATA](https://github.com/Mustafa-AI-DATA)**
