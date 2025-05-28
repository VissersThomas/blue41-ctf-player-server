# CTF Blue41 RAG User App

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
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Run the server
Execute the server setup script:
```bash
python start_server.py
```

### 5. Start playing
Your application is now ready to use!

## Protect Your Application

### Input Guardrails
Configure input guardrails in `config/config.yml`. Restart the server with `python start_server.py` for changes to take effect.

⚠️ **Warning**: Only minimal downtime is allowed when restarting. Applications must remain available for other contestants.