# Player server for RAG Attacker-Defender Game

## Getting Started

Follow these steps to set up and run the application:

### 1. Sign up for CTF
Visit [ctf.blue41.com](https://ctf.blue41.com) and sign up, then create a new team.

### 2. Start ngrok
Start your ngrok tunnel:
```bash
python start_ngrok.py
```
Submit the public URL to [ctf.blue41.com](https://ctf.blue41.com).
You will get the milvus credentials. Create a .env file (if it didn't exist yet). Add the milvus credentials to it. Also add your OpenAI API key.
```bash
MILVUS_HOST=host
MILVUS_PORT=port
MILVUS_USER=user_
MILVUS_PASSWORD=pass_
COLLECTION_NAME=kb_
OPENAI_API_KEY=your-openai-key
LANGSMITH_API_KEY=your-langsmith-key # Optional
LANGSMITH_TRACING=true # Optional
```



### 3. Set up Python environment
Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Run the server
You will need the Milvus connection details, as well as an OPENAI API key.
Execute the server setup script:
```bash
python start_server.py
```

### 5. Start playing
Your application is now ready to use!
Don't forget to change the guardrails in config/config.yml. Restart the server (python start\_server.py) for changes to take effect!

## Protect Your Application

### Input Guardrails
Configure your input guardrails policy `config/config.yml`. 
Kill (CTRL+C) and restart the server with `python start_server.py` for changes to take effect.

⚠️ **Warning**: Only minimal downtime is allowed when restarting. Applications must remain available for other contestants.
