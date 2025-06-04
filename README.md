# Player server for RAG Attacker-Defender Game

## Getting Started

Follow these steps to set up and run the application:

### 1. Sign up for CTF
Visit [ctf.blue41.com](https://ctf.blue41.com) and sign up, then create a new team.

### 2. Set up ngrok
This exposes will expose your local port on a publically accessible URL.

1. Create ngrok account at [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
2. Copy your ngrok auth token at [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Start the ngrok tunnel on your machine
```bash
NGROK_AUTHTOKEN=xxxxxx ngrok http 8999
```
Alternatively, start the ngrok tunnel via Docker.

*MacOS and Windows*:
```bash
docker run -it -e NGROK_AUTHTOKEN=xxxxxx ngrok/ngrok:latest http host.docker.internal:8999
```
*Linux*:
```bash
docker run --net=host -it -e NGROK_AUTHTOKEN=xxxxxx ngrok/ngrok:latest http 8999
```

4. Submit the endpoint for your team on [ctf.blue41.com](https://ctf.blue41.com) (e.g. https://2a79-178-51-98-11.ngrok-free.app)

### 3. Get and set your Milvus (vector db) credentials
Once you submit an endpoint on ctf.blue41.com, you will get the milvus credentials. Create a .env file (if it didn't exist yet). Add the milvus credentials to it. Also add your OpenAI API key.
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
### 4. Run the server
Execute the server setup script:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python app.py
```

Alternatively (if you have trouble setting up), you can use **Docker** instead.

```bash
docker build -t ctf-player . && docker run -p 8999:8999 --env-file .env ctf-player
```

### 5. Start playing
Your application is now ready to use!

## Protect Your Application

### Input Guardrails
Configure your input guardrails policy `config/config.yml`. 
Kill (CTRL+C) and restart the server with `python start_server.py` for changes to take effect.

⚠️ **Warning**: Only minimal downtime is allowed when restarting. Applications must remain available for other contestants.

