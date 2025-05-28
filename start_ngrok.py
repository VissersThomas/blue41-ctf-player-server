#!/usr/bin/env python3
"""
Script to set up and configure ngrok for public access.
"""

import subprocess
import time
import requests


def check_ngrok():
    """Check if ngrok is installed"""
    try:
        subprocess.run(["ngrok", "version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def setup_ngrok_auth():
    """Setup ngrok auth token if needed"""
    print("\n🔑 Ngrok requires an auth token for public tunnels.")
    print("   Get your free token from: \033]8;;https://dashboard.ngrok.com/get-started/your-authtoken\033\\https://dashboard.ngrok.com/get-started/your-authtoken\033]8;;\033\\")
    token = input("Enter your ngrok auth token (or press Enter to skip): ").strip()
    
    if token:
        try:
            subprocess.run(["ngrok", "authtoken", token], check=True)
            print("✅ Auth token configured successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to configure auth token")
            return False
    return False


def start_ngrok():
    """Start ngrok tunnel in background"""
    print("\n🌐 Starting ngrok tunnel...")

    try:
        # Build ngrok command for ephemeral URL
        cmd = ["ngrok", "http", "8999", "--log=stdout"]

        # Start ngrok in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait a moment for ngrok to start
        time.sleep(3)

        # Get the public URL from ngrok API
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()["tunnels"]
            if tunnels:
                public_url = tunnels[0]["public_url"]
                print(f"🌍 Public URL: \033]8;;{public_url}\033\\{public_url}\033]8;;\033\\")
                return process, public_url
            else:
                print("❌ No ngrok tunnels found")
                return process, None
        except Exception as e:
            print(f"⚠️  Could not get ngrok URL: {e}")
            print("   Check ngrok dashboard at: \033]8;;http://localhost:4040\033\\http://localhost:4040\033]8;;\033\\")
            return process, None

    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        return None, None


def main():
    print("🌐 Ngrok Setup")
    print("=" * 20)
    
    # Check if ngrok is installed
    if not check_ngrok():
        print("❌ ngrok not found. Please install ngrok first:")
        print("\n📥 Installation instructions:")
        print("   • macOS:    brew install ngrok")
        print("   • Windows:  choco install ngrok")
        print("   • Linux:    snap install ngrok")
        print("   • Web:      \033]8;;https://ngrok.com/download\033\\https://ngrok.com/download\033]8;;\033\\")
        return
    
    print("✅ ngrok is installed")
    
    # Setup auth token
    if not setup_ngrok_auth():
        print("⚠️  Continuing without auth token. Public tunnels may not work.")

    # Start ngrok
    ngrok_process, public_url = start_ngrok()
    
    if ngrok_process and public_url:
        print("\n✅ Ngrok tunnel is running!")
        print(f"🌍 Public URL: \033]8;;{public_url}\033\\{public_url}\033]8;;\033\\")
        print("📱 Local URL: \033]8;;http://localhost:8999\033\\http://localhost:8999\033]8;;\033\\")
        print("\n💡 To use this tunnel:")
        print("   1. Keep this terminal open")
        print("   2. Run your app on port 8999")
        print("   3. Access via the public URL above")
        print("\nPress Ctrl+C to stop ngrok...")
        
        try:
            # Keep the process running
            ngrok_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping ngrok...")
            ngrok_process.terminate()
            print("👋 Ngrok stopped")
    else:
        print("❌ Failed to start ngrok tunnel")


if __name__ == "__main__":
    main()