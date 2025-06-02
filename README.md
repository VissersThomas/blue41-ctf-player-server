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

### 3. Set up Python environment
Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python requirements
```bash
pip install -r requirements.txt 
```

### 5. Run the server
You will need the Milvus connection details (which you'll get after creating your team on ctf.blue41.com), as well as an OPENAI API key.
Execute the server setup script:
```bash
python start_server.py
```

### 6. Start playing
Your application is now ready to use!

## Protect Your Application

### Input Guardrails
Configure your input guardrails policy `config/config.yml`. 
Kill (CTRL+C) and restart the server with `python start_server.py` for changes to take effect.

⚠️ **Warning**: Only minimal downtime is allowed when restarting. Applications must remain available for other contestants.
