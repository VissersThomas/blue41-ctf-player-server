# Player server for RAG Attacker-Defender Game

## Getting Started

Follow these steps to set up and run the application:

### 1. Sign up for CTF
Visit [ctf.blue41.com](https://ctf.blue41.com) and sign up, then create a new team.

### 2. Set up Python environment
Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python requirements
```bash
pip install -r requirements.txt 
```

### 4. Start ngrok

1. Create ngrok account at [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
2. Fetch your ngrok auth token at [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Start the ngrok tunnel on your machine using docker (fill in your auth token)

*MacOS and Windows*:
```bash
docker run -it -e NGROK_AUTHTOKEN=your-ngrok-auth-token ngrok/ngrok:latest http host.docker.internal:8999
```
*Linux*:
```bash
docker run --net=host -it -e NGROK_AUTHTOKEN=your-ngrok-auth-token ngrok/ngrok:latest http 8999
```
4. Submit the endpoint for your team on [ctf.blue41.com](https://ctf.blue41.com) (e.g. https://2a79-178-51-98-11.ngrok-free.app)

### 5. Get and set your Milvus (vector db) credentials
Once you submit and endpoint on ctf.blue41.com, you will get the milvus credentials. Create a .env file (if it didn't exist yet). Add the milvus credentials to it. Also add your OpenAI API key.
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

