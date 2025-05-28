#!/usr/bin/env python3
"""
Script to configure environment variables for the application.
Prompts user for missing values and updates the .env file.
"""

import os
import re
from dotenv import load_dotenv, set_key


def load_env_vars():
    """Load existing environment variables from .env file"""
    load_dotenv()
    return {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'MILVUS_HOST': os.getenv('MILVUS_HOST'),
        'MILVUS_PORT': os.getenv('MILVUS_PORT'),
        'MILVUS_USER': os.getenv('MILVUS_USER'),
        'MILVUS_PASSWORD': os.getenv('MILVUS_PASSWORD'),
        'COLLECTION_NAME': os.getenv('COLLECTION_NAME')
    }


def prompt_for_missing_vars(env_vars):
    """Prompt user for missing environment variables"""
    print("🔧 Environment Configuration Setup")
    print("=" * 40)
    
    # Check OpenAI API Key
    if not env_vars['OPENAI_API_KEY']:
        print("\nEnter your OpenAI API Key:")
        print("You can find this at: https://platform.openai.com/api-keys")
        api_key = input("OpenAI API Key: ").strip()
        if api_key:
            env_vars['OPENAI_API_KEY'] = api_key
            set_key('.env', 'OPENAI_API_KEY', api_key)
        else:
            print("❌ OpenAI API Key is required")
            exit(1)
    else:
        print(f"✅ OpenAI API Key already configured")
    
    # Check Milvus Host
    if not env_vars['MILVUS_HOST']:
        print("\nEnter the Milvus database domain:")
        print("Examples: localhost, vdb.blue41.com, 192.168.1.100")
        domain = input("Domain: ").strip()
        if domain:
            env_vars['MILVUS_HOST'] = domain
            set_key('.env', 'MILVUS_HOST', domain)
        else:
            print("❌ Milvus host cannot be empty")
            exit(1)
    else:
        print(f"✅ Milvus host already configured: {env_vars['MILVUS_HOST']}")
    
    # Check Milvus Port
    if not env_vars['MILVUS_PORT']:
        port = "19530"  # Default port
        env_vars['MILVUS_PORT'] = port
        set_key('.env', 'MILVUS_PORT', port)
        print(f"✅ Using default Milvus port: {port}")
    else:
        print(f"✅ Milvus port already configured: {env_vars['MILVUS_PORT']}")
    
    # Check Collection Name
    if not env_vars['COLLECTION_NAME']:
        print("\nEnter the collection name:")
        print("Example: kb_b5rKQ3iUUldk7tim_baibai_bank")
        collection_name = input("Collection name: ").strip()
        if collection_name:
            env_vars['COLLECTION_NAME'] = collection_name
            set_key('.env', 'COLLECTION_NAME', collection_name)
            
            # Extract and set credentials from collection name
            user, password = extract_credentials_from_collection(collection_name)
            env_vars['MILVUS_USER'] = user
            env_vars['MILVUS_PASSWORD'] = password
            set_key('.env', 'MILVUS_USER', user)
            set_key('.env', 'MILVUS_PASSWORD', password)
        else:
            print("❌ Collection name cannot be empty")
            exit(1)
    else:
        print(f"✅ Collection name already configured: {env_vars['COLLECTION_NAME']}")
        
        # Check if credentials need to be set based on collection name
        if not env_vars['MILVUS_USER'] or not env_vars['MILVUS_PASSWORD']:
            user, password = extract_credentials_from_collection(env_vars['COLLECTION_NAME'])
            if not env_vars['MILVUS_USER']:
                env_vars['MILVUS_USER'] = user
                set_key('.env', 'MILVUS_USER', user)
            if not env_vars['MILVUS_PASSWORD']:
                env_vars['MILVUS_PASSWORD'] = password
                set_key('.env', 'MILVUS_PASSWORD', password)
        
        print(f"✅ Milvus credentials configured")


def extract_credentials_from_collection(collection_name):
    """Extract user/password from collection name pattern"""
    # Pattern: kb_{id}_{name}
    match = re.match(r'kb_([^_]+)_(.+)', collection_name)
    if match:
        user_id = match.group(1)
        return f"user_{user_id}", f"pass_{user_id}"
    else:
        print("⚠️  Warning: Could not extract credentials from collection name")
        print("    Using default credentials. You may need to update manually.")
        return "default_user", "default_password"


def install_requirements():
    """Install Python requirements"""
    import subprocess
    import sys
    
    print("\n📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False


def start_server():
    """Start the FastAPI server"""
    import subprocess
    import sys
    
    print("\n🚀 Starting the server...")
    print("📱 Local URL: http://localhost:8999")
    print("🌐 For public access, run: python start_ngrok.py")
    print("Press Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")


def main():
    # Check if we're in the right directory
    if not os.path.exists("remote_vector_store.py"):
        print("❌ Error: remote_vector_store.py not found in current directory")
        print("   Please run this script from the project root directory")
        exit(1)
    
    if not os.path.exists("requirements.txt"):
        print("❌ Error: requirements.txt not found in current directory")
        exit(1)
    
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found in current directory")
        exit(1)
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("""# OpenAI Configuration
OPENAI_API_KEY=

# Milvus Database Configuration
MILVUS_HOST=
MILVUS_PORT=
MILVUS_USER=
MILVUS_PASSWORD=
COLLECTION_NAME=
""")
        print("✅ Created .env file")
    
    # Load existing environment variables
    env_vars = load_env_vars()
    
    # Prompt for missing variables
    prompt_for_missing_vars(env_vars)
    
    print("\n✅ Configuration completed!")
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Please install manually and try again.")
        exit(1)
    
    # Ask if user wants to start the server
    print("\n🚀 Would you like to start the server now? (y/n)")
    start_now = input("Start server: ").strip().lower()
    
    if start_now in ['y', 'yes']:
        start_server()
    else:
        print("\n✅ Setup complete!")
        print("📱 To start locally: python app.py")
        print("🌐 For public access: python start_ngrok.py")


if __name__ == "__main__":
    main()